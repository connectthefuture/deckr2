"""
This module contains the deckr client.
"""

import socket
import time


class DeckrClient(object):
    """
    A client for interacting with a deckr server.
    """

    def __init__(self, ip, port, backoff=0.1):
        self._ip = ip
        self._port = port
        self._socket = None
        self._backoff = backoff # How long to wait between retries

    def initialize(self, max_retries=3):
        """
        Create a connection with the server.
        """

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        attempt_number = 0
        while attempt_number < max_retries:
            try:
                self._socket.connect((self._ip, self._port))
                break
            except IOError as ex:
                attempt_number += 1
                if attempt_number == max_retries:
                    raise ex
                time.sleep(self._backoff)

    def shutdown(self):
        """
        Cleanly shutdown a client.
        """

        self._socket.close()
