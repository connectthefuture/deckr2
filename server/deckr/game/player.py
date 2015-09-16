"""
This module provides the code for Players.
"""

import deckr.game.game_object
import deckr.game.zone
import proto.game_pb2 as proto_lib


def mana_pool_from_string(str):
    """
    Create a mana pool from a string.
    """

    mana_pool = ManaPool()
    white = str.count("W")
    blue = str.count("U")
    black = str.count("B")
    red = str.count("R")
    green = str.count("G")
    remainder = str.translate(None, "WUBRG")
    if remainder:
        colorless = int(remainder)
    else:
        colorless = 0
    mana_pool.add(white=white, blue=blue, black=black, red=red, green=green, colorless=colorless)
    return mana_pool


class ManaPool(deckr.game.game_object.GameObject):
    """
    A mana pool provides a clean interface for controlling mana. Each player
    has exactly one mana pool.
    """

    # Almost all of these will have 6 arguments. Suppress this.
    # pylint: disable=too-many-arguments
    def __init__(self):
        super(ManaPool, self).__init__()
        self.white = 0
        self.blue = 0
        self.black = 0
        self.red = 0
        self.green = 0
        self.colorless = 0

    def add(self, white=0, blue=0, black=0, red=0, green=0, colorless=0):
        """
        Modify the amount of mana in the pool.
        """

        self.white += white
        self.blue += blue
        self.black += black
        self.red += red
        self.green += green
        self.colorless += colorless

    def can_pay(self, amount):
        """
        Can we pay the given amount (as a string).
        """

        other = mana_pool_from_string(amount)
        return (self.white >= other.white and
                self.blue >= other.blue and
                self.black >= other.black and
                self.red >= other.red and
                self.green >= other.green and
                self.total() >= other.total())

    def total(self):
        """
        Return the total mana in this pool.
        """

        return self.white + self.blue + self.black + self.red + self.green + self.colorless

    def subtract(self, amount):
        """
        Remove the amount specified from this mana pool.
        """

        assert self.can_pay(amount)

        other = mana_pool_from_string(amount)
        self.white -= other.white
        self.blue -= other.blue
        self.black -= other.black
        self.red -= other.red
        self.green -= other.green

        # TODO: Colorless calculation

    def update_proto(self, proto):
        """
        Update a proto.
        """

        super(ManaPool, self).update_proto(proto)
        proto.game_object_type = proto_lib.GameObject.MANA_POOL
        proto.mana_pool.white = self.white
        proto.mana_pool.blue = self.blue
        proto.mana_pool.black = self.black
        proto.mana_pool.red = self.red
        proto.mana_pool.green = self.green


class Player(deckr.game.game_object.GameObject):  # pylint: disable=too-many-instance-attributes
    """
    A player has a number of attributes associated with them (life, etc.) and also is able to
    perform actions.
    """

    def __init__(self, game):
        super(Player, self).__init__()

        self.life = 20
        self.poison_counters = 0

        self.mana_pool = ManaPool()
        self.hand = deckr.game.zone.Zone('hand', self)
        self.graveyard = deckr.game.zone.Zone('graveyard', self)
        self.library = deckr.game.zone.Zone('library', self)

        self.lost = False
        self.lands_played = 0
        self.land_limit = 1  # Some effects might change this.

        self._game = game

    def draw(self):
        """
        Draw a card.
        """

        if len(self.library) == 0:
            self.lost = True
        else:
            self.hand.append(self.library.pop())

    def start_new_turn(self):
        """
        Clear all internal state for a new turn.
        """

        self.lands_played = 0

    def start(self):
        """
        Start the game. Draw the initial hand of 7 cards.
        """

        for _ in range(7):
            self.draw()

    def play_card(self, card):
        """
        Play a card. This will either put the card directly onto the field
        if it's a land, or put it onto the stack.
        """

        self._game.action_validator.validate(self._game, self, 'play', card)

        # Lands don't use the stack
        if card.is_land():
            self.hand.remove(card)
            self._game.battlefield.append(card)
            self.lands_played += 1
        else:  # Otherwise we put it on the stack
            self.hand.remove(card)
            self._game.stack.append(card)
            self.mana_pool.subtract(card.mana_cost)

        card.controller = self

    def activate_ability(self, card, ability_index):  # pylint: disable=no-self-use
        """
        Activate an ability. Resolve it if it's a mana ability, otherwise, put it on the stack.
        """

        card.activate_ability(ability_index)

    def declare_attackers(self, attackers):
        """
        Declare attackers. All cards will be updated to indicate they are attacking.
        """

        pass

    def declare_blockers(self, blockers):
        """
        Declare blockers. All cards will be updated to indicate they are defending.
        """

        pass

    def deal_combat_damage(self, comabt_damage):
        """
        Assign combat damage. Most of the time this should happen automatically, but there
        are some cases when you need to manually assign combat damage.
        """

        pass

    def pass_priority(self):
        """
        Pass priority to the next player.
        """

        self._game.action_validator.validate(self._game, self, 'pass_priority')
        self._game.turn_manager.advance()

    def update_proto(self, proto):
        """
        Update a player proto.
        """

        super(Player, self).update_proto(proto)
        proto.game_object_type = proto_lib.GameObject.PLAYER
        proto.player.graveyard = self.graveyard.game_id
        proto.player.library = self.library.game_id
        proto.player.hand = self.hand.game_id
        proto.player.mana_pool = self.mana_pool.game_id
        proto.player.life = self.life
        proto.player.lost = self.lost
