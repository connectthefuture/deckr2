"""
This module tests the game master functionality.
"""

import tempfile
import unittest

import mock
import nose.plugins.attrib

import deckr.core.game_master
import deckr.game.game


class GameMasterTestCase(unittest.TestCase):
    """
    This file contains simple tests around the game master.
    """

    def setUp(self):
        self.game_master = deckr.core.game_master.GameMaster()

    def test_create(self):
        """
        Make sure we can create a new game and then look it up.
        """

        result = self.game_master.create()
        self.assertIsNotNone(result)

    def test_service_methods(self):
        """
        Test the simple setters.
        """

        # pylint: disable=protected-access
        action_validator = mock.MagicMock()
        card_library = mock.MagicMock()
        self.game_master.set_action_validator(action_validator)
        self.game_master.set_card_library(card_library)
        self.assertEqual(self.game_master._action_validator, action_validator)
        self.assertEqual(self.game_master._card_library, card_library)
        # Make sure these run properly (they don't really need to do anything)
        self.game_master.start()
        self.game_master.stop()

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
        self.assertTrue(isinstance(
            instance1, deckr.game.game.MagicTheGathering))
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
        # Destruction should not fail if there's nothing to destroy.
        self.game_master.destroy(result)

    def test_save_file(self):
        """
        Make sure if we have the save_file set we try to load from it and save to it
        properly.
        """

        game_master = deckr.core.game_master.GameMaster(
            {'save_file': 'foobar'})
        game_master.save_to_file = mock.MagicMock()
        game_master.load_from_file = mock.MagicMock()
        game_master.start()
        game_master.load_from_file.assert_called_with('foobar')
        game_master.stop()
        game_master.save_to_file.assert_called_with('foobar')

    @nose.plugins.attrib.attr('integration')
    def test_load_and_save_integration(self):
        """
        Actually test the write and read ability to files. We mark this as an
        integration test since it will actually hit a file.
        """

        # pylint: disable=protected-access
        save_file = tempfile.NamedTemporaryFile()
        self.game_master._games = {"foo": "bar"}  # Some fake data
        self.game_master.save_to_file(save_file.name)

        game_master = deckr.core.game_master.GameMaster()
        game_master.load_from_file(save_file.name)
        self.assertEqual(self.game_master._games, game_master._games)
