"""
This module provides code for the core game. Most of this is not logic, but instead simply a
container.
"""

from game.game_loop import GameLoop


class GameRegistry(object):
    """
    The game registry is responsible for handing out game_ids.
    """

    def __init__(self):
        self._game_objects = []

    def register(self, game_object):
        """
        Register a new game_object and give it a game_id.

        Args:
            game_object GameObject: The object to register.
        """

        pass

    def unregister(self, game_object):
        """
        Unregister a game_object; will also set it's game_id to None

        Args:
            game_object GameObject: The object to unregister.
        """

    def lookup(self, game_id):
        """
        Find a game object based on the ID.

        Args:
            game_id (int): The id to lookup.

        Returns:
            GameObject the game object with the corresponding ID.
        """

        pass


class MagicTheGathering(object):
    """
    This is the actual game class. Most of the logic is kept out of this class except things
    directly relating to the game.
    """

    def __init__(self, action_validator):
        self._game_master = None

        # Objects inherited from the game_master
        self.action_validator = action_validator

        # Local objects
        self.game_registry = GameRegistry()
        self.game_loop = GameLoop()

        # Each game has a set of shared zones
        self.battlefield = Zone('battlefield', None)
        self.exile = Zone('exile', None)
        self.stack = Zone('stack', None)
        self.players = []

        # Global game stat that doesn't really belong elsewhere.
        self.game_state = {
            'current_phase': None,
            'current_step': None,
            'active_player': None,
            'priority_player': None,
            'turn_number': 1
        }

    def create_player(self):
        """
        Create a new player and register it with this game.

        Returns:
            Player The newly created player
        """

        pass
