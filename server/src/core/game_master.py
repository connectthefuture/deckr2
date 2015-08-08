"""
This module provides code for the GameMaster which manages all of the games.
"""


from services.service import Service


class GameMaster(Service):
    """
    The game master is a pretty straightforwards service. It tracks all games, allows for easy
    querying, creation, and deletion. It also has capabilities for serializing all games for
    later reloading.
    """

    def __init__(self, config=None):
        if config is None:
            config = {}

        self._games = {}
        self._save_on_quit = config.get('save_on_quit', False)

        # Services
        self._action_validator = None

    def start(self):
        """
        Start the game master.
        """

        pass

    def stop(self):
        """
        Stop the game master and do any associated cleanup.
        """

        pass

    def set_action_validator(self, action_validator):
        """
        Set up the action validator.

        Args:
            action_validator (ActionValidator):
        """

    def create(self, options=None):
        """
        Create a new game. Takes in an optional dictionary for configuration. This will just
        be passed directly to the game.

        Returns:
            MagicTheGathering: The newly created game instance.
        """

        pass

    def destroy(self, game_id):
        """
        Destroy a game. This will delete all players from that game.

        Args:
            game_id (string): The game_id of the game to be destroyed.
        """

        pass

    def get_game(self, game_id):
        """
        Lookup a game by game_id.

        Args:
            game_id (string): The game to lookup.

        Returns:
            MagicTheGathering: The game in question (will throw a KeyError if not found).
        """

        pass

	def load_from_file(self, file_name):
		"""
		Attempt to load all games from a file.

        Args:
            file_name (str): File to load games from.
		"""

		pass

	def save_to_file(self, file_name):
		"""
		Save all games to a file.

        Args:
            file_name (str): File to save games to.
		"""

		pass
