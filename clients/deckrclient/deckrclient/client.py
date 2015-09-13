"""
This module contains the deckr client.
"""

import socket
import threading
import time

import proto.client_message_pb2
import proto.server_response_pb2

BUFFER_SIZE = 2048

class DeckrClient(object):  # pylint: disable=too-many-instance-attributes
    """
    A client for interacting with a deckr server.

    A client can run in one of two modes: sync or async. In sync mode, the
    client must explicitly listen for messages. It will still run internal
    callbacks, but it will then return the message from listen. In async mode,
    a special thread will be spun up that will continually listen. It will
    then call a callback whenever a message comes in.
    """

    def __init__(self, ip, port, sync=True, backoff=0.1, callback=None): # pylint: disable=too-many-arguments
        self._ip = ip
        self._port = port
        self._socket = None
        self._backoff = backoff # How long to wait between retries
        self._sync = sync # Should this client run in sync mode.
        self._buffer = ''
        self._listener_thread = None
        self._callback = callback

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

        if not self._sync: # Create the listener thread
            self._listener_thread = threading.Thread(target=self._listener_thread_worker)
            self._listener_thread.daemon = True
            self._listener_thread.start()

    def _listener_thread_worker(self):
        """
        Listen until done.
        """

        while True:
            result = self.listen()
            if not result: # Bail if the socket has closed
                return
            self._callback(result)

    def shutdown(self):
        """
        Cleanly shutdown a client.
        """

        self._socket.close()
        # Note the thread sholud be cleaned up when the program exits.
    def _send_message(self, message):
        """
        Takes in a ClientMessage protobuf, serialize it to a string, and append
        \r\n.
        """

        self._socket.send(message.SerializeToString() + '\r\n')

    def _listen_raw(self):
        """
        Wait for the next raw message
        """

        while True:
            if '\r\n' in self._buffer:
                data, self._buffer = self._buffer.split('\r\n', 1)
                return data
            data = self._socket.recv(BUFFER_SIZE)
            if not data: # No data means the connection has closed.
                self.shutdown()
                return
            self._buffer += data

    def _listen(self):
        """
        Get the next message from the server.
        """

        raw_message = self._listen_raw()
        if not raw_message:
            return
        response = proto.server_response_pb2.ServerResponse()
        response.ParseFromString(raw_message)
        return response

    def listen(self):
        """
        Public listen function. This will wait for the next message, run all
        internal handling, and then return the message.
        """

        return self._listen()

    ###################
    # Client Messages #
    ###################

    def create(self):
        """
        Send a create message to create a new game.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.CREATE
        self._send_message(message)
