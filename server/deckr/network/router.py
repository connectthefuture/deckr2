"""
This module provides code for the Router.
"""

import logging

from proto.client_message_pb2 import ClientMessage
from proto.server_response_pb2 import ServerResponse

LOGGER = logging.getLogger(__name__)


class Router(object):
    """
    This is basically a router. It takes in protobuff objects (decoded by
    the server), extracts useful information and passes them onto the game_master,
    games, other services. Each server has a single proxy associated with it.
    """

    def __init__(self):
        #: GameMaster The game master for this router.
        self._game_master = None
        #: dict(string:[Connection]) holds all of the game rooms.
        self._game_rooms = {}

    def set_game_master(self, game_master):
        """
        Called to set the game master for the Router.
        """

        self._game_master = game_master

    def handle_message(self, message, connection):
        """
        Entry point for all messages. This will call the appropriate subhandler and send
        any responses that are generated.

        Args:
            message (ClientMessage): The protobuf object (already parsed)
            connection (Connection): The connection that sent this message.
        """

        message_type = message.message_type
        if message_type == ClientMessage.CREATE:
            self._handle_create(message, connection)
        elif message_type == ClientMessage.JOIN:
            self._handle_join(message, connection)
        elif message_type == ClientMessage.LEAVE:
            self._handle_leave(message, connection)
        else:
            connection.send_error("Not implemented yet")

    def create_room(self, room_id, game):
        """
        Create a new room with the given id and game.
        """

        self._game_rooms[room_id] = (game, [])

    def add_to_room(self, connection, room_id):
        """
        Adds the connection to the given room.
        """

        self._game_rooms[room_id][1].append(connection)
        connection.room_id = room_id

    def get_room_connections(self, room_id):
        """
        Get a list of connections in a room.
        """

        return self._game_rooms[room_id][1]

    def _handle_create(self, message, connection):
        """
        Handle a create message. This will create a game through the game master and then return
        a create response.
        """

        game_id = self._game_master.create()
        game = self._game_master.get_game(game_id)
        self.create_room(game_id, game)

        response = ServerResponse()
        response.response_type = ServerResponse.CREATE
        response.create_response.game_id = game_id
        connection.send_response(response)

    def _handle_join(self, message, connection):
        """
        Handle a join message.
        """

        game_id = message.join_message.game_id
        game = self._game_master.get_game(game_id)
        player = game.create_player()
        self.add_to_room(connection, game_id)

        response = ServerResponse()
        response.response_type = ServerResponse.JOIN
        connection.send_response(response)

    def _handle_leave(self, message, connection):
        """
        Handle a message that the user wants to leave the current game.
        """

        response = ServerResponse()
        response.response_type = ServerResponse.LEAVE
        connection.send_response(response)
