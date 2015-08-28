"""
This module provides the base code for cards.
"""

import json

import proto.game_pb2 as proto_lib
from deckr.game.game_object import GameObject
from deckr.services.service import Service


def create_card_from_dict(card_data):
    """
    Create a new card from a dictionary.

    Args:
        card_data (dict): Dictionary containing card data.

    Returns:
        Card The newly created card.
    """

    card = Card()
    card.name = card_data['name']
    card.types = card_data['types']
    card.subtypes = card_data.get('subtypes', [])
    card.supertypes = card_data.get('supertypes', [])
    return card


class Card(GameObject):
    """
    A card represents a card in magic. Instead of having subclasses we implement all card
    functionality on this class (since basically any card can become any other card type).
    """

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)

        self.supertypes = []
        self.types = []
        self.subtypes = []
        self.name = ''
        self.owner = None
        self.controller = None
        # These will generally be hidden based on the types of the card.
        self.power = 0
        self.toughness = 0

    def reset(self):
        """
        Call whenever a card changes zones to remove any modifications.
        (We'll deal with exceptions eventually.)
        """

        pass

    def update_proto(self, proto):
        """
        Update a protobuf.
        """

        super(Card, self).update_proto(proto)
        proto.game_object_type = proto_lib.GameObject.CARD



class CardLibrary(Service):
    """
    A card library contains all of the cards that can be used, and the ability to create
    instances.
    """

    def __init__(self, config=None):
        super(CardLibrary, self).__init__()

        if config is None:
            config = {}

        self._cards = {}
        self._load_file = config.get('load_from', None)
        library = config.get('library', None)
        if library:
            self.load_from_dict(library)

    def start(self):
        """
        Load up any cards if configured.
        """

        if self._load_file:
            self.load_from_dict(json.load(open(self._load_file)))

    def load_from_dict(self, data):
        """
        Load all of the cards in the given dictionary into the card library. If there
        are conflicting cards the new one will win.
        """

        for key in data:
            self._cards[key] = data[key]

    def create(self, card_name):
        """
        Create a new card.
        """

        return create_card_from_dict(self._cards[card_name])

    def create_from_list(self, card_list):
        """
        A utility method to create cards from a card list.
        """

        return [self.create(x) for x in card_list]
