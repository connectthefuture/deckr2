"""
This module provides code for various deckr server implementations.
"""

import logging

import deckr.core.service
import deckr.network.connection
import deckr.network.router
import twisted.internet.endpoints
import twisted.internet.reactor
import txsockjs.factory

LOGGER = logging.getLogger(__name__)


class DeckrServer(deckr.core.service.Service):
    """
    An interface for the deckr server.
    """

    def __init__(self, config):
        self._router = deckr.network.router.Router()
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
            self._factory = txsockjs.factory.SockJSFactory(self._factory)

        twisted.internet.endpoints.serverFromString(twisted.internet.reactor, "tcp:%d" %
                                                    self._port).listen(self._factory)
        LOGGER.info('Starting the DeckrServer listening on port %d', self._port)
        twisted.internet.reactor.run()

    def stop(self):
        """
        Stop the server and relinquish the control loop.
        """

        if twisted.internet.reactor.running:
            twisted.internet.reactor.stop()


class DeckrFactory(twisted.internet.protocol.Factory):
    """
    A very simple factory for building deckr connetions.
    """

    def __init__(self, router):
        self._router = router

    def buildProtocol(self, _):
        """
        Build the protocol and pass along the router.
        """

        return deckr.network.connection.Connection(self._router)
