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

#
# def parse_game_state(game_state):
#     """
#     Parse the game state into something with a little more structure.
#     """
#
#     players = {
#         x.game_id: x.player
#         for x in game_state.game_objects
#         if x.game_object_type == proto.game_pb2.GameObject.PLAYER
#     }
#     zones = {
#         x.game_id: x.zone
#         for x in game_state.game_objects
#         if x.game_object_type == proto.game_pb2.GameObject.ZONE
#     }
#     # cards = {x.game_id: x.card for x in game_state.game_objects
#     #         if x.game_object_type == proto.game_pb2.GameObject.CARD}
#     game = {}
#
#     for game_id, player in players.items():
#         game[game_id] = {
#             'library': zones[player.library].objs,
#             'graveyard': zones[player.graveyard].objs,
#             'hand': zones[player.hand].objs
#         }
#     return game
#
#
# def get_game_object(game_state, game_id):
#     """
#     Get a game object by game_id.
#     """
#
#     for obj in game_state.game_objects:
#         if obj.game_id == game_id:
#             if obj.game_object_type == proto.game_pb2.GameObject.PLAYER:
#                 return obj.player
#             elif obj.game_object_type == proto.game_pb2.GameObject.CARD:
#                 return obj.card
#             elif obj.game_object_type == proto.game_pb2.GameObject.ZONE:
#                 return obj.zone
#             elif obj.game_object_type == proto.game_pb2.GameObject.MANA_POOL:
#                 return obj.mana_pool
#     raise ValueError("{} not in game state response".format(game_id))


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


        
    # def _check_response(self):
    #     """
    #     Get a response and make sure the response does not contain errors.
    #     """
    #
    #     response = self.client.listen()
    #     self.assertIsNotNone(response)
    #     if response.response_type == proto.server_response_pb2.ServerResponse.ERROR:
    #         raise AssertionError("Unexpected error response: " + str(response))
    #     self.last_response = response
    #     return response
    #
    # def _create_join_start(self, card_count=10):
    #     """
    #     Create, join, and start a game. Returns the player that we joined as.
    #     """
    #
    #     self.client.create()
    #     response = self._check_response()
    #     self.client.join(response.create_response.game_id,
    #                      deck=["Forest"] * card_count)
    #     response = self._check_response()
    #     player = response.join_response.player_id
    #     self.client.start()
    #     response = self._check_response()
    #     return player, response
    #
    # def _assert_phase_step(self, phase, step, game_state):
    #     """
    #     Takes in a game state response and makes sure that the phase and step
    #     are correct.
    #     """
    #
    #     self.assertEqual(game_state.current_step, step)
    #     self.assertEqual(game_state.current_phase, phase)
    #
    # def _pass_until(self, test, max_passes=100):
    #     """
    #     Pass priority until a test or until we've passed too many times.
    #     """
    #
    #     for _ in range(max_passes):
    #         self.client.pass_priority()
    #         response = self._check_response()
    #         if test(response.game_state_response.game_state):
    #             return
    #     raise ValueError("Should not have reached {} passes".format(
    #         max_passes))
    #

    #
    #
    #
    # def test_pass_turn_draw(self):
    #     """
    #     Create/join/start a game. Then pass through the turn and make sure you
    #     draw again when the next turn starts.
    #     """
    #
    #     player, response = self._create_join_start()
    #     self._assert_phase_step('beginning', 'upkeep',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('beginning', 'draw',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('precombat main', 'precombat main',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('combat', 'beginning of combat',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('combat', 'declare attackers',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('combat', 'declare blockers',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('combat', 'combat damage',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('combat', 'end of combat',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('postcombat main', 'postcombat main',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('end', 'end',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     # Remove this eventually.
    #     self._assert_phase_step('end', 'cleanup',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     # Now we should be bakc to the untap
    #     self._assert_phase_step('beginning', 'untap',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('beginning', 'upkeep',
    #                             response.game_state_response.game_state)
    #     self.client.pass_priority()
    #     response = self._check_response()
    #     self._assert_phase_step('beginning', 'draw',
    #                             response.game_state_response.game_state)
    #     # Make sure we actually drew a card
    #     game_state = parse_game_state(response.game_state_response.game_state)
    #     self.assertEqual(len(game_state[player]['hand']), 8)
    #
    # def test_lost(self):
    #     """
    #     Make sure if we can't draw than we lose the game.
    #     """
    #
    #     player_id, _ = self._create_join_start(7)
    #     player = get_game_object(
    #         self.last_response.game_state_response.game_state, player_id)
    #     self.assertFalse(player.lost)
    #     self._pass_until(lambda game_state: game_state.current_step == 'draw')
    #     # Don't draw until the start of the second turn
    #     self._pass_until(lambda game_state: game_state.current_step == 'draw')
    #     player = get_game_object(
    #         self.last_response.game_state_response.game_state, player_id)
    #     self.assertTrue(player.lost)
    #
    # def test_play_land(self):
    #     """
    #     Make sure we can play a simple land.
    #     """
    #
    #     player_id, _ = self._create_join_start(7)
    #     player = get_game_object(
    #         self.last_response.game_state_response.game_state, player_id)
    #     # Can only play lands at sorcercy speed
    #     self._pass_until(
    #         lambda game_state: game_state.current_step == 'precombat main')
    #     hand = get_game_object(
    #         self.last_response.game_state_response.game_state, player.hand)
    #     card = hand.objs[0]
    #     # Play the forest
    #     self.client.play(card)
    #     response = self.client.listen()
    #     game_state = response.game_state_response.game_state
    #     hand = get_game_object(game_state, player.hand)
    #     self.assertEqual(len(hand.objs), 6)
    #     self.assertNotIn(card, hand.objs)
    #
    # def test_activate_land(self):
    #     """
    #     Make sure we can play a land and then activate it.
    #     """
    #
    #     # TODO: Refactor this so we don't duplicate code from above
    #     player_id, _ = self._create_join_start(7)
    #     player = get_game_object(
    #         self.last_response.game_state_response.game_state, player_id)
    #     # Can only play lands at sorcercy speed
    #     self._pass_until(
    #         lambda game_state: game_state.current_step == 'precombat main')
    #     hand = get_game_object(
    #         self.last_response.game_state_response.game_state, player.hand)
    #     card = hand.objs[0]
    #     # Play the forest
    #     self.client.play(card)
    #     response = self.client.listen()
    #     game_state = response.game_state_response.game_state
    #     hand = get_game_object(game_state, player.hand)
    #     self.assertEqual(len(hand.objs), 6)
    #     self.assertNotIn(card, hand.objs)
    #     self.client.activate_ability(card, 0)
    #
    #     response = self.client.listen()
    #     game_state = response.game_state_response.game_state
    #     mana_pool = get_game_object(game_state, player.mana_pool)
    #     self.assertEqual(mana_pool.green, 1)
    #
    # def test_play_creature(self):
    #     """
    #     Make sure we can play a creature.
    #     """
    #
    #     self.client.create()
    #     response = self._check_response()
    #     self.client.join(response.create_response.game_id,
    #                      deck=["Grizzly Bears"] * 7)
    #     response = self._check_response()
    #     player_id = response.join_response.player_id
    #     self.client.start()
    #     self._check_response()
    #     player = get_game_object(
    #         self.last_response.game_state_response.game_state, player_id)
    #     # Can only play lands at sorcercy speed
    #     self._pass_until(
    #         lambda game_state: game_state.current_step == 'precombat main')
    #     hand = get_game_object(
    #         self.last_response.game_state_response.game_state, player.hand)
    #     card = hand.objs[0]
    #     # Play the forest
    #     self.client.play(card)
    #     response = self.client.listen()
    #     game_state = response.game_state_response.game_state
    #     hand = get_game_object(game_state, player.hand)
    #     self.assertEqual(len(hand.objs), 6)
    #     self.assertNotIn(card, hand.objs)
    #     # It should not be on the battlefield
    #     # TODO: I need to update the protos to identify the stack/battlefield.
    #     # It should be on the stack
