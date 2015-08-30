"""
This module contains player tests.
"""

import unittest

import deckr.game.player
import mock
import proto.game_pb2 as proto_lib


class PlayerTestCase(unittest.TestCase):
    """
    Simple tests around the player.
    """

    def setUp(self):
        self.game = mock.MagicMock()
        self.player = deckr.game.player.Player(self.game)

        # Mock out game ids
        self.player.game_id = 0
        self.player.library.game_id = 1
        self.player.graveyard.game_id = 2
        self.player.hand.game_id = 3

    def test_pass_priority(self):
        """
        Make sure that we can properly pass priority.
        """

        self.player.pass_priority()
        self.game.turn_manager.advance.assert_called_with()

    def test_update_proto(self):
        """
        Make sure we can properly update a protobuf.
        """

        proto = proto_lib.GameObject()
        self.player.update_proto(proto)
        self.assertEqual(proto.player.life, self.player.life)
        self.assertEqual(proto.player.graveyard, self.player.graveyard.game_id)
        self.assertEqual(proto.player.library, self.player.library.game_id)
        self.assertEqual(proto.player.hand, self.player.hand.game_id)
