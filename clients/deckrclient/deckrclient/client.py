"""
This module contains the deckr client.
"""

import socket
import threading
import time

import proto.client_message_pb2
import proto.server_response_pb2

BUFFER_SIZE = 2048

class ManaPool(object):
    """
    Represent a mana pool.
    """
    
    def __init__(self, proto):
        self.white = proto.white
        self.blue = proto.blue
        self.black = proto.black
        self.green = proto.green
        self.red = proto.red

class Card(object):
    """
    A simple repesentation of a card.
    """

    def __init__(self, proto):
        self.game_id = proto.game_id
        self.name = proto.name


class Player(object):
    """
    A simple representation of a player loaded from a proto.
    """

    def __init__(self, proto):
        self.game_id = proto.game_id
        self.life = proto.life
        self.lost = proto.lost
        self.graveyard = [Card(x) for x in proto.graveyard.cards]
        self.hand = [Card(x) for x in proto.hand.cards]
        self.library = [Card(x) for x in proto.library.cards]
        self.mana_pool = ManaPool(proto.mana_pool)

class GameState(object):
    """
    A simple representation of the game state.
    """

    def __init__(self, proto, player_id=None):
        self.step = proto.current_step
        self.phase = proto.current_phase
        self.players = [Player(x) for x in proto.players]
        self.active_player = self.get_player_by_id(proto.active_player)
        self.priority_player = self.get_player_by_id(proto.priority_player)
        self.exile = [Card(x) for x in proto.exile.cards]
        self.battlefield = [Card(x) for x in proto.battlefield.cards]
        self.stack = [Card(x) for x in proto.stack.cards]
        if player_id is not None:
            self.player = self.get_player_by_id(player_id)
        else:
            self.player = None

    def get_player_by_id(self, player_id):
        """
        Get a player by their game id.
        """

        return [x for x in self.players if x.game_id == player_id][0]

class DeckrClient(object):  # pylint: disable=too-many-instance-attributes
    """
    A client for interacting with a deckr server.

    A client can run in one of two modes: sync or async. In sync mode, the
    client must explicitly listen for messages. It will still run internal
    callbacks, but it will then return the message from listen. In async mode,
    a special thread will be spun up that will continually listen. It will
    then call a callback whenever a message comes in.
    """

    def __init__(self, ip, port, sync=True,
                 backoff=0.1, callback=None, raise_errors=False): # pylint: disable=too-many-arguments
        self._ip = ip
        self._port = port
        self._socket = None
        self._backoff = backoff # How long to wait between retries
        self._sync = sync # Should this client run in sync mode.
        self._buffer = ''
        self._listener_thread = None
        self._callback = callback
        self._raise_errors = raise_errors # Should any error message be treated as an exception?

        # Game state
        self.player_id = None
        self.game_state = None

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

        Note that an async thread is dameonized so we don't have to clean it
        up.
        """

        self._socket.close()

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

        response = self._listen()
        # Run internal handlers
        if self._raise_errors and response.response_type == proto.server_response_pb2.ServerResponse.ERROR:
            raise ValueError(response)
        if response.response_type == proto.server_response_pb2.ServerResponse.JOIN:
            self.player_id = response.join_response.player_id
        elif response.response_type == proto.server_response_pb2.ServerResponse.GAME_STATE:
            self.game_state = GameState(response.game_state_response.game_state, self.player_id)
        return response

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

    def join(self, game_id, deck=None):
        """
        Send a join message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.JOIN
        message.join_message.game_id = game_id
        message.join_message.client_type = proto.client_message_pb2.JoinMessage.PLAYER
        if deck is not None:
            for card in deck:
                message.join_message.player_config.deck.append(card)
        self._send_message(message)

    def start(self):
        """
        Send a start message.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.START
        self._send_message(message)

    def pass_priority(self):
        """
        Pass prioirty.
        """

        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.PASS_PRIORITY
        self._send_message(message)

    def play(self, card):
        """
        Play a card. Either takes in an int (for a game_id) or a Card object.
        """


        if isinstance(card, int):
            card_id = card
        else:
            card_id = card.game_id
        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.PLAY
        message.action_message.play.card = card_id
        self._send_message(message)

    def activate_ability(self, card, index):
        """
        Activate a card's ability
        """

        if isinstance(card, int):
            card_id = card
        else:
            card_id = card.game_id
        message = proto.client_message_pb2.ClientMessage()
        message.message_type = proto.client_message_pb2.ClientMessage.ACTION
        message.action_message.action_type = proto.client_message_pb2.ActionMessage.ACTIVATE
        message.action_message.activate_ability.card = card_id
        message.action_message.activate_ability.index = index
        self._send_message(message)
