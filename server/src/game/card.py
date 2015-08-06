from game.game_object import GameObject


def create_card_from_dict(card_data):
    pass

class Card(GameObject):

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)

    def resolve(self):
        """
        Called when the card actually resolves.
        """

        pass
