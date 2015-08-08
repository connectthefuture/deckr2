from deckr.network.router import Router
from deckr.services.service import Service


class DeckrServer(Service):
    """
    An interface for the deckr server.
    """

    def __init__(self):
        self._proxy = Proxy()
        self._game_master = None

    def set_game_master(self, game_master):
        """
        Set the game master (required by the service architecture).

        Args:
            game_master (GameMaster): the game master to set.
        """

        pass

    def start(self):
        """
        Start the server. This will be a blocking function call.
        """

        pass

    def stop(self):
        """
        Stop the server and relinquish the control loop.
        """

        pass
