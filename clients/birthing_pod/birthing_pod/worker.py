""""
This module includes all of the code to support a birthing pod worker.
"""

import json
import logging
import time

import requests

import birthing_pod.client

LOGGER = logging.getLogger(__name__)

class GameState(object):
    """
    A very simple representation of the game state.
    """

    def __init__(self, game_state_proto):
        self.players = {x.game_id: x.player for x in game_state_proto.game_objects
                        if x.game_object_type == 0}
        self.priority_player = game_state_proto.priority_player
        self

class BirthingPodJob(object):
    """
    A job is basically a deck that needs to be played.
    """

    def __init__(self, deckr_client, job_id, game_id, deck, start):
        self._client = deckr_client
        self._job_id = job_id
        self._game_id = game_id
        self._player_id = None
        self._deck = deck
        self._game_state = None
        self._start = start

    def run(self):
        """
        Play the game.
        """

        # Start by joining the game
        response = self._client.send_and_wait(
            birthing_pod.client.message_join(self._game_id, self._deck))
        self._player_id = response.join_response.player_id

        # Start the game
        if self._start:
            time.sleep(0.1) # Sometimes people haven't all connected
            self._client.send_message(birthing_pod.client.message_start())
        self.wait_for_game_state()

        while not self.is_over():
            self.wait_for_priority()
            # Right now the server doesn't do well with events after the game is over.
            if self.is_over():
                return
            self._client.send_message(birthing_pod.client.message_pass_priority())
            self.wait_for_game_state()

    def get_stats(self):
        """
        Get stats about this job upon completion.
        """

        return {
            'job_id': self._job_id,
            'won': not self.lost()
        }

    ##############################
    # Simple actions for waiting #
    ##############################

    def lost(self):
        """
        Check if this player has lost in the last game state.
        """

        return self._game_state.players[self._player_id].lost

    def is_over(self):
        """
        Check the current game state to see if the game is over (i.e. there's
        only one player who hasn't lost).
        """

        return len([x for x in self._game_state.players.values() if not x.lost]) <= 1


    def wait_for_game_state(self):
        """
        Wait until we update the game state.
        """

        while True:
            response = self._client.get_response()
            if response.response_type == 4:
                self._game_state = GameState(response.game_state_response.game_state)
                return
            else:
                print "Encounterd unexpected message", response

    def wait_for_priority(self):
        """
        Wait until I have priority.
        """

        while (self._game_state is None or
               self._game_state.priority_player != self._player_id):
            self.wait_for_game_state()



class BirthingPodWorker(object):
    """
    This class represents a simple birthing pod worker. It will get jobs,
    and play games in an infinite loop.
    """

    def __init__(self, birthing_pod_sever, deckr_server, worker_id):
        self.birthing_pod_server = birthing_pod_sever
        self.deckr_server = deckr_server
        self.worker_id = worker_id

        self._client = None
        self._current_job = None
        self._won = False # Did I win my current job?


    def start(self):
        """
        Start the worker. This will involve creating a deckr client and
        starting the main work loop.
        """

        LOGGER.debug("Worker %d: Initializing deckr_client", self.worker_id)
        self._client = birthing_pod.client.Client()
        self._client.initialize()
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

        job_data = requests.get(self.birthing_pod_server + '/game').json()
        self._current_job = BirthingPodJob(self._client,
                                           job_data['job_id'],
                                           job_data['game_id'],
                                           job_data['deck'],
                                           job_data['start'])

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
        requests.post(self.birthing_pod_server + '/stats',
                      data=json.dumps(stats))

    def reset(self):
        """
        Clear out the state for the next job.
        """

        self._current_job = None
        self._client.send_and_wait(birthing_pod.client.message_leave())
        self._client.clear_buffer()
