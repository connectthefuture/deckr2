"""
This module provides the code for Players.
"""

import deckr.game.game_object
import deckr.game.zone
import proto.game_pb2 as proto_lib


class Player(deckr.game.game_object.GameObject):
    """
    A player has a number of attributes associated with them (life, etc.) and also is able to
    perform actions.
    """

    def __init__(self, game):
        super(Player, self).__init__()

        self.life = 20
        self.poison_counters = 0

        self.hand = deckr.game.zone.Zone('hand', self)
        self.graveyard = deckr.game.zone.Zone('graveyard', self)
        self.library = deckr.game.zone.Zone('library', self)

        self.lost = False

        self._game = game

    def draw(self):
        """
        Draw a card.
        """

        if len(self.library) == 0:
            self.lost = True
        else:
            self.hand.append(self.library.pop())

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

        assert card in self.hand
        # Lands don't use the stack
        if card.is_land():
            self.hand.remove(card)
            self._game.battlefield.append(card)

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
        proto.player.life = self.life
        proto.player.lost = self.lost
