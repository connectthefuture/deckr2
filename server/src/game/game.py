from game.action_validator import ActionValidator


class MagicTheGathering(object):

    def __init__(self):
        self._game_master = None
        self._action_validator = ActionValidator()

    def register(self, game_object):
        pass

    def unregister(self, game_object):
        """
        Should this take a game_id ?
        """

    def lookup(self, game_id):
        pass

    def validate(self, action):
        pass
