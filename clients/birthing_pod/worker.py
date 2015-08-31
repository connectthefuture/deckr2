#!/usr/bin/env python
"""
Includes a simple birthing pod worker.
"""

import json
import logging
import time

import requests

import simple_client

LOGGER = logging.getLogger(__name__)

class BirthingPodWorker(object):

    def __init__(self, birthing_pod_base, worker_id, deckr_client):
        self.birthing_pod_base = birthing_pod_base
        self.worker_id = worker_id
        self.playback_id = None
        self.deckr_client = deckr_client
        self.last_game_state = None
        self.player_id = None

    def has_lost(self):
        """
        Check if we've lost in the last game_state.
        """

        player_obj = [x for x in self.last_game_state.game_objects if x.game_id == self.player_id][0].player
        return player_obj.lost

    def run(self):
        """
        The main run loop is as follows:

        1) Get a game from birthing pod
        2) Play game
        3) Report to birthing pod
        """

        try:
            while(True):
                self.get_game()
                self.play_game()
                self.report()
        except KeyboardInterrupt:
            return

    def get_game(self):
        """
        Get the game from the birthing pod server.
        """

        response = requests.get(self.birthing_pod_base + '/game')
        data = response.json()
        LOGGER.debug("Got a new game %s", data)

        self.playback_id = data['playback_id']
        self.deckr_client.join(data['game_id'], deck=data['deck'])
        self.player_id = self.deckr_client.listen().join_response.player_id
        self.deckr_client.start()
        self.last_game_state = self.deckr_client.listen().game_state_response.game_state

    def play_game(self):
        """
        Play a game.
        """

        while not self.has_lost():
            self.deckr_client.pass_priority()
            self.last_game_state = self.deckr_client.listen().game_state_response.game_state

    def report(self):
        """
        Report my stats.
        """

        payload = {
            'worker_id': self.worker_id,
            'playback_id': self.playback_id
        }
        response = requests.post(self.birthing_pod_base + '/stats', data=json.dumps(payload))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    deckr_client = simple_client.SimpleClient()
    deckr_client.initalize()
    worker = BirthingPodWorker("http://127.0.0.1:5000", 1, deckr_client)
    worker.run()
    deckr_client.shutdown()
    LOGGER.info('Shut it down')
