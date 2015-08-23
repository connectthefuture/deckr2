"""
This module provides code for various deckr server implementations.
"""

import logging

from twisted.internet import endpoints, protocol, reactor

from deckr.network.connection import Connection
from deckr.network.router import Router
from deckr.services.service import Service
from txsockjs.factory import SockJSFactory

LOGGER = logging.getLogger(__name__)


class DeckrServer(Service):
    """
    An interface for the deckr server.
    """

    def __init__(self, config):
        self._router = Router()
        self._game_master = None
        self._factory = None
        # Load values from config
        self._websockets = config.get('websockets', False)
        self._port = config.get('port', 8080)

    def set_game_master(self, game_master):
        """
        Set the game master (required by the service architecture).

        Args:
            game_master (GameMaster): the game master to set.
        """

        self._game_master = game_master
        self._router.set_game_master(game_master)

    def start(self):
        """
        Start the server. This will be a blocking function call.
        """

        self._factory = DeckrFactory(self._router)
        if self._websockets:
            LOGGER.info("Starting with websocket support")
            self._factory = SockJSFactory(self._factory)

        endpoints.serverFromString(reactor, "tcp:%d" %
                                   self._port).listen(self._factory)
        LOGGER.info('Starting the DeckrServer listening on port %d', self._port)
        reactor.run()

    def stop(self):
        """
        Stop the server and relinquish the control loop.
        """

        if reactor.running:
            reactor.stop()


class DeckrFactory(protocol.Factory):
    """
    A very simple factory for building deckr connetions.
    """

    def __init__(self, router):
        self._router = router

    def buildProtocol(self, _):
        """
        Build the protocol and pass along the router.
        """

        return Connection(self._router)
