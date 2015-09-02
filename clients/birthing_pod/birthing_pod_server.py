#!/usr/bin/env python
"""
Run the very simple birthing pod server.
"""

import json
import random

import flask
import simple_client

APP = flask.Flask(__name__)

# Woo, global state....
BIRTHING_POD = BirthingPod()

@APP.route('/')
def index():
    """
    Get the index page.
    """

    user = {'nickname': 'Miguel'}  # fake user
    return flask.render_template('index.html',
                                 decks=BIRTHING_POD.decks)



@APP.route('/game')
def game_view():
    """
    Returns a game that should be joined, and a deck list to use.
    """

    return json.dumps(BIRTHING_POD.get_game())

@APP.route('/stats', methods=['GET', 'POST'])
def stats_view():
    """
    Record statistics after a game ends.
    """

    if flask.request.method == 'POST':
        BIRTHING_POD.update_stats(json.loads(flask.request.data))
        return ''
    else:
        return "/stats only supports POST requests"

if __name__ == '__main__':
    BIRTHING_POD.initialize()
    APP.run(debug=True)
