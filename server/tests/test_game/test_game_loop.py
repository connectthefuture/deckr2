"""
This module provides some simple tests for the game loop.
"""

import unittest

import deckr.game.game
import deckr.game.game_loop


class GameLoopTestCase(unittest.TestCase):

    def setUp(self):
        self.game = deckr.game.game.MagicTheGathering(None, None)
        self.game_loop = deckr.game.game_loop.GameLoop(self.game)

    def assert_player_step_phase(self, priority_player,
                                 active_player, step, phase):
        """
        Check the priority player, active player, step and phase.
        """

        self.assertEqual(self.game.game_state[
                         'priority_player'], priority_player)
        self.assertEqual(self.game.game_state['active_player'], active_player)
        self.assertEqual(self.game.game_state['current_step'], step)
        self.assertEqual(self.game.game_state['current_phase'], phase)

    def test_pass_priority(self):
        """
        Test that passing priority properly updates the priority player,
        current step, current phase, and active player.
        """

        player1 = object()
        player2 = object()
        self.game.players = [player1, player2]
        self.game.game_state = {
            'current_step': 'upkeep',
            'current_phase': 'beginning',
            'priority_player': player1,
            'active_player': player1
        }

        self.game_loop.pass_priority()
        self.assert_player_step_phase(player2, player1, 'upkeep', 'beginning')
        self.game_loop.pass_priority()
        self.assert_player_step_phase(player1, player1, 'draw', 'beginning')
