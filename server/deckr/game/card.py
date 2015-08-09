"""
This module provides the base code for cards.
"""

from deckr.game.game_object import GameObject


def create_card_from_dict(card_data):
    """
    Create a new card from a dictionary.

    Args:
        card_data (dict): Dictionary containing card data.

    Returns:
        Card The newly created card.
    """

    pass


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
