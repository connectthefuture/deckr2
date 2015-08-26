"""
This module provides the code for zones.
"""

from deckr.game.game_object import GameObject


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

    def pop(self, index=0):
        """
        Pop an object by index.

        Args:
            index (int): Location to pop from.

        Returns:
            object The popped object.
        """
        pass

    def insert(self, index, obj):
        """
        Insert an object at a specific index.

        Args:
            index (int): Insertion index
            obj (object): Object to insert
        """

        pass

    def remove(self, obj):
        """
        Remove an object by value.

        Args:
            obj (object): Object to remove.
        """
        pass

    def __contains__(self, obj):
        return obj in self._objs
