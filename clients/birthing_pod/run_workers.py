#!/usr/bin/env python
"""
This a very lightweight script for spinning up multiple birthing pod workers.
"""

import argparse
import json
import logging
import multiprocessing
import threading
import time

import requests

import birthing_pod.player


def get_game(birthing_pod_server):
    """
    Get a new match.
    """

    return requests.get(birthing_pod_server + '/game').json()

def worker_process(deckr_server_ip, deckr_server_port, birthing_pod_server):
    """
    The entry point for a worker process. It will spin up two processes for each
    of the players, and then go into a loop.
    """

    # Create players
    player1 = birthing_pod.player.BirthingPodPlayer(deckr_server_ip, deckr_server_port)
    player2 = birthing_pod.player.BirthingPodPlayer(deckr_server_ip, deckr_server_port)

    player1.initialize()
    player2.initialize()

    while True:
        # Get a game from the master
        data = get_game(birthing_pod_server)
        if not data:
            time.sleep(0.1)
            continue
        # Create and play the game
        game_id = player1.create_and_join(data['deck1'])
        player2.join_and_start(game_id, data['deck2'])
        # At this point the game is started so we just launch both players into
        # their event loop.
        player1_thread = threading.Thread(target=player1.run_event_loop)
        player2_thread = threading.Thread(target=player2.run_event_loop)
        player1_thread.start()
        player2_thread.start()

        player1_thread.join()
        player2_thread.join()
        # Check the last game state
        if player1.client.game_state.player.lost:
            status = 2
        else:
            status = 1
        requests.post(birthing_pod_server + '/stats',
                      data=json.dumps({'job_id': data['job_id'],
                                       'won': status}))

    player1.shutdown()
    player2.shutdown()


def main():
    """
    Parse all the arguments then start workers in subprocesses.
    """

    parser = argparse.ArgumentParser("Run birthing pod workers")
    parser.add_argument("count", type=int, help="Number of workers to start")
    parser.add_argument("--birthing_pod_server", default="http://127.0.0.1:5000",
                        help="The birthing pod master server")
    parser.add_argument("--deckr_server_ip", default="127.0.0.1",
                        help="The deckr server to use for game play")
    parser.add_argument("--deckr_server_port", default=8080, type=int,
                        help="The deckr server to use for game play")
    args = parser.parse_args()

    workers = [
        multiprocessing.Process(target=worker_process,
                                args=(args.deckr_server_ip,
                                      args.deckr_server_port,
                                      args.birthing_pod_server))
        for _ in range(args.count)
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    main()
