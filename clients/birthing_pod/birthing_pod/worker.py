""""
This module includes all of the code to support a birthing pod worker.
"""

import json
import logging
import time

import requests

import birthing_pod.client

LOGGER = logging.getLogger(__name__)

class BirthingPodJob(object):
    """
    A job is basically a deck that needs to be played.
    """

    def __init__(self, deckr_client):
        self._client = deckr_client

    def run(self):
        """
        Play the game.
        """

        pass

    def get_stats(self):
        """
        Get stats about this job upon completion.
        """

        pass


class BirthingPodWorker(object):

    def __init__(self, birthing_pod_sever, deckr_server, worker_id):
        self.birthing_pod_server = birthing_pod_sever
        self.deckr_server = deckr_server
        self.worker_id = worker_id

        self._client = None


    def start(self):
        """
        Start the worker. This will involve creating a deckr client and
        starting the main work loop.
        """

        LOGGER.debug("Worker %d: Initializing deckr_client", self.worker_id)
        self._client = birthing_pod.client.Client()
        self._client.initalize()
        self.main_loop()

    def main_loop(self):
        """
        The main work loop is pretty straightforwards.

        1) Request a job from the master
        2) Complete the job.
        3) Report back to the master.
        """

        while True:
            self.request()
            self.run()
            self.report()
            self.reset()

    def request(self):
        """
        Request a new job from the master.
        """

        # Pull data from the server
        self._current_job = BirthingPodJob(self._client)

    def run(self):
        """
        Run the current job.
        """

        self._current_job.run()

    def report(self):
        """
        Report the result of a job to the master.
        """

        stats = self._current_job.get_stats()
        # Send up to the master

    def reset(self):
        """
        Clear out the state for the next job.
        """

        self._current_job = None
    #
    #
    # def reset(self):
    #     self.player_id = None
    #     self.last_game_state = None
    #     self.deckr_client.leave()
    #     self.wait_for_response(2)
    #
    # def wait_for_response(self, response_type):
    #     while True:
    #         self.last_response = self.deckr_client.listen()
    #         if self.last_response is not None and self.last_response.response_type == response_type:
    #             return self.last_response
    #         elif self.last_response is not None:
    #             print "Unexpected response", self.last_response
    #
    #
    #
    # def wait_for_game_state(self):
    #     """
    #     Wait unti we've updated the game state.
    #     """
    #
    #     self.last_game_state = self.wait_for_response(4).game_state_response.game_state
    #
    #
    # def wait_for_priority_or_over(self):
    #     """
    #     Wait until we have priority, or the game is over.
    #     """
    #
    #     while True:
    #         if self.last_game_state and (self.is_over() or self.last_game_state.priority_player == self.player_id):
    #             return
    #         self.wait_for_game_state()
    #
    #
    # def is_over(self):
    #     """
    #     Check if we've lost in the last game_state.
    #     """
    #
    #     player_objs = [x for x in self.last_game_state.game_objects if x.game_object_type == 0]
    #     return len([x for x in player_objs if not x.player.lost]) <= 1 # The game if over if there's at most one player who hasn't lost.
    #
    # def has_lost(self):
    #     player_obj = [x for x in self.last_game_state.game_objects if x.game_id == self.player_id][0].player
    #     return player_obj.lost
    #
    # def run(self):
    #     """
    #     The main run loop is as follows:
    #
    #     1) Get a game from birthing pod
    #     2) Play game
    #     3) Report to birthing pod
    #     """
    #
    #     try:
    #         while(True):
    #             self.get_game()
    #             self.play_game()
    #             self.report()
    #             self.reset()
    #     except KeyboardInterrupt:
    #         return
    #
    # def get_game(self):
    #     """
    #     Get the game from the birthing pod server.
    #     """
    #
    #     response = requests.get(self.birthing_pod_base + '/game')
    #     data = response.json()
    #     LOGGER.debug("Got a new game %s", data)
    #
    #     self.playback_id = data['playback_id']
    #     self.deckr_client.join(data['game_id'], deck=data['deck'])
    #     self.player_id = self.wait_for_response(1).join_response.player_id
    #     print self.player_id
    #     if data['start']:
    #         time.sleep(0.2) # Make sure everyone has time to connect
    #         self.deckr_client.start()
    #     self.wait_for_game_state()
    #
    # def play_game(self):
    #     """
    #     Play a game.
    #     """
    #
    #     while not self.is_over():
    #         self.wait_for_priority_or_over()
    #         if not self.is_over():
    #             self.deckr_client.pass_priority()
    #             self.wait_for_game_state() # Make sure we don't spam, so wait until we have a new game state.
    #
    # def report(self):
    #     """
    #     Report my stats.
    #     """
    #
    #     payload = {
    #         'worker_id': self.worker_id,
    #         'playback_id': self.playback_id,
    #         'lost': self.has_lost()
    #     }
    #     response = requests.post(self.birthing_pod_base + '/stats', data=json.dumps(payload))
