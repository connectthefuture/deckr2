"""
This module provides code around testing connections.
"""

import base64
import unittest

import mock

import deckr.network.connection
import deckr.network.json_proxy
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
        self.json_message = deckr.network.json_proxy.encode_to_json(self.message)

    def test_recieve_message(self):
        """
        Make sure that when we recieve a message we decode it and pass it off to the router.
        """

        self.connection.recieve_message(self.message.SerializeToString())
        self.router.handle_message.assert_called_with(
            self.message, self.connection)
        # Check recieve json
        self.connection._json = True
        self.connection.recieve_message(self.json_message)
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

    def test_send_response(self):
        """
        We should serialize a response properly.
        """

        response = proto.server_response_pb2.ServerResponse()
        response.response_type = proto.server_response_pb2.ServerResponse.ERROR
        response.error_response.message = "Something went wrong."
        json_response = '{"response_type": 3, "error_response": {"message": "Something went wrong."}}'
        base64_json_response = "eyJyZXNwb25zZV90eXBlIjogMywgImVycm9yX3Jlc3BvbnNlIjogeyJtZXNzYWdlIjogIlNvbWV0aGluZyB3ZW50IHdyb25nLiJ9fQ=="
        self.connection.sendLine = mock.MagicMock()
        self.connection.send_response(response)
        # It should have just sent out the serialized response.
        self.connection.sendLine.assert_called_with(response.SerializeToString())
        # It should do JSON encoding
        self.connection._json = True
        self.connection.send_response(response)
        self.connection.sendLine.assert_called_with(json_response)
        # It should do base 64 encoding
        self.connection._base64 = True
        self.connection.send_response(response)
        self.connection.sendLine.assert_called_with(base64_json_response)

    def test_twisted_specific(self):
        """
        Test the twisted specific functions.
        """

        self.connection.recieve_message = mock.MagicMock()
        self.connection.connectionMade()
        self.connection.lineReceived('foobar')
        self.connection.recieve_message.assert_called_with('foobar')

if __name__ == "__main__":
    unittest.main()
