"""
This module tests the router to make sure it can properly route requests.
"""

from unittest import TestCase

from mock import MagicMock

from deckr.network.router import Router
from proto.client_message_pb2 import ActionMessage, ClientMessage, JoinMessage
from proto.server_response_pb2 import ServerResponse


class RouterTestCase(TestCase):
    """
    Test the core router functionality.
    """

    def setUp(self):
        self.router = Router()
        self.game_master = MagicMock()
        self.connection = MagicMock()
        self.game = MagicMock()
        self.router.set_game_master(self.game_master)

    def _create_and_join_game(self):
        """
        Utility to make sure that the client is part of a game.
        """

        self.router.create_room(0, self.game)
        self.router.add_to_room(self.connection, 0)

    def test_create(self):
        """
        A create message should call create on the game master and then return a create response.
        """

        game_id = 0
        self.game_master.create.return_value = game_id

        message = ClientMessage()
        message.message_type = ClientMessage.CREATE

        expected_response = ServerResponse()
        expected_response.response_type = ServerResponse.CREATE
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
        self.router.create_room(game_id, None)
        self.game_master.get_game.return_value = self.game

        message = ClientMessage()
        message.message_type = ClientMessage.JOIN
        message.join_message.client_type = JoinMessage.PLAYER
        message.join_message.game_id = game_id
        message.join_message.player_config.deck.append("Forest")

        expected_response = ServerResponse()
        expected_response.response_type = ServerResponse.JOIN

        self.router.handle_message(message, self.connection)
        self.game_master.get_game.assert_called_with(game_id)
        self.game.create_player.assert_called_with(["Forest"])
        self.connection.send_response.assert_called_with(expected_response)

        # Make sure we were added to the room
        self.assertIn(self.connection,
                      self.router.get_room_connections(game_id))

        self.assertIsNotNone(self.connection.player)

    def test_leave(self):
        """
        Make sure that we can properly handle a leave message.
        """

        message = ClientMessage()
        message.message_type = ClientMessage.LEAVE

        expected_response = ServerResponse()
        expected_response.response_type = ServerResponse.LEAVE

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

        message = ClientMessage()
        message.message_type = ClientMessage.ACTION
        message.action_message.action_type = ActionMessage.START

        self._create_and_join_game()

        self.router.handle_message(message, self.connection)
        self.game.start.assert_called_with()
