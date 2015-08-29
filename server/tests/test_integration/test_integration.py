"""
This module provides simple integration tests. It will spin up a lightweight server and client,
and send messages from the client to the server with expected responses.
"""

import multiprocessing
import unittest

import nose.plugins.attrib
import yaml

import deckr.core.service
import proto.game_pb2
import proto.server_response_pb2
import tests.test_integration.simple_client
import tests.utils


def start_server():
    """
    Start a lightweight server.
    """
    
    starter = deckr.core.service.ServiceStarter()
    starter.add_service(
        yaml.load(open('config/services/deckr_server_service.yml')), {})
    starter.add_service(
        yaml.load(open('config/services/card_library_service.yml')),
        {'library': tests.utils.SIMPLE_CARD_LIBRARY})
    starter.add_service(
        yaml.load(open('config/services/action_validator_service.yml')), {})
    starter.add_service(
        yaml.load(open('config/services/game_master_service.yml')), {})
    starter.start()

def parse_game_state(game_state):
    """
    Parse the game state into something with a little more structure.
    """

    players = {x.game_id: x.player for x in game_state.game_objects
               if x.game_object_type == proto.game_pb2.GameObject.PLAYER}
    zones = {x.game_id: x.zone for x in game_state.game_objects
             if x.game_object_type == proto.game_pb2.GameObject.ZONE}
    # cards = {x.game_id: x.card for x in game_state.game_objects
    #         if x.game_object_type == proto.game_pb2.GameObject.CARD}
    game = {}

    for game_id, player in players.items():
        game[game_id] = {
            'library': zones[player.library].objs,
            'graveyard': zones[player.graveyard].objs,
            'hand': zones[player.hand].objs
        }
    return game


class SimpleServer(object):
    """
    A very simple instance of a deckr server.
    """

    def __init__(self):
        self._server_process = None

    def start(self):
        """
        Start the server in a subprocess and return.
        """

        self._server_process = multiprocessing.Process(
            target=start_server)
        self._server_process.start()

    def stop(self):
        """
        Terminate the server.
        """

        self._server_process.terminate()

@nose.plugins.attrib.attr('integration')
class SinglePlayerTestCase(unittest.TestCase):
    """
    Integration tests for a single player. Generally, this is more related
    to the network stack than the gaming stack.
    """

    def setUp(self):
        self.server = SimpleServer()
        self.client = tests.test_integration.simple_client.SimpleClient()
        self.server.start()
        self.client.initalize()

    def tearDown(self):
        self.client.shutdown()
        self.server.stop()

    def _check_response(self):
        """
        Get a response and make sure the response does not contain errors.
        """

        response = self.client.listen()
        self.assertIsNotNone(response)
        if response.response_type == proto.server_response_pb2.ServerResponse.ERROR:
            raise AssertionError("Unexpected error response: " + str(response))
        return response

    def test_create(self):
        """
        Make sure that create gets a create response back.
        """

        expected_response = proto.server_response_pb2.ServerResponse()
        expected_response.response_type = proto.server_response_pb2.ServerResponse.CREATE
        expected_response.create_response.game_id = 0

        self.client.create()
        response = self.client.listen()
        self.assertEqual(response, expected_response)

    def test_create_join_start(self):
        """
        Create a game, join it, and then start it. There should be no
        errors.
        """

        self.client.create()
        response = self._check_response()
        self.client.join(response.create_response.game_id,
                         deck=["Forest"] * 10)
        response = self._check_response()
        player = response.join_response.player_id
        self.client.start()
        response = self._check_response()
        # Check the starting hand
        game_state = parse_game_state(response.game_state_response.game_state)
        self.assertEqual(len(game_state[player]['hand']), 7)
