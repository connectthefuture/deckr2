"""
This module provides unittests for the card and card library logic.
"""

import unittest

import deckr.game.card
import mock
import proto.game_pb2 as proto_lib
import tests.utils


class AbilityTestCase(unittest.TestCase):
    """
    Test abilities and the ability factory.
    """

    def test_tap_cost(self):
        """
        Make sure we can use {T} as a cost.
        """

        card = mock.MagicMock()
        player = mock.MagicMock()
        card.tapped = False
        ability_factory = deckr.game.card.AbilityFactory(
            card=card,
            resolution=lambda: None,
            cost="{T}")
        self.assertTrue(ability_factory.can_pay_cost(player))
        ability_factory.pay_cost()
        card.tap.assert_called_with()
        card.tapped = True
        self.assertFalse(ability_factory.can_pay_cost(player))


class CardTestCase(unittest.TestCase):
    """
    Test the functionality associated with a generic card.
    """

    def setUp(self):
        self.card = deckr.game.card.Card()
        self.card.game_id = 0
        self.card.name = "Test Card"
        self.card.tapped = False
        self.card.raw_abilities = ["{T}: Add {G} to your mana pool"]

    def test_activate_ability(self):
        """
        Make sure we can activate a card's ability.
        """

        ability1 = mock.MagicMock()
        ability2 = mock.MagicMock()
        self.card.abilities = [ability1, ability2]
        self.card.activate_ability(0)
        ability1.create_instance.assert_called_with()
        self.card.activate_ability(1)
        ability2.create_instance.assert_called_with()
        self.assertRaises(IndexError, self.card.activate_ability, 2)

    def test_update_proto(self):
        """
        Make sure we can properly update a protobuf.
        """

        proto = proto_lib.Card()
        self.card.update_proto(proto)
        self.assertEqual(proto.name, self.card.name)
        self.assertEqual(proto.tapped, self.card.tapped)
        self.assertEqual(len(proto.abilities), 1)
        self.assertEqual(proto.abilities[0], "{T}: Add {G} to your mana pool")


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
        self.assertEqual(card.raw_abilities, ["{T}: Add {G} to your mana pool"])

    def test_forest_abilities(self):
        """
        Make sure when we create a forest it gets a single ability.
        """

        card = deckr.game.card.Card()
        card.name = "Forest"
        deckr.game.card.populate_abilities(card)
        self.assertEqual(len(card.abilities), 1)


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
