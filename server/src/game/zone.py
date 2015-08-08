"""
This module provides the code for zones.
"""

from game.game_object import GameObject


class Zone(GameObject):
    """
    A zone is really just a collection of game objects. For the most part it looks like a list, but
    it has some extra logic to call triggers.
    """

    def __init__(self, name, owner):
        self._objs = []
        self._name = name
        self._owner = owner

    def append(self, obj):
        pass

    def pop(self, index=0):
        pass

    def insert(self, index, obj):
        pass

    def remove(self, obj):
        pass
