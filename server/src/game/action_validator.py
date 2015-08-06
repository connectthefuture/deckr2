class ActionValidator(object):
    """
    Makes sure that actions are legal and if not gives a descriptive error message.
    """

    def __init__(self, game):
        self._game = game

    def validate(self, action):
        pass
