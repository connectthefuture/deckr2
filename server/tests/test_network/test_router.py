"""
This module tests the router to make sure it can properly route requests.
"""

from unittest import TestCase

from mock import MagicMock

from deckr.network.router import Router
from proto.client_message_pb2 import ClientMessage, JoinMessage
from proto.server_response_pb2 import ServerResponse


class RouterTestCase(TestCase):
    """
    Test the core router functionality.
    """

    def setUp(self):
        self.router = Router()
        self.game_master = MagicMock()
        self.connection = MagicMock()
        self.game = MagicMock()
        self.router.set_game_master(self.game_master)

    def test_create(self):
        """
        A create message should call create on the game master and then return a create response.
        """

        self.game_master.create.return_value = 'foo'

        message = ClientMessage()
        message.message_type = ClientMessage.CREATE

        expected_response = ServerResponse()
        expected_response.response_type = ServerResponse.CREATE
        expected_response.create_response.game_id = 'foo'

        self.router.handle_message(message, self.connection)
        self.game_master.create.assert_called_with()
        self.connection.send_response.assert_called_with(expected_response)

    def test_join(self):
        """
        A join message should lookup the game and then join the game room. It should return a
        join response.
        """

        self.game_master.get_game.return_value = self.game

        message = ClientMessage()
        message.message_type = ClientMessage.JOIN
        message.join_message.client_type = JoinMessage.PLAYER
        message.join_message.game_id = 'foo'

        expected_response = ServerResponse()
        expected_response.response_type = ServerResponse.JOIN

        self.router.handle_message(message, self.connection)
        self.game_master.get_game.assert_called_with('foo')
        self.game.create_player.assert_called_with()
        self.connection.send_response.assert_called_with(expected_response)

    def test_leave(self):
        """
        Make sure that we can properly handle a leave message.
        """

        message = ClientMessage()
        message.message_type = ClientMessage.LEAVE

        expected_response = ServerResponse()
        expected_response.response_type = ServerResponse.LEAVE

        self.router.handle_message(message, self.connection)
        self.connection.send_response.assert_called_with(expected_response)
