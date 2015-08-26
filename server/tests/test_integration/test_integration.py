"""
This module provides simple integration tests. It will spin up a lightweight server and client,
and send messages from the client to the server with expected responses.
"""

import multiprocessing
import time
from unittest import TestCase

import yaml
from nose.plugins.attrib import attr

from deckr.services.service_starter import ServiceStarter
from proto.server_response_pb2 import ServerResponse
from tests.test_integration.simple_client import SimpleClient


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
            target=self._start_server)
        self._server_process.start()

    def stop(self):
        """
        Terminate the server.
        """

        self._server_process.terminate()

    def _start_server(self):
        """
        Actually start the server. Main target for multiprocessing.
        """

        starter = ServiceStarter()
        starter.add_service(
            yaml.load(open('config/services/deckr_server_service.yml')), {})
        starter.add_service(
            yaml.load(open('config/services/card_library_service.yml')), {})
        starter.add_service(
            yaml.load(open('config/services/action_validator_service.yml')), {})
        starter.add_service(
            yaml.load(open('config/services/game_master_service.yml')), {})
        starter.start()


@attr('integration')
class SinglePlayerTestCase(TestCase):
    """
    Integration tests for a single player. Generally, this is more related
    to the network stack than the gaming stack.
    """

    def setUp(self):
        self.server = SimpleServer()
        self.client = SimpleClient()
        self.server.start()
        time.sleep(0.1)  # Wait for the server to start up.
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
        if response.response_type == ServerResponse.ERROR:
            raise AssertionError("Unexpected error response: " + str(response))
        return response

    def test_create(self):
        """
        Make sure that create gets a create response back.
        """

        expected_response = ServerResponse()
        expected_response.response_type = ServerResponse.CREATE
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
        self.client.join(response.create_response.game_id)
        response = self._check_response()
        self.client.start()
        response = self._check_response()
