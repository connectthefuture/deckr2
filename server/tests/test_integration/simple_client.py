#!/usr/bin/env python
"""
This is a very simple client for debugging and testing.
"""

import socket
import threading
import time

import proto.client_message_pb2
import proto.server_response_pb2

BUFFER_SIZE = 2048


class SimpleClient(object):
    """
    A very simple class that encapsulates a client. Involves two threads, one for listening and
    printing out the responses, and one for actually sending data.
    """

    def __init__(self, ip_addr='127.0.0.1', port=8080):
        self._socket = None
        self._buffer = ''
        self._listen_thread = None
        self._ip = ip_addr
        self._port = port

    def initalize(self, retry=3, sync=True):
        """
        Initialize the client. If sync is not true it will spin up a thread
        to listen for responses.
        """

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        retry_count = 0
        while True:
            try:
                self._socket.connect((self._ip, self._port))
                break
            except IOError as ex:  # Retry if we can't connect.
                retry_count += 1
                if retry_count >= retry:
                    print str(retry_count) + "retry attempts failed"
                    raise ex
                time.sleep(0.1)

        if not sync:
            self._listen_thread = threading.Thread(
                target=self.listen,
                args=(True, ))
            self._listen_thread.start()

    def shutdown(self):
        """
        Send a quit message and close the socket.
        """

        self.quit()
        self._socket.close()

    def listen(self, listen_forever=False):
        """
        Listen for a message, and print it out when recieved.
        """

        while True:
            data = self._socket.recv(BUFFER_SIZE)
            if not data:
                print "Connection closed"
                return
            self._buffer += data
            if '\r\n' in self._buffer:
                data, self._buffer = self._buffer.split('\r\n', 1)
                response = proto.server_response_pb2.ServerResponse()
                response.ParseFromString(data)
                if listen_forever:
                    print response
                else:
                    return response

    def send_message(self, message):
        """
        Takes in a protobuf and sends it out over the socket.
        """

        self._socket.send(message.SerializeToString() + '\r\n')

    def create(self):
        """
        Send a create message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.CREATE
        self.send_message(message)

    def join(self, game_id,
             client_type=proto.client_message_pb2.JoinMessage.PLAYER,
             deck=None):
        """
        Send a join message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.JOIN
        message.join_message.game_id = game_id
        message.join_message.client_type = client_type
        if deck is not None:
            for card in deck:
                message.join_message.player_config.deck.append(card)
        self.send_message(message)

    def quit(self):
        """
        Send the quit message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.QUIT
        self.send_message(message)

    def leave(self):
        """
        Send the leave message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.LEAVE
        self.send_message(message)

    def start(self):
        """
        Send a start message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.START
        self.send_message(message)

    def pass_priority(self):
        """
        Pass prioirty.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.PASS_PRIORITY
        self.send_message(message)

    def play(self, card):
        """
        Play a card (specified by card id).
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.PLAY
        message.action_message.play.card = card
        self.send_message(message)
