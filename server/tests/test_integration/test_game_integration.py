"""
This module provides integration tests for the game without spinning up an whole
server/client. Thus, this doesn't test the full stack, but tests the entire
game stack.
"""

import unittest

import nose.plugins.attrib

import deckr.game.action_validator
import deckr.game.card
import deckr.game.game
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
        self.game = deckr.game.game.MagicTheGathering(self.action_validator,
                                                      self.card_library)

        self.player = self.game.player_manager.create_player([])  # Empty decklist for now.
        self.player2 = self.game.player_manager.create_player([])  # Empty decklist for now.

    def _prep_for_sorcery(self):
        """
        Prepare to play a sorcery speed spell.
        """

        self.game.turn_manager.priority_player = self.player
        self.game.turn_manager.active_player = self.player
        self.game.turn_manager.step = 'precombat main'
        self.game.turn_manager.phase = 'precombat main'

    def _prep_for_attack(self):
        """
        Prepare to declare attackers.
        """

        self.game.turn_manager.priority_player = self.player
        self.game.turn_manager.active_player = self.player
        self.game.turn_manager.step = 'declare attackers'
        self.game.turn_manager.phase = 'combat'

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
        self.assertEqual(self.player.mana_pool.green, 0)
        self.player.pass_priority()  # This should allow the spell to resolve
        self.player2.pass_priority()
        self.assertIn(card, self.game.battlefield)

    def test_activate_land(self):
        """
        Make sure we can activate a mana ability and it doesn't go on the stack.
        """

        forest = self.card_library.create("Forest")
        forest.controller = self.player
        self.game.battlefield.append(forest)
        self._prep_for_sorcery()

        self.player.activate_ability(forest, 0)
        self.assertEqual(self.player.mana_pool.green, 1)
        # Make sure we can't activate it again, since it should be tapped.
        self.assertTrue(forest.tapped)
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.player.activate_ability, forest, 0)

    def test_lose_0_life(self):
        """
        Make sure that a player loses if tehy have 0 life.
        """

        self._prep_for_sorcery()
        self.assertFalse(self.player.lost)
        self.player.life = 0
        self.player.pass_priority()
        self.assertTrue(self.player.lost)

    def test_creature_death(self):
        """
        Make sure we can kill a creature with combat damage.
        """

        self._prep_for_sorcery()
        creature = self.card_library.create("Grizzly Bears")
        creature.owner = self.player
        self.game.battlefield.append(creature)
        creature.deal_combat_damage(2)
        self.player.pass_priority()
        self.assertNotIn(creature, self.game.battlefield)
        self.assertIn(creature, self.player.graveyard)

    def test_summoning_sickness(self):
        """
        Make sure we can't attack with a crature the first turn we play it.
        """

        card = self.card_library.create("Grizzly Bears")
        card.controller = self.player
        self._prep_for_attack()
        self.game.battlefield.append(card)

        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.player.declare_attackers, {card: self.player2})
        card.has_summoning_sickness = False
        self.player.declare_attackers({card: self.player2})
        self.assertTrue(card.attacking)
