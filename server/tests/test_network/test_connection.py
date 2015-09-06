"""
This module provides code around testing connections.
"""

import unittest

import base64
import deckr.network.connection
import mock
import proto.client_message_pb2
import proto.server_response_pb2


class ConnectionTestCase(unittest.TestCase):
    """
    A simple unittest case around the connection.
    """

    def setUp(self):
        self.router = mock.MagicMock()
        self.connection = deckr.network.connection.Connection(self.router)
        # Create a message
        self.message = proto.client_message_pb2.ClientMessage()
        self.message.message_type = proto.client_message_pb2.ClientMessage.CREATE
        self.message.create_message.variant = 'standard'

    def test_recieve_message(self):
        """
        Make sure that when we recieve a message we decode it and pass it off to the router.
        """

        self.connection.recieve_message(self.message.SerializeToString())
        self.router.handle_message.assert_called_with(
            self.message, self.connection)

    def test_base64_support(self):
        """
        Make sure that when the base64 flag is set to true, we can encode and decode messages.
        """

        self.connection._base64 = True

        encoded_message = base64.b64encode(self.message.SerializeToString())
        self.connection.recieve_message(encoded_message)
        self.router.handle_message.assert_called_with(
            self.message, self.connection)

        self.connection._base64 = False


    def test_survives_malformed_input(self):
        """
        Make sure that if we can't decode a message we send an error instead of dying.
        """

        expected_response = proto.server_response_pb2.ServerResponse()
        expected_response.response_type = proto.server_response_pb2.ServerResponse.ERROR
        expected_response.error_response.message = "Could not parse message"

        self.connection.send_response = mock.MagicMock()
        self.connection.recieve_message("foobar")
        self.connection.send_response.assert_called_with(expected_response)

    def test_quit(self):
        """
        If we get a quit message we should lose connection.
        """

        self.message.message_type = proto.client_message_pb2.ClientMessage.QUIT
        self.connection.transport = mock.MagicMock()
        self.connection.recieve_message(self.message.SerializeToString())
        self.connection.transport.loseConnection.assert_called_with()

    def test_survives_exception(self):
        """
        If we encounter an exception processing a message, we should catch it and let the
        end user know.
        """

        self.router.handle_message.side_effect = Exception(
            "Never should happen")
        self.connection.send_error = mock.MagicMock()
        self.connection.recieve_message(self.message.SerializeToString())
        self.connection.send_error.called_once()

if __name__ == "__main__":
    unittest.main()
