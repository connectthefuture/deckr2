from deckr.game.game_object import GameObject


class Ability(GameObject):
    """
    This is for activated or triggered abilities on the stack. These should be somewhat short lived,
    but since they can be targeted, they need to exist as game objects.
    """

    def __init__(self, *args, **kwargs):
        super(Ability, self).__init__(*args, **kwargs)
