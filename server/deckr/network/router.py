"""
This module provides code for the Router.
"""

import logging

import deckr.game.action_validator
import proto.client_message_pb2
import proto.server_response_pb2

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
            message (proto.client_message_pb2.ClientMessage): The protobuf object (already parsed)
            connection (Connection): The connection that sent this message.
        """

        message_type = message.message_type
        if message_type == proto.client_message_pb2.ClientMessage.CREATE:
            self._handle_create(message, connection)
        elif message_type == proto.client_message_pb2.ClientMessage.JOIN:
            self._handle_join(message, connection)
        elif message_type == proto.client_message_pb2.ClientMessage.LEAVE:
            self._handle_leave(connection)
        elif message_type == proto.client_message_pb2.ClientMessage.ACTION:
            try:
                self._handle_action(message.action_message, connection)
            except deckr.game.action_validator.InvalidActionException as exc:
                connection.send_error(exc.message)
                return
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

    def _handle_create(self, message, connection):  # pylint: disable=unused-argument
        """
        Handle a create message. This will create a game through the game master and then return
        a create response.
        """

        game_id = self._game_master.create()
        game = self._game_master.get_game(game_id)
        self.create_room(game_id, game)

        response = proto.server_response_pb2.ServerResponse()
        response.response_type = proto.server_response_pb2.ServerResponse.CREATE
        response.create_response.game_id = game_id
        connection.send_response(response)

    def _handle_join(self, message, connection):
        """
        Handle a join message.
        """

        game_id = message.join_message.game_id
        game = self._game_master.get_game(game_id)

        player_config = message.join_message.player_config
        connection.player = game.player_manager.create_player(
            player_config.deck)
        self.add_to_room(connection, game_id)

        response = proto.server_response_pb2.ServerResponse()
        response.response_type = proto.server_response_pb2.ServerResponse.JOIN
        response.join_response.player_id = connection.player.game_id
        connection.send_response(response)

    def _handle_leave(self, connection):  # pylint: disable=no-self-use
        """
        Handle a message that the user wants to leave the current game.
        """

        response = proto.server_response_pb2.ServerResponse()
        response.response_type = proto.server_response_pb2.ServerResponse.LEAVE
        connection.send_response(response)

    def _handle_action(self, message, connection):
        """
        Handle an action message. Mainly this just figures out where to dispatch the call.
        It will also swap out game ids for the actual game objects.
        """

        game = self._game_rooms[connection.room_id][0]
        player = connection.player

        assert game is not None and player is not None

        if message.action_type == proto.client_message_pb2.ActionMessage.START:
            game.start()
        elif message.action_type == proto.client_message_pb2.ActionMessage.PASS_PRIORITY:
            player.pass_priority()
        elif message.action_type == proto.client_message_pb2.ActionMessage.PLAY:
            card = game.registry.lookup(message.play.card)
            player.play_card(card)
        elif message.action_type == proto.client_message_pb2.ActionMessage.ACTIVATE:
            card = game.registry.lookup(message.activate_ability.card)
            player.activate_ability(card, message.activate_ability.index)
        elif message.action_type == proto.client_message_pb2.ActionMessage.DECLARE_ATTACKERS:
            attackers = {
                game.registry.lookup(x.attacker): game.registry.lookup(
                    x.target)
                for x in message.declare_attackers.attackers
            }
            player.declare_attackers(attackers)
        elif message.action_type == proto.client_message_pb2.ActionMessage.DECLARE_BLOCKERS:
            blockers = {
                game.registry.lookup(x.blocker): game.registry.lookup(
                    x.blocking)
                for x in message.declare_blockers.blockers
            }
            player.declare_blockers(blockers)
        else:  # Catch all bail out case.
            connection.send_error("Invalid action type {}".format(
                message.action_type))
            return

        # Assuming the action was completed, we broadcast the current state
        # to all clients.
        response = proto.server_response_pb2.ServerResponse()
        response.response_type = proto.server_response_pb2.ServerResponse.GAME_STATE
        game.update_proto(response.game_state_response.game_state)
        for conn in self.get_room_connections(connection.room_id):
            conn.send_response(response)
