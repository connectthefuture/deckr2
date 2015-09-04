#!/usr/bin/env python
"""
This a very lightweight script for spinning up multiple birthing pod workers.
"""

import argparse
import logging
import multiprocessing

import birthing_pod.worker


def start_worker(birthing_pod_server, deckr_server, worker_id):
    """
    Start a new worker.
    """

    logging.debug("Starting worker %d", worker_id)
    worker = birthing_pod.worker.BirthingPodWorker(birthing_pod_server,
                                                   deckr_server,
                                                   worker_id)
    worker.start()
    logging.debug("Worker %d has shutdown", worker_id)


def main():
    """
    Parse all the arguments then start workers in subprocesses.
    """

    parser = argparse.ArgumentParser("Run birthing pod workers")
    parser.add_argument("count", type=int, help="Number of workers to start")
    parser.add_argument("--birthing_pod_server", default="http://127.0.0.1:5000",
                        help="The birthing pod master server")
    parser.add_argument("--deckr_server", default="127.0.0.1:8080",
                        help="The deckr server to use for game play")
    args = parser.parse_args()

    workers = [multiprocessing.Process(target=start_worker,
                                       args=(args.birthing_pod_server,
                                             args.deckr_server,
                                             worker_id)) for worker_id in range(args.count)]
    [worker.start() for worker in workers]
    [worker.join() for worker in workers]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    main()
