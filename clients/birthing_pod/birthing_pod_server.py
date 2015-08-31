#!/usr/bin/env python
import json

import flask
import simple_client

app = flask.Flask(__name__)

class BirthingPod(object):
    """
    This is the overall manager class. It tracks decks that it's created, their current wins and
    loses, etc.
    """

    def __init__(self):
        self.next_playback_id = 0 # The next playback id
        self.client = simple_client.SimpleClient()

    def initialize(self):
        """
        Get everything set up properly.
        """

        self.client.initalize()

    def get_game(self):
        """
        Get the data for the next worker.
        """

        self.client.create()
        response = self.client.listen()

        playback_id = self.next_playback_id
        self.next_playback_id += 1

        return {
            'game_id': response.create_response.game_id,
            'deck': ["Forest"] * 10,
            'start': False,
            'playback_id': playback_id
        }


BIRTHING_POD = BirthingPod()


@app.route('/game')
def game():
    """
    Returns a game that should be joined, and a deck list to use.
    """

    return json.dumps(BIRTHING_POD.get_game())

@app.route('/stats', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        print flask.request.data
        return ''
    else:
        return "/stats only supports POST requests"

if __name__ == '__main__':
    BIRTHING_POD.initialize()
    app.run(debug=True)
