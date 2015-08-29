"""
This module provides code for the core game. Most of this is not logic, but instead simply a
container.
"""

import logging

import deckr.game.game_loop
import deckr.game.game_object
import deckr.game.player
import deckr.game.zone

LOGGER = logging.getLogger(__name__)


class GameRegistry(object):
    """
    The game registry is responsible for handing out game_ids.
    """

    def __init__(self):
        self._game_objects = {}
        self._next_game_id = 0

    def register(self, game_object):
        """
        Register a new game_object and give it a game_id.

        Args:
            game_object GameObject: The object to register.
        """

        assert isinstance(game_object, deckr.game.game_object.GameObject)
        game_id = self._next_game_id
        game_object.game_id = game_id
        self._next_game_id += 1
        self._game_objects[game_id] = game_object

    def unregister(self, game_object):
        """
        Unregister a game_object.

        Args:
            game_object GameObject: The object to unregister.
        """

        assert game_object.game_id in self._game_objects
        del self._game_objects[game_object.game_id]

    def lookup(self, game_id):
        """
        Find a game object based on the ID.

        Args:
            game_id (int): The id to lookup.

        Returns:
            GameObject the game object with the corresponding ID.
        """

        return self._game_objects[game_id]

    def __getitem__(self, key):
        return self.lookup(key)

    def __iter__(self):
        return self._game_objects.values().__iter__()


class MagicTheGathering(object):
    """
    This is the actual game class. Most of the logic is kept out of this class except things
    directly relating to the game.
    """

    def __init__(self, action_validator, card_library):
        # Objects inherited from the game_master
        self.action_validator = action_validator
        self.card_library = card_library

        # Local objects
        self.game_registry = GameRegistry()
        self.game_loop = deckr.game.game_loop.GameLoop(self)

        # Each game has a set of shared zones
        self.battlefield = deckr.game.zone.Zone('battlefield', None)
        self.exile = deckr.game.zone.Zone('exile', None)
        self.stack = deckr.game.zone.Zone('stack', None)
        self.players = []

        # Global game stat that doesn't really belong elsewhere.
        self.game_state = {
            'current_phase': None,
            'current_step': None,
            'active_player': None,
            'priority_player': None,
            'turn_number': 1
        }

        # Register all game objects
        self.game_registry.register(self.battlefield)
        self.game_registry.register(self.exile)
        self.game_registry.register(self.stack)

        # Private bookkeeping
        self._started = False

    def create_player(self, deck_list):
        """
        Create a new player and register it with this game.

        Returns:
            Player The newly created player
        """

        player = deckr.game.player.Player(self)
        self.game_registry.register(player)
        self.players.append(player)
        # Register zones
        self.game_registry.register(player.hand)
        self.game_registry.register(player.library)
        self.game_registry.register(player.graveyard)
        # Create the deck
        cards = self.card_library.create_from_list(deck_list)
        for card in cards:
            self.game_registry.register(card)
            player.library.append(card)

        return player

    def next_player(self, player):
        """
        Returns the next player in turn order.
        """

        assert player in self.players
        index = self.players.index(player)
        if index == len(self.players) - 1:
            return self.players[0]
        else:
            return self.players[index + 1]

    def start(self):
        """
        Start the game.
        """

        LOGGER.info("Starting game")
        self._started = True

        self.game_state['current_step'] = 'untap'
        self.game_state['current_phase'] = 'beginning'

        # Draw starting hands
        for player in self.players:
            for _ in range(7):
                player.hand.append(player.library.pop())

    def update_proto(self, game_state_proto):
        """
        Update a game state proto to reflect the current game state.
        """

        # Grab the simple global stuff
        game_state_proto.current_step = self.game_state['current_step']
        game_state_proto.current_phase = self.game_state['current_phase']
        for obj in self.game_registry:
            proto = game_state_proto.game_objects.add()
            obj.update_proto(proto)
