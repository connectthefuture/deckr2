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
        self._base64 = config.get('base64', False)
        self._json = config.get('json', False)

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

        if self._base64:
            LOGGER.info("Starting with base64 enconding/decoding")

        if self._json:
            LOGGER.info("Starting with JSON enconding/decoding")

        self._factory = DeckrFactory(self._router, self._base64, self._json)
        if self._websockets:
            LOGGER.info("Starting with websocket support")
            self._factory = txsockjs.factory.SockJSFactory(self._factory)

        twisted.internet.endpoints.serverFromString(
            twisted.internet.reactor,
            "tcp:%d" % self._port).listen(self._factory)
        LOGGER.info('Starting the DeckrServer listening on port %d',
                    self._port)
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

    def __init__(self, router, use_base64=False, json=False):
        self._router = router
        self._base64 = use_base64
        self._json = json

    def buildProtocol(self, _):
        """
        Build the protocol and pass along the router.
        """

        return deckr.network.connection.Connection(self._router, self._base64, self._json)
