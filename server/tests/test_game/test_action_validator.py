"""
Unittests for the action validator.
"""

import unittest
import mock

import deckr.game.action_validator


class ActionValidatorTestCase(unittest.TestCase):

    def setUp(self):
        self.game = mock.MagicMock()
        self.player = mock.MagicMock()  # The player trying to act
        self.action_validator = deckr.game.action_validator.ActionValidator()

    def test_no_priority_pass(self):
        """
        Make sure we can't pass priority if we don't have priority.
        """

        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'pass_priority')

    def test_play_card_priority(self):
        """
        Make sure we can't play a card if we don't have priority.
        """

        card = mock.MagicMock()
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'play', card)

    def test_play_sorcercy_speed(self):
        """
        Make sure we can only play a land at sorcercy speed.
        """

        card = mock.MagicMock()
        card.is_sorcery_speed.return_value = True

        self.game.turn_manager.priority_player = self.player

        # Play during a non main phase
        self.game.turn_manager.phase = 'beginning'
        self.game.turn_manager.step = 'upkeep'
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'play', card)

        # Make sure we can't do it if there's anything on the stack.
        self.game.turn_manager.phase = 'precombat main'
        self.game.turn_manager.step = 'precombat main'
        self.game.stack.is_empty.return_value = False
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'play', card)

    def test_play_land_limit(self):
        """
        We should only be able to play one land per turn.
        """

        card = mock.MagicMock()
        card.is_land.return_value = True
        self.game.turn_manager.phase = 'precombat main'
        self.game.turn_manager.step = 'precombat main'
        self.game.turn_manager.priority_player = self.player

        self.player.land_limit = 1
        self.player.lands_played = 1

        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'play', card)

    def test_play_mana_cost(self):
        """
        Make sure that a player can pay the mana cost for the card they're
        trying to play.
        """

        card = mock.MagicMock()
        card.is_land.return_value = False
        self.game.turn_manager.phase = 'precombat main'
        self.game.turn_manager.step = 'precombat main'
        self.game.turn_manager.priority_player = self.player
        self.player.mana_pool.can_pay.return_value = False

        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'play', card)
