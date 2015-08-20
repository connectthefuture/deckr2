#!/usr/bin/env python
"""
This is a very simple proxy that listens on 8001 for websocket traffic to communicate with
the deckr server on the backend.
"""

LISTEN_PORT = 8000
SERVER_PORT = 8080
SERVER_ADDR = "127.0.0.1"
 
import json

from protobuf_to_dict import protobuf_to_dict
from dict_to_protobuf import dict_to_protobuf
from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver
from proto.client_message_pb2 import ClientMessage
from proto.server_response_pb2 import ServerResponse
 
 
# Adapted from http://stackoverflow.com/a/15645169/221061
class ServerProtocol(LineReceiver):
    def __init__(self):
        self.buffer = None
        self.client = None
 
    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ClientProtocol
        factory.server = self

        reactor.connectTCP(SERVER_ADDR, SERVER_PORT, factory)

    # Client => Proxy
    def lineReceived(self, data):
        try:
            data_dict = json.loads(data)
            message = ClientMessage()
            dict_to_protobuf(data_dict, message)
        except:
            self.write("proxy error")
            return
        if self.client:
            self.client.write(message.SerializeToString())
        else:
            self.buffer = data
 
    # Proxy => Client
    def write(self, data):
        self.sendLine(data)
 
 
class ClientProtocol(LineReceiver):
    def connectionMade(self):
        self.factory.server.client = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''
 
    # Server => Proxy
    def lineReceived(self, data):
        # Decode the data and rencode as JSON
        response = ServerResponse()
        response.ParseFromString(data)
        self.factory.server.write(json.dumps(protobuf_to_dict(response)))

    # Proxy => Server
    def write(self, data):
        if data:
            self.sendLine(data)
 
 
 
def main():
    factory = protocol.ServerFactory()
    factory.protocol = ServerProtocol
 
    reactor.listenTCP(LISTEN_PORT, factory)
    reactor.run()
 
 
if __name__ == '__main__':
    main()
