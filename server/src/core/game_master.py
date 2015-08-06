
class GameMaster(object):

    def __init__(self):
        self._games = {}

    def create(self):
        """
        Create a new game.
        """

        pass

    def destroy(self, game_id):
        """
        Destroy a game.
        """

        pass

	def get_game(self, game_id):
		pass

	def load_from_file(self, file_name):
		"""
		Attempt to load all games from a file.
		"""

		pass

	def save_to_file(self, file_name):
		"""
		Save all games to a file.
		"""
	
		pass
