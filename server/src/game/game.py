from game.action_validator import ActionValidator
from game.game_loop import GameLoop

class GameRegistry(object):
    def register(self, game_object):
        pass

    def unregister(self, game_object):
        """
        Should this take a game_id ?
        """

    def lookup(self, game_id):
        pass


class MagicTheGathering(object):

    def __init__(self):
        self._game_master = None

        self.game_registry = GameRegistry()
        self.action_validator = ActionValidator()
        self.game_loop = GameLoop()

        # Each game has a set of shared zones
        self.battlefield = Zone('battlefield', None)
        self.exile = Zone('exile', None)
        self.stack = Zone('stack', None)
        self.players = []

        self.game_state = {
            'current_phase': None,
            'current_step': None,
            'active_player': None,
            'priority_player': None,
            'turn_number': 1
        }

    def create_player(self):
        """
        Should this be here? Do we want to ever create players independetly of games?
        """

        pass
