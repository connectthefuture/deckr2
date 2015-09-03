#!/usr/bin/env python
"""
Run flask ontop of the birthing pod master.
"""

import json
import random

import flask

import birthing_pod.master

APP = flask.Flask(__name__)

# Woo, global state....
BIRTHING_POD = birthing_pod.master.BirthingPodMaster()

@APP.route('/')
def index():
    """
    Get the index page.
    """

    return flask.render_template('index.html')

@APP.route('/game')
def game_view():
    """
    Returns a game that should be joined, and a deck list to use.
    """

    return json.dumps(BIRTHING_POD.get_job())

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
