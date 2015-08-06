from network.proxy import Proxy
from services.service import Service


class DeckrServer(Service):
    """
    An interface for the deckr server.
    """

    def __init__(self):
        self._proxy = Proxy()
        self._game_master = None

    def set_game(self, game):
        pass
