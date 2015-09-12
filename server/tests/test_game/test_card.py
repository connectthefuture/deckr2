"""
This module provides unittests for the card and card library logic.
"""

import unittest

import deckr.game.card
import tests.utils


class CardUtilityFunctionsTestCase(unittest.TestCase):
    """
    Test the utility functions.
    """

    def test_create_forest_from_dict(self):
        """
        Make sure we can create a basic land from a dict.
        """

        card = deckr.game.card.create_card_from_dict(
            tests.utils.FOREST_CARD_DATA)
        self.assertIsNotNone(card)
        self.assertEqual(card.name, "Forest")
        self.assertIn("Land", card.types)
        self.assertIn("Basic", card.supertypes)
        self.assertIn("Forest", card.subtypes)


class CardLibraryTestCase(unittest.TestCase):
    """
    Test the card library.
    """

    def setUp(self):
        self.card_library = deckr.game.card.CardLibrary()
        self.card_library.load_from_dict(tests.utils.SIMPLE_CARD_LIBRARY)

    def test_create(self):
        """
        Make sure we can create a single card.
        """

        card = self.card_library.create("Forest")
        self.assertIsNotNone(card)
        # We do more extensive checking above
        self.assertEqual(card.name, "Forest")

    def test_create_from_card_list(self):
        """
        Make sure we can create from a card list.
        """

        cards = self.card_library.create_from_list(
            ["Forest", "Forest", "Forest"])
        self.assertEqual(len(cards), 3)
        for card in cards:
            self.assertEqual(card.name, "Forest")

    def test_is_land(self):
        """
        Make sure we can identify a card as a land.
        """

        forest = self.card_library.create("Forest")
        self.assertTrue(forest.is_land())
