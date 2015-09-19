"""
This offers simple code for a birthing pod player.
"""

import deckrclient.client


class BirthingPodPlayer(object):

    def __init__(self, ip, port):
        self.client = deckrclient.client.DeckrClient(ip, port)

    def initialize(self):
        """
        Initialize a player.
        """

        self.client.initialize()

    def shutdown(self):
        """
        Cleanly shutdwon a player.
        """
        self.client.shutdown()

    def create_and_join(self, deck):
        """
        Create a game, and join it with the specified deck.
        """

        self.client.create()
        create_response = self.client.listen()
        game_id = create_response.create_response.game_id
        self.client.join(game_id, deck=deck)
        self.client.listen()
        return game_id

    def join_and_start(self, game_id, deck):
        """
        Join a game and start it.
        """

        self.client.join(game_id, deck=deck)
        self.client.listen()
        self.client.start()

    def run_event_loop(self):
        """
        Run my main event loop.
        """

        # We start out with no game state, but the game should have started so
        # we wait for our first game state message.
        self.client.listen()
        while not self.client.game_state.is_over():
            if (self.client.game_state.player ==
                self.client.game_state.priority_player):
                self.client.pass_priority()
            self.client.listen()
