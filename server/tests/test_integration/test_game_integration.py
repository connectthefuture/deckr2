"""
This module provides integration tests for the game without spinning up an whole
server/client. Thus, this doesn't test the full stack, but tests the entire
game stack.
"""

import unittest


import nose.plugins.attrib

import deckr.game.game
import deckr.game.card
import deckr.game.action_validator

import tests.utils

# DO NOT IMPORT MOCK. You shouldn't mock anything out in these tests.


@nose.plugins.attrib.attr('integration')
class GameIntegrationTestCase(unittest.TestCase):
    """
    Integration tests for the game to make sure all of the components are
    talking properly.
    """

    def setUp(self):
        self.card_library = deckr.game.card.CardLibrary()
        self.card_library.load_from_dict(tests.utils.SIMPLE_CARD_LIBRARY)
        self.action_validator = deckr.game.action_validator.ActionValidator()
        self.game = deckr.game.game.MagicTheGathering(self.action_validator, self.card_library)

        self.player = self.game.player_manager.create_player([])  # Empty decklist for now.

    def _prep_for_sorcery(self):
        """
        Prepare to play a sorcery speed spell.
        """

        self.game.turn_manager.priority_player = self.player
        self.game.turn_manager.active_player = self.player
        self.game.turn_manager.step = 'precombat main'
        self.game.turn_manager.phase = 'precombat main'

    def test_play_card(self):
        """
        Make sure we can play a card. We need to have the proper mana, then it
        should go on the stack. After everyone passes, it should resolve to the battlefield.
        """

        card = self.card_library.create("Grizzly Bears")
        self.player.hand.append(card)
        self._prep_for_sorcery()

        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.player.play_card, card)
        self.player.mana_pool.add(green=2)
        self.player.play_card(card)
        self.assertNotIn(card, self.player.hand)
        self.assertIn(card, self.game.stack)
        # TODO: Restore this when colorless mana is working
        # self.assertEqual(self.player.mana_pool.green, 0)
        self.player.pass_priority()  # This should allow the spell to resolve
        self.assertIn(card, self.game.battlefield)