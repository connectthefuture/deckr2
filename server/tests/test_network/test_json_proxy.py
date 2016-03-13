"""
Unittests for the JSON proxy functions.
"""

import json
import unittest

import deckr.network.json_proxy
import proto.client_message_pb2
import proto.server_response_pb2


class JsonProxyTestCase(unittest.TestCase):
    """
    Unittests around the json proxy.
    """

    def test_encode_game_state(self):
        """
        Take a game state and make sure we can encode it.
        """

        message = proto.server_response_pb2.ServerResponse()
        message.response_type = proto.server_response_pb2.ServerResponse.GAME_STATE
        message.game_state_response.game_state.current_step = 'untap'
        message.game_state_response.game_state.current_phase = 'beginning'
        message.game_state_response.game_state.active_player = 1
        message.game_state_response.game_state.priority_player = 1
        player1 = message.game_state_response.game_state.players.add()
        player1.game_id = 1
        player1.life = 20
        hand = player1.hand
        hand.game_id = 2
        card = hand.cards.add()
        card.game_id = 3
        card.name = "Forest"

        result = deckr.network.json_proxy.encode_to_json(message)
        dict_data = json.loads(result)
        self.assertEqual(dict_data['response_type'], 4)
        game_state = dict_data['game_state_response']['game_state']
        self.assertEqual(game_state['current_step'], 'untap')
        self.assertEqual(game_state['current_phase'], 'beginning')
        self.assertEqual(game_state['active_player'], 1)
        self.assertEqual(game_state['priority_player'], 1)

    def test_decode_create(self):
        """
        Make sure we can decode a create message.
        """

        message = {
            'message_type': proto.client_message_pb2.ClientMessage.CREATE
        }

        result = deckr.network.json_proxy.decode_from_json(json.dumps(message))
        self.assertEqual(result.message_type,
                         proto.client_message_pb2.ClientMessage.CREATE)

    def test_decode_join(self):
        """
        Make sure we can decode a join message.
        """

        message = {
            'message_type': proto.client_message_pb2.ClientMessage.JOIN,
            'join_message': {
                'game_id': 1,
                'player_config': {
                    'deck': ["Forest"]
                }
            }
        }

        result = deckr.network.json_proxy.decode_from_json(json.dumps(message))
        self.assertEqual(result.message_type,
                         proto.client_message_pb2.ClientMessage.JOIN)
        self.assertEqual(result.join_message.game_id, 1)
        self.assertEqual(len(result.join_message.player_config.deck), 1)
        self.assertEqual(result.join_message.player_config.deck[0], "Forest")

    def test_decode_declare_attackers(self):
        """
        Make sure we can decode declare attackers message.
        """

        message = {
            'message_type': proto.client_message_pb2.ClientMessage.ACTION,
            'action_message': {
                'action_type': proto.client_message_pb2.ActionMessage.DECLARE_ATTACKERS,
                'declare_attackers': {
                    'attackers': [
                        {'attacker': 1, 'target': 2}
                    ]
                }
            }
        }
        result = deckr.network.json_proxy.decode_from_json(json.dumps(message))
        self.assertEqual(result.message_type,
                         proto.client_message_pb2.ClientMessage.ACTION)
        self.assertEqual(len(result.action_message.declare_attackers.attackers), 1)
