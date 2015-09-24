"""
This module provides the base code for cards.
"""

import json

import deckr.core.service
import deckr.game.game_object


def populate_abilities(card):
    """
    At some point this will be greatly expanded to do rules parsing, etc.
    Right now this is in place to allow for quick development. It will take in
    a card and then generate some abilities for it.
    """

    ### Default ability functions. ###
    def forest_ability(ability):
        """{T}: Add {G} to the controller's mana pool."""

        ability.controller.mana_pool.add(green=1)

    ### Ability population ###
    if card.name == "Forest":
        ability_factory = AbilityFactory(card, forest_ability, cost="{T}")
        card.abilities.append(ability_factory)


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
    card.mana_cost = card_data.get('mana_cost', None)
    card.power = card_data.get('power', 0)
    card.toughness = card_data.get('toughness', 0)
    populate_abilities(card)
    return card


class Ability(object):
    """
    Represents an ability on the stack.
    """

    def __init__(self, resolve, controller, *args, **kwargs):
        super(Ability, self).__init__(*args, **kwargs)
        # This is a function that takes in this ability as an argument.
        self.resolve = lambda: resolve(self)
        self.controller = controller


class AbilityFactory(object):
    """
    Creates abilities, generally registered to a card.
    """

    def __init__(self, card, resolution, mana_ability=False, cost=None):
        self.card = card
        self.mana_ability = mana_ability
        self.cost = cost
        self.resolution = resolution

    def can_pay_cost(self, player):  # pylint: disable=unused-argument
        """
        Can we pay the cost (for activated abilities only).
        """

        if "{T}" in self.cost:
            return self.card.tapped == False

    def pay_cost(self):
        """
        Pay the cost for this ability.
        """

        if "{T}" in self.cost:
            self.card.tap()

    def create_instance(self):
        """
        Create a new instance of this ability.
        """

        return Ability(self.resolution, self.card.controller)


class Card(deckr.game.game_object.GameObject):  # pylint: disable=too-many-instance-attributes
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
        self.mana_cost = None
        # Store function pointers for abilities
        self.abilities = []
        # These will generally be hidden based on the types of the card.
        self.power = 0
        self.toughness = 0
        self.tapped = False

        # Transitory state
        self.attacking = None
        self.blocking = None
        self.damage = 0

    def reset(self):
        """
        Call whenever a card changes zones to remove any modifications.
        (We'll deal with exceptions eventually.)
        """

        pass

    def tap(self):
        """
        Tap.
        """

        self.tapped = True

    def untap(self):
        """
        Untap.
        """

        self.tapped = False

    def deal_combat_damage(self, amount):
        """
        Deal combat damage to this card.
        """

        assert "Creature" in self.types
        self.damage += amount

    def is_land(self):
        """
        Check if the card is a land of any type.
        """

        return 'Land' in self.types

    def is_creature(self):
        """
        Is this a creature?
        """

        return 'Creature' in self.types

    def is_sorcery_speed(self):
        """
        Check if we can only cast this at sorcercy speed.
        """

        return not "Instant" in self.types

    def is_permanent(self):
        """
        Is the card a permanent.
        """

        return not "Sorcercy" in self.types and not "Instant" in self.types

    def update_proto(self, proto):
        """
        Update a protobuf.
        """

        super(Card, self).update_proto(proto)
        proto.name = self.name
        if self.controller:
            proto.controller = self.controller.game_id
        proto.tapped = self.tapped

    def activate_ability(self, index):
        """
        Activate an ability for this card.
        """

        return self.abilities[index].create_instance()


class CardLibrary(deckr.core.service.Service):
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
