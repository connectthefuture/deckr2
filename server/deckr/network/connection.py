"""
This module provides code for deckr connections.
"""

import logging
import traceback

import google.protobuf.message
import proto.client_message_pb2
import proto.server_response_pb2
import twisted.protocols.basic

LOGGER = logging.getLogger(__name__)


class Connection(twisted.protocols.basic.LineReceiver):
    """
    This represents a single client connection. Each connection can be associated with at most
    1 game.
    """

    def __init__(self, router):
        # What room this connection is part of
        self.room_id = None
        # The player assocaited with this connection, if any
        self.player = None
        #: Router The central router for deckr messages.
        self._router = router

    def send_response(self, response):
        """
        Response should be a protobuf. This will encode it and send it out over the wire.

        Arg:
            response (ServerResponse): A server response that should be sent over the wire.
        """

        self.sendLine(response.SerializeToString())

    def recieve_message(self, message):
        """
        Message should be a raw string that this connection has recieved. This function will
        decode it to a protobuf and route it appropriatly.

        Arg:
            message (str): The raw message that is recieved from the network. Will be decoded here
                and then pass off to the router.
        """

        decoded_message = proto.client_message_pb2.ClientMessage()
        try:
            decoded_message.ParseFromString(message)
        except google.protobuf.message.DecodeError:
            self.send_error("Could not parse message")
            return

        LOGGER.debug("Got a message %s from %s", decoded_message, self)
        if decoded_message.message_type == proto.client_message_pb2.ClientMessage.QUIT:
            self.transport.loseConnection()  # twisted specific
            return

        # We use a bare try except clause here because we don't want any lower level exception
        # to kill the connection. Hopefully we don't hit this very often.
        try:
            self._router.handle_message(decoded_message, self)
        except Exception:  # pylint: disable=broad-except
            LOGGER.exception("Encountered unexpected exception")
            # Potentially hide this behind a debug flag.
            self.send_error(traceback.format_exc())

    def send_error(self, message):
        """
        Send an error.
        """

        LOGGER.warn("Sending error message %s", message)
        response = proto.server_response_pb2.ServerResponse()
        response.response_type = proto.server_response_pb2.ServerResponse.ERROR
        response.error_response.message = message
        self.send_response(response)

    # Everything below this is twisted. Everything above should be able to use
    # any backend.

    def connectionMade(self):
        """
        We made a connection. Log it.
        """

        LOGGER.debug("Got a connection")

    def lineReceived(self, line):
        """
        Called whenever we recieve a raw message.
        """

        self.recieve_message(line)
