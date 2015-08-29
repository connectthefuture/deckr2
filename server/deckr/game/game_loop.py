"""
This module provides code related to the game loop.
"""


GAME_ORDER = {
    "beginning": [
        "untap",
        "upkeep",
        "draw"
    ]
}


class GameLoop(object):
    """
    This handles the core game logic when players aren't acting. This will generally be called
    whenever a player completes an action and will run until it requires player action.
    """

    def __init__(self, game):
        self._game = game

    def run_loop(self):
        """
        Run the main game loop. This has a lot of logic embedded in it, but all you need to know
        is that this will run until the next time when user input is needed.
        """

        pass

    def pass_priority(self):
        """
        The priority player will call this when they are done and want to
        pass priorty.
        """

        # Update priority
        active_player = self._game.game_state['active_player']
        next_player = self._game.next_player(
            self._game.game_state['priority_player'])
        self._game.game_state['priority_player'] = next_player

        if next_player == active_player:
            # We've come full circle, either resolve the top item on the stack
            # or move to the next step.
            current_phase = GAME_ORDER[self._game.game_state['current_phase']]
            next_step = current_phase[current_phase.index(
                self._game.game_state['current_step']) + 1]
            self._game.game_state['current_step'] = next_step
