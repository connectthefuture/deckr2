"""
This module provides unittests for the card and card library logic.
"""

from unittest import TestCase

from deckr.game.card import Card, CardLibrary, create_card_from_dict
from tests.utils import FOREST_CARD_DATA, SIMPLE_CARD_LIBRARY


class CardUtilityFunctionsTestCase(TestCase):
    """
    Test the utility functions.
    """

    def test_create_forest_from_dict(self):
        """
        Make sure we can create a basic land from a dict.
        """

        card = create_card_from_dict(FOREST_CARD_DATA)
        self.assertIsNotNone(card)
        self.assertEqual(card.name, "Forest")
        self.assertIn("Land", card.types)
        self.assertIn("Basic", card.supertypes)
        self.assertIn("Forest", card.subtypes)


class CardLibraryTestCase(TestCase):
    """
    Test the card library.
    """

    def setUp(self):
        self.card_library = CardLibrary()

    def test_load_from_dict(self):
        """
        Try to load a card library from a dict and create a card.
        """

        self.card_library.load_from_dict(SIMPLE_CARD_LIBRARY)
        card = self.card_library.create("Forest")
        self.assertIsNotNone(card)
        self.assertEqual(card.name, "Forest") # We do more extensive checking above
