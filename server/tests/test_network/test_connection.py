"""
This module provides code around testing connections.
"""

from unittest import TestCase

from mock import MagicMock

from deckr.network.connection import Connection
from proto.client_message_pb2 import ClientMessage
from proto.server_response_pb2 import ServerResponse


class ConnectionTestCase(TestCase):
    """
    A simple unittest case around the connection.
    """

    def setUp(self):
        self.router = MagicMock()
        self.connection = Connection(self.router)
        # Create a message
        self.message = ClientMessage()
        self.message.message_type = ClientMessage.CREATE
        self.message.create_message.variant = 'standard'

    def test_recieve_message(self):
        """
        Make sure that when we recieve a message we decode it and pass it off to the router.
        """

        self.connection.recieve_message(self.message.SerializeToString())
        self.router.handle_message.assert_called_with(self.message, self.connection)

    def test_survives_malformed_input(self):
        """
        Make sure that if we can't decode a message we send an error instead of dying.
        """

        expected_response = ServerResponse()
        expected_response.response_type = ServerResponse.ERROR
        expected_response.error_response.message = "Could not parse message"

        self.connection.send_response = MagicMock()
        self.connection.recieve_message("foobar")
        self.connection.send_response.assert_called_with(expected_response)
