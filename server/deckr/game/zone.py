"""
This module provides code to interact with zones.
"""

import deckr.game.game_object
import proto.game_pb2 as proto_lib


class Zone(deckr.game.game_object.GameObject):
    """
    A zone is really just a collection of game objects. For the most part it looks like a list, but
    it has some extra logic to call triggers.
    """

    def __init__(self, name, owner):
        super(Zone, self).__init__()

        self._objs = []
        self._name = name
        self._owner = owner

    def append(self, obj):
        """
        Add an object to the end of the zone.

        Args:
            obj (object): Object to append to the zone
        """

        self._objs.append(obj)

    def pop(self, index=None):
        """
        Pop an object by index.

        Args:
            index (int): Location to pop from.

        Returns:
            object The popped object.
        """

        if index is not None:
            return self._objs.pop(index)
        return self._objs.pop()

    def insert(self, index, obj):
        """
        Insert an object at a specific index.

        Args:
            index (int): Insertion index
            obj (object): Object to insert
        """

        self._objs.insert(index, obj)

    def remove(self, obj):
        """
        Remove an object by value.

        Args:
            obj (object): Object to remove.
        """

        self._objs.remove(obj)

    def is_empty(self):
        """
        Is the zone empty?
        """

        return not self._objs

    def update_proto(self, proto):
        """
        Update a protobuff.
        """

        super(Zone, self).update_proto(proto)

        for obj in self._objs:
            card_proto = proto.cards.add()
            obj.update_proto(card_proto)

    def __contains__(self, obj):
        return obj in self._objs

    def __len__(self):
        return len(self._objs)

    def __getitem__(self, key):
        return self._objs[key]


class Stack(Zone):
    """
    The stack is a special zone that has additional methods to check the stack
    and resolve the top card.
    """

    def __init__(self, game, *args, **kwargs):
        super(Stack, self).__init__(*args, **kwargs)
        # Need to keep track of the game so we can add to the battlefield
        self._game = game

    def resolve(self):
        """
        Resolve the top card on the stack.
        """

        card = self.pop()
        if card.is_permanent():
            self._game.battlefield.append(card)
        else:
            pass
