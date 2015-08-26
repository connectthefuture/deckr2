"""
This contains all of the tests directly related to the MagicTheGathering game and it's assocaited
classes.
"""

from unittest import TestCase

from mock import MagicMock

from deckr.game.game import GameRegistry, MagicTheGathering
from deckr.game.game_object import GameObject
from deckr.game.player import Player


class MagicTheGatheringTestCase(TestCase):
    """
    Test the core game logic
    """

    def setUp(self):
        self.mock_action_validator = MagicMock()
        self.card_library = MagicMock()
        self.game = MagicTheGathering(
            self.mock_action_validator, self.card_library)

    def test_create_player(self):
        """
        Make sure we can create a player. It should be registered with the game.
        """

        player = self.game.create_player([])
        self.assertIsNotNone(player)
        self.assertTrue(isinstance(player, Player))
        self.assertIn(player, self.game.players)
        self.assertEqual(
            player, self.game.game_registry.lookup(player.game_id))
        # All player zones should be registered
        self.assertEqual(self.game.game_registry.lookup(player.hand.game_id),
                         player.hand)
        self.assertEqual(self.game.game_registry.lookup(player.graveyard.game_id),
                         player.graveyard)

    def test_create_player_deck(self):
        """
        Make sure we can create a player and their deck.
        """

        card = GameObject()
        self.card_library.create_from_list.return_value = [card]
        player = self.game.create_player(["Forest"])
        self.assertIn(card, player.library)
        self.assertIsNotNone(card.game_id)

    def test_start(self):
        """
        Make sure that when we start a game each player draws a hand of 7 cards.
        """

        cards = [GameObject() for _ in range(10)]
        self.card_library.create_from_list.return_value = cards
        player = self.game.create_player(["Forest"] * 10)
        self.game.start()
        self.assertEqual(len(player.hand), 7)


class GameRegistryTestCase(TestCase):
    """
    Tests directly related to the game registry.
    """

    def setUp(self):
        self.game_object1 = GameObject()
        self.game_object2 = GameObject()
        self.registry = GameRegistry()

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
