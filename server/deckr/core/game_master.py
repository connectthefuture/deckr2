"""
This module provides code for the GameMaster which manages all of the games.
"""

import logging
import pickle

import deckr.core.service
import deckr.game.game

LOGGER = logging.getLogger(__name__)


class GameMaster(deckr.core.service.Service):
    """
    The game master is a pretty straightforwards service. It tracks all games, allows for easy
    querying, creation, and deletion. It also has capabilities for serializing all games for
    later reloading.
    """

    def __init__(self, config=None):
        if config is None:
            config = {}

        self._next_game_id = 0
        self._games = {}
        self._save_file = config.get('save_file', None)

        # Services
        self._action_validator = None
        self._card_library = None

    def start(self):
        """
        Start the game master.
        """

        if self._save_file is not None:
            self.load_from_file(self._save_file)

    def stop(self):
        """
        Stop the game master and do any associated cleanup.
        """

        if self._save_file is not None:
            self.save_to_file(self._save_file)

    def set_action_validator(self, action_validator):
        """
        Set up the action validator.

        Args:
            action_validator (ActionValidator):
        """

        self._action_validator = action_validator

    def set_card_library(self, card_library):
        """
        Set up the card library.
        """

        self._card_library = card_library

    def create(self):
        """
        Create a new game.

        Returns:
            int: The game_id of the newly created game
        """

        game_id = self._next_game_id
        self._next_game_id += 1
        self._games[game_id] = deckr.game.game.MagicTheGathering(
            self._action_validator, self._card_library)
        return game_id

    def destroy(self, game_id):
        """
        Destroy a game. This will delete all players from that game.

        Args:
            game_id (int): The game_id of the game to be destroyed.
        """

        if game_id in self._games:
            del self._games[game_id]

    def get_game(self, game_id):
        """
        Lookup a game by game_id.

        Args:
            game_id (string): The game to lookup.

        Returns:
            MagicTheGathering: The game in question (will throw a KeyError if not found).
        """

        return self._games[game_id]

    def load_from_file(self, file_name):
        """
        Attempt to load all games from a file.

        Args:
            file_name (str): File to load games from.
        """

        LOGGER.info("Loading games from %s", file_name)
        with open(file_name, "rb") as fin:
            self._games = pickle.load(fin)

    def save_to_file(self, file_name):
        """
        Save all games to a file.

        Args:
            file_name (str): File to save games to.
        """

        LOGGER.info("Saving games to %s", file_name)
        with open(file_name, "wb") as fout:
            pickle.dump(self._games, fout)
