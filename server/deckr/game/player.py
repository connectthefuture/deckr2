"""
This module provides the code for Players.
"""

import deckr.game.game_object
import deckr.game.zone


def mana_pool_from_string(string):
    """
    Create a mana pool from a string.
    """

    mana_pool = ManaPool()
    white = string.count("W")
    blue = string.count("U")
    black = string.count("B")
    red = string.count("R")
    green = string.count("G")
    remainder = ''.join(c for c in string if c not in "WUBRG")
    if remainder:
        colorless = int(remainder)
    else:
        colorless = 0
    mana_pool.add(white=white,
                  blue=blue,
                  black=black,
                  red=red,
                  green=green,
                  colorless=colorless)
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
        return (self.white >= other.white and self.blue >= other.blue and
                self.black >= other.black and self.red >= other.red and
                self.green >= other.green and self.total() >= other.total())

    def total(self):
        """
        Return the total mana in this pool.
        """

        return self.white + self.blue + self.black + self.red + self.green + self.colorless

    def subtract(self, amount):
        """
        Remove the amount specified from this mana pool.
        """

        other = mana_pool_from_string(amount)
        if other.total() == self.total():
            self.reset()
            return

        # TODO: Support not exact mana costs.
        raise NotImplementedError("Deckr only supports exact mana right now")

    def reset(self):
        """
        Set all values to 0.
        """

        self.white = 0
        self.blue = 0
        self.black = 0
        self.red = 0
        self.green = 0
        self.colorless = 0

    def update_proto(self, proto):
        """
        Update a proto.
        """

        super(ManaPool, self).update_proto(proto)
        proto.white = self.white
        proto.blue = self.blue
        proto.black = self.black
        proto.red = self.red
        proto.green = self.green


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

    def deal_combat_damage(self, amount):
        """
        Deal combat damage to the player.
        """

        self.life -= amount

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

        self._game.action_validator.validate(self._game, self, 'activate',
                                             card, ability_index)

        # Pay the cost first
        card.abilities[ability_index].pay_cost()
        ability = card.activate_ability(ability_index)
        # Don't do this for non mana abilities.
        ability.resolve()

    def declare_attackers(self, attackers):  # pylint: disable=no-self-use
        """
        Declare attackers. All cards will be updated to indicate they are attacking.
        """

        self._game.action_validator.validate(self._game, self, 'declare_attackers',
                                             attackers)
        for attacker in attackers:
            attacker.attacking = attackers[attacker]

    def declare_blockers(self, blockers):
        """
        Declare blockers. All cards will be updated to indicate they are defending.
        """

        self._game.action_validator.validate(self._game, self, 'declare_blockers',
                                             blockers)

        for blocker in blockers:
            blocker.blocking = blockers[blocker]

    def assign_combat_damage(self, comabt_damage):
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
        self.graveyard.update_proto(proto.graveyard)
        self.library.update_proto(proto.library)
        self.hand.update_proto(proto.hand)
        self.mana_pool.update_proto(proto.mana_pool)
        proto.life = self.life
        proto.lost = self.lost
