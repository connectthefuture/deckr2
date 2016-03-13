"""
This module tests the router to make sure it can properly route requests.
"""

import unittest

import deckr.game.action_validator
import deckr.network.router
import mock
import proto.client_message_pb2
import proto.server_response_pb2


class RouterTestCase(unittest.TestCase):
    """
    Test the core router functionality.
    """

    def setUp(self):
        self.router = deckr.network.router.Router()
        self.game_master = mock.MagicMock()
        self.connection = mock.MagicMock()
        self.game = mock.MagicMock()
        self.router.set_game_master(self.game_master)

    def _create_and_join_game(self):
        """
        Utility to make sure that the client is part of a game.
        """

        self.router.create_room(0, self.game)
        self.router.add_to_room(self.connection, 0)
        # Mock out the player
        self.connection.player = mock.MagicMock()

    def test_create(self):
        """
        A create message should call create on the game master and then return a create response.
        """

        game_id = 0
        self.game_master.create.return_value = game_id

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.CREATE

        expected_response = proto.server_response_pb2.ServerResponse()
        expected_response.response_type = proto.server_response_pb2.ServerResponse.CREATE
        expected_response.create_response.game_id = game_id

        self.router.handle_message(message, self.connection)
        self.game_master.create.assert_called_with()
        self.connection.send_response.assert_called_with(expected_response)
        # No one should be in the game yet
        self.assertEqual(self.router.get_room_connections(game_id), [])

    def test_join(self):
        """
        A join message should lookup the game and then join the game room. It should return a
        join response.
        """

        game_id = 0
        player = mock.MagicMock()
        self.router.create_room(game_id, None)
        self.game_master.get_game.return_value = self.game
        self.game.player_manager.create_player.return_value = player
        player.game_id = 1

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.JOIN
        message.join_message.client_type = proto.client_message_pb2.JoinMessage.PLAYER
        message.join_message.game_id = game_id
        message.join_message.player_config.deck.append("Forest")

        expected_response = proto.server_response_pb2.ServerResponse()
        expected_response.response_type = proto.server_response_pb2.ServerResponse.JOIN
        expected_response.join_response.player_id = player.game_id

        self.router.handle_message(message, self.connection)
        self.game_master.get_game.assert_called_with(game_id)
        self.game.player_manager.create_player.assert_called_with(["Forest"])
        self.connection.send_response.assert_called_with(expected_response)

        # Make sure we were added to the room
        self.assertIn(self.connection,
                      self.router.get_room_connections(game_id))

        self.assertIsNotNone(self.connection.player)

    def test_leave(self):
        """
        Make sure that we can properly handle a leave message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.LEAVE

        expected_response = proto.server_response_pb2.ServerResponse()
        expected_response.response_type = proto.server_response_pb2.ServerResponse.LEAVE

        self.router.handle_message(message, self.connection)
        self.connection.send_response.assert_called_with(expected_response)

    def test_rooms(self):
        """
        Make sure that we can add a connection to a room.
        """

        room_id = 'foobar'
        self.router.create_room(room_id, None)
        self.router.add_to_room(self.connection, room_id)
        self.assertIn(self.connection,
                      self.router.get_room_connections(room_id))
        self.assertEqual(self.connection.room_id, room_id)

    def test_game_action_start(self):
        """
        Make sure that we can pass a start action on to the game.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.START

        self._create_and_join_game()

        self.router.handle_message(message, self.connection)
        self.game.start.assert_called_with()

    def test_pass_priority(self):
        """
        Make sure a pass priority action is properly relayed.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.PASS_PRIORITY
        self._create_and_join_game()
        self.router.handle_message(message, self.connection)
        self.connection.player.pass_priority.assert_called_with()

    def test_play_card(self):
        """
        Make sure that we can play a card, and that it will properly parse the
        card to play.
        """

        test_object = object()
        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.PLAY
        message.action_message.play.card = 1
        self.game.registry.lookup.return_value = test_object
        self._create_and_join_game()
        self.router.handle_message(message, self.connection)
        # Make sure we look it up in the registry
        self.game.registry.lookup.assert_called_with(1)
        # Make sure we properly sub in the object
        self.connection.player.play_card.assert_called_with(test_object)

    def test_activate_ability(self):
        """
        Make sure we can activate the ability of a card.
        """

        test_object = object()
        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.ACTIVATE
        message.action_message.activate_ability.card = 1
        message.action_message.activate_ability.index = 0
        self.game.registry.lookup.return_value = test_object
        self._create_and_join_game()
        self.router.handle_message(message, self.connection)
        # Make sure we look it up in the registry
        self.game.registry.lookup.assert_called_with(1)
        # Make sure we properly sub in the object
        self.connection.player.activate_ability.assert_called_with(test_object,
                                                                   0)

    def test_declare_attackers(self):
        """
        Make sure that we can declare attackers.
        """

        test_attacker = object()
        test_target = object()
        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        action_message = message.action_message
        action_message.action_type = proto.client_message_pb2.ActionMessage.DECLARE_ATTACKERS
        declare_attackers = action_message.declare_attackers
        attacker = declare_attackers.attackers.add()
        attacker.attacker = 0
        attacker.target = 1

        self.game.registry.lookup.side_effect = (
            lambda x: test_attacker if x == 0 else test_target)
        self._create_and_join_game()
        self.router.handle_message(message, self.connection)
        # Make sure we look it up in the registry
        self.game.registry.lookup.assert_any_call(0)
        self.game.registry.lookup.assert_any_call(1)
        # Make sure we properly sub in the object
        self.connection.player.declare_attackers.assert_called_with(
            {test_attacker: test_target})

    def test_declare_blockers(self):
        """
        Make sure that we can declare blocker.
        """

        test_blocker = object()
        test_attacker = object()
        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        action_message = message.action_message
        action_message.action_type = proto.client_message_pb2.ActionMessage.DECLARE_BLOCKERS
        declare_blockers = action_message.declare_blockers
        blocker = declare_blockers.blockers.add()
        blocker.blocker = 0
        blocker.blocking = 1

        self.game.registry.lookup.side_effect = (
            lambda x: test_blocker if x == 0 else test_attacker)
        self._create_and_join_game()
        self.router.handle_message(message, self.connection)
        # Make sure we look it up in the registry
        self.game.registry.lookup.assert_any_call(0)
        self.game.registry.lookup.assert_any_call(1)
        # Make sure we properly sub in the object
        self.connection.player.declare_blockers.assert_called_with(
            {test_blocker: test_attacker})

    def test_catches_invlaid_action(self):
        """
        Make sure that if we try to perform an invalid action we get the proper error message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.PASS_PRIORITY
        self._create_and_join_game()
        self.connection.player.pass_priority.side_effect = deckr.game.action_validator.InvalidActionException("foobar")
        self.router.handle_message(message, self.connection)
        self.connection.send_error.assert_called_with("foobar")
