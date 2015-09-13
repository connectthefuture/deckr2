"""
Run unittests for the deckr client.
"""

import unittest

import deckrclient.client
import mock

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8000


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
