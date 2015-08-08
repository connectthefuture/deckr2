"""
This module provides the code for Players.
"""

from deckr.game.game_object import GameObject
from deckr.game.zone import Zone


class Player(GameObject):
    """
    A player has a number of attributes associated with them (life, etc.) and also is able to
    perform actions.
    """

    def __init__(self, game):
        self.life = 20
        self.poison_counters = 0

        self.hand = Zone('hand', self)
        self.graveyard = Zone('graveyard', self)
        self.library = Zone('library', self)

        self._game = game

    def play_card(self, card):
        pass

    def activate_ability(self, card, ability_index):
        pass

    def declare_attackers(self, attackers):
        pass

    def declare_defenders(self, defenders):
        pass

    def deal_combat_damage(self, comabt_damage):
        pass

    def pass_priority(self):
        pass
