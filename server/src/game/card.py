from game.game_object import GameObject


def create_card_from_dict(card_data):
    pass

class Card(GameObject):

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)

        self.supertypes = []
        self.types = []
        self.subtypes = []
        self.name = ''
        self.owner = None
        self.controller = None

    def resolve(self):
        """
        Called when the card actually resolves.
        """

        pass

    def reset(self):
        """
        Call whenever a card changes zones to remove and modifications.
        (We'll deal with exceptions eventually.)
        """

# Here we have a set of mixins to help with different card types
class CreatureMixin(object):
    def __init__(self, *args, **kwargs):
        super(CreatureMixin, self).__init__(*args, **kwargs)
        
        self.power = 0
        self.toughness = 0

