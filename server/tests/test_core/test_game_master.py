"""
This module tests the game master functionality.
"""

from unittest import TestCase

from mock import MagicMock

from deckr.core.game_master import GameMaster
from deckr.game.game import MagicTheGathering


class GameMasterTestCase(TestCase):

    def setUp(self):
        self.game_master = GameMaster()

    def test_create(self):
        """
        Make sure we can create a new game and then look it up.
        """

        result = self.game_master.create()
        self.assertIsNotNone(result)

    def test_create_unique_ids(self):
        """
        Make sure that if we create two games they get unique ids.
        """

        result1 = self.game_master.create()
        result2 = self.game_master.create()
        self.assertNotEqual(result1, result2)

    def test_get_game(self):
        """
        Make sure we can create a game and then get the actual instance.
        """

        result = self.game_master.create()
        instance1 = self.game_master.get_game(result)
        instance2 = self.game_master.get_game(result)
        self.assertIsNotNone(instance1)
        self.assertTrue(isinstance(instance1, MagicTheGathering))
        # Make sure we get the same object back
        self.assertEqual(instance1, instance2)

    def test_get_game_failure(self):
        """
        Make sure get game throws a KeyError if it can't find a game.
        """

        self.assertRaises(KeyError, self.game_master.get_game, -1)

    def test_destroy(self):
        """
        Once we destroy a game we should no longer be able to access it.
        """

        result = self.game_master.create()
        self.game_master.destroy(result)
        self.assertRaises(KeyError, self.game_master.get_game, result)

    def test_save_file(self):
        """
        Make sure if we have the save_file set we try to load from it and save to it
        properly.
        """

        game_master = GameMaster({'save_file': 'foobar'})
        game_master.save_to_file = MagicMock()
        game_master.load_from_file = MagicMock()
        game_master.start()
        game_master.load_from_file.assert_called_with('foobar')
        game_master.stop()
        game_master.save_to_file.assert_called_with('foobar')
