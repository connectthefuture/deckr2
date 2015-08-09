"""
This module provides code for the Router.
"""


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

        pass

    def handle_message(self, message, connection):
        """
        Entry point for all messages. This will call the appropriate subhandler and send
        any responses that are generated.

        Args:
            message (ClientMessage): The protobuf object (already parsed)
            connection (Connection): The connection that sent this message.
        """

        print("Got message ", message, " from ", connection)
