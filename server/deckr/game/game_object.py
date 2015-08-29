"""
This module provides the base GameObject and the Zone and Ability game objects
"""

import proto.game_pb2 as proto_lib


class GameObject(object):
    """
    A game object is anything in the game (player, card, zone, etc.). These all have game_ids.
    """

    def __init__(self):
        self.game_id = None

    def update_proto(self, proto):
        """
        Get a protobuf representation of this game object.
        """

        # TODO: Make this raise notimplementederror and actually implement
        # in subcalsses.
        proto.game_id = self.game_id


class Zone(GameObject):
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

    def update_proto(self, proto):
        """
        Update a protobuff.
        """

        super(Zone, self).update_proto(proto)
        proto.game_object_type = proto_lib.GameObject.ZONE

        for obj in self._objs:
            assert obj.game_id is not None
            proto.zone.objs.append(obj.game_id)

    def __contains__(self, obj):
        return obj in self._objs

    def __len__(self):
        return len(self._objs)

    def __getitem__(self, key):
        return self._objs[key]


class Ability(GameObject):
    """
    This is for activated or triggered abilities on the stack. These should be somewhat short lived,
    but since they can be targeted, they need to exist as game objects.
    """

    def __init__(self, *args, **kwargs):
        super(Ability, self).__init__(*args, **kwargs)
