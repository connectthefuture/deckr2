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

    def test_invalid_action(self):
        """
        We should throw a ValueError if we try to validate an action we don't know about.
        """

        self.assertRaises(ValueError, self.action_validator.validate,
                          self.game, self.player, 'foobar')

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
        card.is_land.return_value = False

        self.game.turn_manager.priority_player = self.player
        self.game.turn_manager.active_player = self.player

        # Play during a non main phase
        self.game.turn_manager.phase = 'beginning'
        self.game.turn_manager.step = 'upkeep'
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'play', card)

        # We should be able to play it if it's a main phase and the stack is empty.
        self.game.turn_manager.phase = 'precombat main'
        self.game.turn_manager.step = 'precombat main'
        self.action_validator.validate(self.game, self.player, 'play', card)

        # Make sure we can't do it if there's anything on the stack.
        self.game.stack.is_empty.return_value = False
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'play', card)

        # We should be able to play an instant speed card here
        card.is_sorcery_speed.return_value = False
        self.action_validator.validate(self.game, self.player, 'play', card)

    def test_play_land_limit(self):
        """
        We should only be able to play one land per turn.
        """

        card = mock.MagicMock()
        card.is_land.return_value = True
        self.game.turn_manager.phase = 'precombat main'
        self.game.turn_manager.step = 'precombat main'
        self.game.turn_manager.priority_player = self.player
        self.game.turn_manager.active_player = self.player

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
        self.game.turn_manager.active_player = self.player

        self.player.mana_pool.can_pay.return_value = False

        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game,
                          self.player, 'play', card)

    def test_declare_attackers(self):
        """
        Test all functionality around declaring attackers.
        """

        attacker = mock.MagicMock()
        attackers = {attacker: self.player}

        # Not the active player
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game, self.player,
                          'declare_attackers', attackers)
        self.game.turn_manager.active_player = self.player

        # Make sure we have to be in the right phase
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game, self.player,
                          'declare_attackers', attackers)

        self.game.turn_manager.phase = 'combat'
        self.game.turn_manager.step = 'declare attackers'
        attacker.tapped = True

        # We can't attack if the creature is tapped
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game, self.player,
                          'declare_attackers', attackers)

        attacker.tapped = False

        # Finally make sure that we allow if everything lines up.
        self.action_validator.validate(self.game, self.player, 'declare_attackers', attackers)

    def test_declare_blockers(self):
        """
        Test all functionality around declaring blockers.
        """

        attacker = mock.MagicMock()
        blocker = mock.MagicMock()
        blockers = {blocker: attacker}

        # Make sure we have to be in the right phase
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game, self.player,
                          'declare_blockers', blockers)

        self.game.turn_manager.phase = 'combat'
        self.game.turn_manager.step = 'declare blockers'
        blocker.tapped = True

        # We can't attack if the creature is tapped
        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.game, self.player,
                          'declare_blockers', blockers)

        blocker.tapped = False

        # Finally make sure that we allow if everything lines up.
        self.action_validator.validate(self.game, self.player, 'declare_blockers', blockers)
