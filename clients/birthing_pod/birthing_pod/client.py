"""
This module provides a client for both the birthing pod server and worker.
"""

#!/usr/bin/env python
"""
This is a very simple client for debugging and testing.
"""

import socket
import threading
import time

import proto.client_message_pb2
import proto.server_response_pb2

BUFFER_SIZE = 2048 # Bytes to request at a time.
BACKOFF = 0.1 # Number of seconds between retries

class Client(object):
    """
    A client for the birthing pod objects. Maintains a persistent Connection
    and includes a bunch of utility methods to make it easier for birthing pod
    to play.
    """

    def __init__(self, deckr_server="127.0.0.1:8080"):
        self._deckr_server = deckr_server
        self._socket = None
        self._buffer = ''

    #########################
    # Starting and stopping #
    #########################

    def initialize(self, max_retries=3):
        """
        Initialize the client and open a connection to the deckr server. If
        the connection fails this will try again up to max_retries.
        """

        ip, port = self._deckr_server.split(':')
        port = int(port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        retry_count = 0
        while True:
            try:
                self._socket.connect((ip, port))
                break
            except IOError as ex:
                retry_count += 1
                if retry_count >= max_retries:
                    print str(retry_count) + "retry attempts failed"
                    raise ex
                time.sleep(BACKOFF)

    def stop(self):
        """
        Cleanly shutdown the the client.
        """

        self.send_message(message_quit())
        self._socket.close()

    ########################
    # Sending and reciving #
    ########################

    def send_message(self, message):
        """
        Takes in a client message protobuf and sends it out over the wire.
        This will not wait for a response; generally you want to use
        send_and_wait.
        """

        self._socket.send(message.SerializeToString() + '\r\n')

    def get_response(self):
        """
        Get a response from the server. Note that because of the async nature,
        it may not actually be the response you were expecting.
        """

        while True:
            # Check for a full message in the buffer
            if '\r\n' in self._buffer:
                data, self._buffer = self._buffer.split('\r\n', 1)
                response = proto.server_response_pb2.ServerResponse()
                response.ParseFromString(data)
                return response
            # Get more data out of the stream
            data = self._socket.recv(BUFFER_SIZE)
            if not data:
                return
            self._buffer += data

    def send_and_wait(self, message):
        """
        This will send a message and then wait for a response.
        """

        self.send_message(message)
        return self.get_response()

    def clear_buffer(self):
        """
        Clear out the buffer.
        """
        self.buffer = ''

###########################################
# Utility functions for cretaing messages #
###########################################
def message_quit():
    message = proto.client_message_pb2.ClientMessage()
    message.message_type = proto.client_message_pb2.ClientMessage.QUIT
    return message

def message_create():
    message = proto.client_message_pb2.ClientMessage()
    message.message_type = proto.client_message_pb2.ClientMessage.CREATE
    return message

def message_join(game_id, deck):
    message = proto.client_message_pb2.ClientMessage()
    message.message_type = proto.client_message_pb2.ClientMessage.JOIN
    message.join_message.game_id = game_id
    message.join_message.client_type = proto.client_message_pb2.JoinMessage.PLAYER
    for card in deck:
        message.join_message.player_config.deck.append(card)
    return message

def message_leave():
    message = proto.client_message_pb2.ClientMessage()
    message.message_type = proto.client_message_pb2.ClientMessage.LEAVE
    return message

def message_start():
    message = proto.client_message_pb2.ClientMessage()
    message.message_type = proto.client_message_pb2.ClientMessage.ACTION
    message.action_message.action_type = proto.client_message_pb2.ActionMessage.START
    return message

def message_pass_priority():
    message = proto.client_message_pb2.ClientMessage()
    message.message_type = proto.client_message_pb2.ClientMessage.ACTION
    message.action_message.action_type = proto.client_message_pb2.ActionMessage.PASS_PRIORITY
    return message
