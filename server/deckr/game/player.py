"""
This module provides the code for Players.
"""

import proto.game_pb2 as proto_lib
from deckr.game.game_object import GameObject
from deckr.game.zone import Zone


class Player(GameObject):
    """
    A player has a number of attributes associated with them (life, etc.) and also is able to
    perform actions.
    """

    def __init__(self, game):
        super(Player, self).__init__()

        self.life = 20
        self.poison_counters = 0

        self.hand = Zone('hand', self)
        self.graveyard = Zone('graveyard', self)
        self.library = Zone('library', self)

        self._game = game

    def play_card(self, card):
        """
        Play a card. This will either put the card directly onto the field
        if it's a land, or put it onto the stack.
        """

        pass

    def activate_ability(self, card, ability_index):
        """
        Activate an ability. Resolve it if it's a mana ability, otherwise, put it on the stack.
        """

        pass

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

        pass

    def update_proto(self, proto):
        """
        Update a player proto.
        """

        super(Player, self).update_proto(proto)
        proto.game_object_type = proto_lib.GameObject.PLAYER
        proto.player.graveyard = self.graveyard.game_id
        proto.player.library = self.library.game_id
        proto.player.hand = self.hand.game_id
        proto.player.life = self.life
