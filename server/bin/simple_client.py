#!/usr/bin/env python
"""
This is a very simple client for debugging and testing.

Run this interactivily with python -i ./bin/simple_client.py
"""

import socket
import threading

from proto.client_message_pb2 import ClientMessage, JoinMessage
from proto.server_response_pb2 import ServerResponse

TCP_IP = '127.0.0.1'
TCP_PORT = 8080
BUFFER_SIZE = 2048

class ClientConnection(object):
    """
    A very simple class that encapsulates a client. Involves two threads, one for listening and
    printing out the responses, and one for actually sending data.
    """

    def __init__(self):
        self._socket = None
        self._buffer = ''
        self._listen_thread = None

    def initalize(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TCP_IP, TCP_PORT))

        # Start a listener thread
        self._listen_thread = threading.Thread(target=connection.listen)
        self._listen_thread.start()

    def shutdown(self):
        """
        Send a quit message and close the socket.
        """

        self.quit()
        self.socket.close()

    def listen(self):
        """
        Listen for a message, and print it out when recieved.
        """

        while(True):
            data = self.socket.recv(BUFFER_SIZE)
            if not data:
                print("Connection closed")
                return
            self.buffer += data
            if '\r\n' in self.buffer:
                data, self.buffer = self.buffer.split('\r\n', 1)
                response = ServerResponse()
                response.ParseFromString(data)
                print(response)

    def send_message(self, message):
        """
        Takes in a protobuf and sends it out over the socket.
        """

        self.socket.send(message.SerializeToString() + '\r\n')

    def create(self):
        """
        Send a create message.
        """

        message = ClientMessage()
        message.message_type = ClientMessage.CREATE
        self.send_message(message)

    def join(self, game_id, client_type=JoinMessage.PLAYER):
        """
        Send a join message.
        """

        message = ClientMessage()
        message.message_type = ClientMessage.JOIN
        message.join_message.game_id = game_id
        message.join_message.client_type = client_type
        self.send_message(message)

    def quit(self):
        """
        Send the quit message.
        """

        message = ClientMessage()
        message.message_type = ClientMessage.QUIT
        self.send_message(message)

if __name__ == "__main__":
    connection = ClientConnection()
    connection.initalize()
