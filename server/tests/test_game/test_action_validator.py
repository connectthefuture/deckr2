"""
Unittests for the action validator.
"""

import unittest
import mock

import deckr.game.action_validator

class ActionValidatorTestCase(unittest.TestCase):

    def setUp(self):
        self.game = mock.MagicMock()
        self.player = mock.MagicMock() # The player trying to act
        self.action_validator = deckr.game.action_validator.ActionValidator()

    def test_no_priority_pass(self):
        """
        Make sure we can't pass priority if we don't have priority.
        """

        self.assertRaises(deckr.game.action_validator.InvalidActionException,
                          self.action_validator.validate, self.player,
                          self.game, 'pass_priority')
