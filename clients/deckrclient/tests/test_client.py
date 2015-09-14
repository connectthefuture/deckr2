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

        def mock_listen():
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

    def test_raise_errors(self):
        """
        Make sure if the raise_errors flag is set, then we raise any error response
        as an exception.
        """

        error_response = proto.server_response_pb2.ServerResponse()
        error_response.response_type = proto.server_response_pb2.ServerResponse.ERROR
        self.client._raise_errors = True
        self.client._listen = mock.MagicMock()
        self.client._listen.return_value = error_response
        self.assertRaises(ValueError, self.client.listen)

    def test_join(self):
        """
        Make sure we can send a join message.
        """

        expected_message = proto.client_message_pb2.ClientMessage()
        expected_message.message_type = proto.client_message_pb2.ClientMessage.JOIN
        expected_message.join_message.game_id = 0
        expected_message.join_message.client_type = proto.client_message_pb2.JoinMessage.PLAYER
        self.client._send_message = mock.MagicMock()
        self.client.join(game_id=0)
        self.client._send_message.assert_called_with(expected_message)

    def test_start(self):
        """
        Make sure we can start a game.
        """

        expected_message = proto.client_message_pb2.ClientMessage()
        expected_message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        expected_message.action_message.action_type = proto.client_message_pb2.ActionMessage.START
        self.client._send_message = mock.MagicMock()
        self.client.start()
        self.client._send_message.assert_called_with(expected_message)

    def test_pass_priority(self):
        """
        Make sure we can pass priority.
        """

        expected_message = proto.client_message_pb2.ClientMessage()
        expected_message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        expected_message.action_message.action_type = proto.client_message_pb2.ActionMessage.PASS_PRIORITY
        self.client._send_message = mock.MagicMock()
        self.client.pass_priority()
        self.client._send_message.assert_called_with(expected_message)


    def test_join_response(self):
        """
        Make sure that we properly parse a join response.
        """

        response = proto.server_response_pb2.ServerResponse()
        response.response_type = proto.server_response_pb2.ServerResponse.JOIN
        response.join_response.player_id = 1
        self.client._listen = mock.MagicMock()
        self.client._listen.return_value = response
        self.client.listen()

        self.assertEqual(self.client.player_id, 1)

    def test_play(self):
        """
        Make sure we can play a card.
        """

        card_proto = proto.game_pb2.Card()
        card_proto.game_id = 1
        card_proto.name = "Grizzly Bears"
        mock_card = deckrclient.client.Card(card_proto)
        expected_message = proto.client_message_pb2.ClientMessage()
        expected_message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        expected_message.action_message.action_type = proto.client_message_pb2.ActionMessage.PLAY
        expected_message.action_message.play.card = 1

        self.client._send_message = mock.MagicMock()
        self.client.play(1)
        self.client._send_message.assert_called_with(expected_message)
        self.client.play(mock_card)
        self.client._send_message.assert_called_with(expected_message)

    def test_game_state_response(self):
        """
        Make sure we update the game state when we get a gamestate response.
        """

        response = proto.server_response_pb2.ServerResponse()
        response.response_type = proto.server_response_pb2.ServerResponse.GAME_STATE
        game_state = response.game_state_response.game_state
        player = game_state.players.add()
        player.game_id = 1
        game_state.active_player = 1
        game_state.priority_player = 1
        self.client._listen = mock.MagicMock()
        self.client._listen.return_value = response
        self.client.listen()

        self.assertIsNotNone(self.client.game_state)
        self.assertIsInstance(self.client.game_state.priority_player, deckrclient.client.Player)

class GameStateTestCase(unittest.TestCase):
    """
    Test the client game state.
    """

    def test_card(self):
        """
        Make sure we can load a card from a card protobuf.
        """

        card_proto = proto.game_pb2.Card()
        card_proto.game_id = 0
        card_proto.name = "Grizzly Bears"
        card = deckrclient.client.Card(card_proto)
        self.assertEqual(card.game_id, 0)
        self.assertEqual(card.name, "Grizzly Bears")

    def test_player(self):
        """
        Make sure we can load a player from a protobuf.
        """

        player_proto = proto.game_pb2.Player()
        player_proto.game_id = 0
        player_proto.lost = False
        player_proto.life = 20
        player_proto.hand.cards.add()
        player_proto.library.cards.add()
        player_proto.graveyard.cards.add()
        player = deckrclient.client.Player(player_proto)
        self.assertEqual(player.game_id, 0)
        self.assertEqual(player.life, 20)
        self.assertEqual(player.lost, False)
        self.assertEqual(len(player.library), 1)
        self.assertEqual(len(player.graveyard), 1)
        self.assertEqual(len(player.hand), 1)

    def test_game_state(self):
        """
        Make sure we can properly parse the entire game state.
        """

        game_state_proto = proto.game_pb2.GameState()
        game_state_proto.current_step = 'upkeep'
        game_state_proto.current_phase = 'beginning'
        game_state_proto.priority_player = 1
        game_state_proto.active_player = 1
        player = game_state_proto.players.add()
        player.game_id = 1

        game_state = deckrclient.client.GameState(game_state_proto)
        self.assertEqual(game_state.step, 'upkeep')
        self.assertEqual(game_state.phase, 'beginning')
        self.assertEqual(len(game_state.players), 1)
        player1 = game_state.players[0]
        self.assertEqual(game_state.active_player, player1)
        self.assertEqual(game_state.priority_player, player1)
