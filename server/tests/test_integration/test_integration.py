"""
This module provides simple integration tests. It will spin up a lightweight server and client,
and send messages from the client to the server with expected responses.
"""

import multiprocessing
import unittest

import nose.plugins.attrib
import yaml

import deckr.core.service
import deckrclient.client
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

        self._server_process = multiprocessing.Process(target=start_server)
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

    @classmethod
    def setUpClass(cls):
        cls.server = SimpleServer()
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def setUp(self):
        self.client = deckrclient.client.DeckrClient(ip='127.0.0.1',
                                                     port=8080, raise_errors=True)
        self.client.initialize()

    def tearDown(self):
        self.client.shutdown()

    def _create_join_start(self, deck):
        """
        Create, join, and start a game. Returns the player that we joined as.
        """

        self.client.create()
        response = self.client.listen()
        self.client.join(response.create_response.game_id,
                         deck=deck)
        self.client.listen()
        self.client.start()
        self.client.listen()

    def _assert_phase_step(self, phase, step):
        """
        Takes in a game state response and makes sure that the phase and step
        are correct.
        """

        self.assertEqual(self.client.game_state.step, step)
        self.assertEqual(self.client.game_state.phase, phase)

    def _pass_until_step(self, step):
        """
        Pass until we reach the step.
        """

        while not self.client.game_state.step == step:
            self.client.pass_priority()
            self.client.listen()

    def test_create(self):
        """
        Make sure that create gets a create response back.
        """

        self.client.create()
        response = self.client.listen()
        self.assertEqual(response.response_type,
                         proto.server_response_pb2.ServerResponse.CREATE)
        self.assertIsNotNone(response.create_response.game_id)

    def test_create_join_start(self):
        """
        Create a game, join it, and then start it. There should be no
        errors.
        """

        deck = ["Forest"] * 7
        self._create_join_start(deck)
        self.assertEqual(len(self.client.game_state.player.hand), 7)
        for card in self.client.game_state.player.hand:
            self.assertEqual(card.name, "Forest")

    def test_pass_turn_draw(self):
        """
        Create/join/start a game. Then pass through the turn and make sure you
        draw again when the next turn starts.
        """

        deck = ["Forest"] * 8
        self._create_join_start(deck)
        self._assert_phase_step('beginning', 'upkeep')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('beginning', 'draw')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('precombat main', 'precombat main')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('combat', 'beginning of combat')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('combat', 'declare attackers')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('combat', 'declare blockers')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('combat', 'combat damage')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('combat', 'end of combat')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('postcombat main', 'postcombat main')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('end', 'end')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('end', 'cleanup')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('beginning', 'untap')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('beginning', 'upkeep')
        self.client.pass_priority()
        self.client.listen()
        self._assert_phase_step('beginning', 'draw')
        self.client.pass_priority()
        self.client.listen()
        self.assertEqual(len(self.client.game_state.player.hand), 8)

    def test_lost(self):
        """
        Make sure if we can't draw than we lose the game.
        """

        self._create_join_start(["Forest"] * 7)
        self.assertFalse(self.client.game_state.player.lost)
        self._pass_until_step('draw')
        # Need to force the second turn.
        self.client.pass_priority()
        self.client.listen()
        self._pass_until_step('draw')
        self.assertTrue(self.client.game_state.player.lost)

    def test_play_land(self):
        """
        Make sure we can play a simple land.
        """

        self._create_join_start(["Forest"] * 7)
        self._pass_until_step('precombat main')
        card = self.client.game_state.player.hand[0]
        self.client.play(card)
        self.client.listen()
        self.assertEqual(len(self.client.game_state.player.hand), 6)
        self.assertEqual(len(self.client.game_state.battlefield), 1)
        self.assertEqual(self.client.game_state.battlefield[0].game_id, card.game_id)

    def test_activate_land(self):
        """
        Make sure we can play a land and then activate it.
        """

        self._create_join_start(["Forest"] * 7)
        self._pass_until_step('precombat main')
        card = self.client.game_state.player.hand[0]
        self.client.play(card)
        self.client.listen()
        self.client.activate_ability(card, 0)
        self.client.listen()
        self.assertEqual(self.client.game_state.player.mana_pool.green, 1)
