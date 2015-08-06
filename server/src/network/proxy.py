class Proxy(object):
    """
    This is basically a router. It takes in protobuff objects (decoded by
    the server), extracts useful information and passes them onto the game_master,
    games, other services. Each server has a single proxy associated with it.
    """

    def __init__(self):
        self._game_master

    def set_game_master(self, game_master):
        pass

    def handle_message(self, message, connection):
        """
        Entry point for all messages. This will call the appropriate subhandler.
        """

        pass

    def _handle_create(self, message, connection):
        pass

    def _handle_join(self, message, connection):
        pass
