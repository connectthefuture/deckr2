"""
This module provides code for deckr connections.
"""

from twisted.protocols.basic import LineReceiver


class Connection(LineReceiver):
    """
    This represents a single client connection. Each connection can be associated with at most
    1 game.
    """

    def __init__(self, router):
        #: Router The central router for deckr messages.
        self._router = router

    def send_response(self, response):
        """
        Response should be a protobuf. This will encode it and send it out over the wire.

        Arg:
            response (ServerResponse): A server response that should be sent over the wire.
        """

        pass

    def recieve_message(self, message):
        """
        Message should be a raw string that this connection has recieved. This function will
        decode it to a protobuf and route it appropriatly.

        Arg:
            message (str): The raw message that is recieved from the network. Will be decoded here
                and then pass off to the router.
        """

        pass

    # Everything below this is twisted. Everything above should be able to use any backend.
    def lineReceived(self, line):
        """
        Called whenever we recieve a raw message.
        """

        self.recieve_message(line)
