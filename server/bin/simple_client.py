#!/usr/bin/env python
"""
This is a very simple client for debugging and testing. This is meant to be run interactivily.
"""

import socket

from proto.client_message_pb2 import ClientMessage
from proto.server_response_pb2 import ServerResponse

TCP_IP = '127.0.0.1'
TCP_PORT = 8080
BUFFER_SIZE = 2048

class ClientConnection(object):

    def __init__(self):
        self.socket = None
        self.buffer = ''

    def initalize(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((TCP_IP, TCP_PORT))

    def shutdown(self):
        self.quit()
        self.socket.close()

    def send_message(self, message):
        """
        Takes in a protobuf, waits for a response and then returns it.
        """

        self.socket.send(message.SerializeToString() + '\r\n')

        while(True):
            data = self.socket.recv(BUFFER_SIZE)
            if not data:
                print "Connection closed"
                return
            self.buffer += data
            if '\r\n' in self.buffer:
                data, self.buffer = self.buffer.split('\r\n', 1)
                break

        response = ServerResponse()
        response.ParseFromString(data)
        print response
        return response

    def quit(self):
        message = ClientMessage()
        message.message_type = ClientMessage.QUIT
        self.send_message(message)

connection = ClientConnection()
connection.initalize()
