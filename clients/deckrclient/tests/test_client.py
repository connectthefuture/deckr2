"""
Run unittests for the deckr client.
"""

import unittest

import deckrclient.client
import mock
import proto.client_message_pb2
import proto.server_response_pb2

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8000

CALL_COUNT = 0

# pylint: disable=protected-access

class DeckrClientTestCase(unittest.TestCase):
    """
    Unittests for the actual client.
    """

    def setUp(self):
        self.client = deckrclient.client.DeckrClient(ip=SERVER_IP,
                                                     port=SERVER_PORT,
                                                     backoff=0)

    @mock.patch('socket.socket')
    def test_initialize(self, socket_mock):
        """
        Make sure that we can properly connect to the server.
        """

        mock_connection = mock.MagicMock()
        socket_mock.return_value = mock_connection

        self.client.initialize()

        mock_connection.connect.assert_called_with((SERVER_IP, SERVER_PORT))

    @mock.patch('threading.Thread')
    @mock.patch('socket.socket')
    def test_initialize_async(self, socket_mock, thread_mock):
        """
        Make sure that we can initialize async.
        """

        self.client._sync = False
        mock_connection = mock.MagicMock()
        socket_mock.return_value = mock_connection
        self.client.initialize()
        mock_connection.connect.assert_called_with((SERVER_IP, SERVER_PORT))
        # Make sure we spin up a listener thread
        self.assertEqual(thread_mock.call_count, 1)


    @mock.patch('socket.socket')
    def test_retry(self, socket_mock):
        """
        Make sure that we can retry before failing.
        """

        mock_connection = mock.MagicMock()
        mock_connection.connect.side_effect = IOError
        socket_mock.return_value = mock_connection

        self.assertRaises(IOError, self.client.initialize, max_retries=3)

        self.assertEqual(mock_connection.connect.call_count, 3)

    def test_shutdown(self):
        """
        Make sure we cleanly shutdown the sockets.
        """

        self.client._socket = mock.MagicMock()
        self.client.shutdown()
        self.client._socket.close.assert_called_with()

    def test_send_message(self):
        """
        Make sure that we can send a mesasage over the socket.
        """

        message = mock.MagicMock()
        message.SerializeToString.return_value = 'foobar'
        self.client._socket = mock.MagicMock()
        self.client._send_message(message)
        self.client._socket.send.assert_called_with('foobar\r\n')

    def test_listen_raw(self):
        """
        Make sure that we can listen for a raw message
        """

        self.client._socket = mock.MagicMock()
        self.client._socket.recv.return_value = 'foobar\r\n'
        self.assertEqual(self.client._listen_raw(), 'foobar')

    def test_listen_raw_multiple(self):
        """
        Make sure we can properly handle multiple messages.
        """

        self.client._socket = mock.MagicMock()
        self.client._socket.recv.return_value = 'foobar\r\nfoobaz\r\n'
        self.assertEqual(self.client._listen_raw(), 'foobar')
        self.assertEqual(self.client._listen_raw(), 'foobaz')
        self.assertEqual(self.client._socket.recv.call_count, 1)

    def test_listen_internal(self):
        """
        Make sure we parse a message into a protobuf.
        """

        self.client._listen_raw = mock.MagicMock() # Don't actually need a message.
        self.assertIsInstance(self.client._listen(),
                              proto.server_response_pb2.ServerResponse)
        self.client._listen_raw.assert_called_with()

    def test_listen(self):
        """
        Make sure the external facing listen function gets a message and then
        dispatches properly.
        """

        response = mock.MagicMock()
        self.client._listen = mock.MagicMock()
        self.client._listen.return_value = response
        self.assertEqual(response, self.client.listen())

    def test_create(self):
        """
        Make sure we can create a new game.
        """

        expected_message = proto.client_message_pb2.ClientMessage()
        expected_message.message_type = proto.client_message_pb2.ClientMessage.CREATE
        self.client._send_message = mock.MagicMock()
        self.client.create()
        self.client._send_message.assert_called_with(expected_message)

    def test_listener_thread_worker(self):
        """
        Make sure we can listen and then call a callback.
        """

        def mock_listen(): # TODO: Can I do this better?
            """Mock listener."""
            global CALL_COUNT
            if CALL_COUNT == 0:
                CALL_COUNT += 1
                return "foobar"
            return None

        callback = mock.MagicMock()
        self.client._callback = callback
        self.client.listen = mock_listen

        self.client._listener_thread_worker()
        callback.assert_called_with("foobar")
