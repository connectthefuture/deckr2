"""
This contains all of the tests directly related to the MagicTheGathering game and it's assocaited
classes.
"""

import unittest

import deckr.game.game
import deckr.game.game_object
import deckr.game.player
import mock
import proto.game_pb2 as game_proto


class PlayerManagerTestCase(unittest.TestCase):
    """
    Test the player manager.
    """

    def setUp(self):
        self.game = mock.MagicMock()
        self.player_manager = deckr.game.game.PlayerManager(self.game)

    def assert_registered(self, obj):
        """
        Assert that an object was registered with the game.
        """

        self.game.registry.register.assert_any_call(obj)

    def test_create_player(self):
        """
        Make sure we can create a player. It should be registered with the game.
        """

        player = self.player_manager.create_player([])
        self.assertIsNotNone(player)
        self.assertTrue(isinstance(player, deckr.game.player.Player))
        self.assertIn(player, self.player_manager.players)
        self.assert_registered(player)
        self.assert_registered(player.hand)
        self.assert_registered(player.library)
        self.assert_registered(player.graveyard)

    def test_create_player_deck(self):
        """
        Make sure we can create a player and their deck.
        """

        card = deckr.game.game_object.GameObject()
        self.game.card_library.create_from_list.return_value = [card]
        player = self.player_manager.create_player(["Forest"])
        self.assertIn(card, player.library)
        self.assert_registered(card)

    def test_start(self):
        """
        Make sure we properly start each player.
        """

        player = self.player_manager.create_player([])
        player.start = mock.MagicMock()
        self.player_manager.start()
        player.start.assert_called_with()


class TurnManagerTestCase(unittest.TestCase):
    """
    Test the turn manager.
    """

    def setUp(self):
        self.turn_manager = deckr.game.game.TurnManager()


class MagicTheGatheringTestCase(unittest.TestCase):
    """
    Test the core game logic
    """

    def setUp(self):
        self.mock_action_validator = mock.MagicMock()
        self.card_library = mock.MagicMock()
        self.game = deckr.game.game.MagicTheGathering(
            self.mock_action_validator, self.card_library)

    def test_update_proto(self):
        """
        Make sure that we properly update the game state proto.
        """

        proto = game_proto.GameState()
        mock_game_object = deckr.game.game_object.GameObject()
        mock_game_object.update_proto = mock.MagicMock()

        # Set up the game
        self.game.turn_manager.current_step = 'untap'
        self.game.turn_manager.current_phase = 'beginning'
        self.game.registry.register(mock_game_object)

        self.game.update_proto(proto)
        self.assertEqual(proto.current_step, 'untap')
        self.assertEqual(proto.current_phase, 'beginning')
        self.assertTrue(mock_game_object.update_proto.called)
        self.assertEqual(len(proto.game_objects), 4)


class GameRegistryTestCase(unittest.TestCase):
    """
    Tests directly related to the game registry.
    """

    def setUp(self):
        self.game_object1 = deckr.game.game_object.GameObject()
        self.game_object2 = deckr.game.game_object.GameObject()
        self.registry = deckr.game.game.GameRegistry()

    def test_register(self):
        """
        Test the register function. It should assign a unique game_id to each game object.
        """

        self.registry.register(self.game_object1)
        self.registry.register(self.game_object2)
        self.assertIsNotNone(self.game_object1.game_id)
        self.assertIsNotNone(self.game_object2.game_id)
        self.assertNotEqual(self.game_object1.game_id,
                            self.game_object2.game_id)

    def test_lookup(self):
        """
        Make sure we can lookup a game object by ID
        """

        self.registry.register(self.game_object1)
        self.assertEqual(self.registry.lookup(
            self.game_object1.game_id), self.game_object1)

    def test_unregister(self):
        """
        Make sure we can unregister an object.
        """

        self.registry.register(self.game_object1)
        self.registry.unregister(self.game_object1)
        self.assertRaises(KeyError, self.registry.lookup,
                          self.game_object1.game_id)
