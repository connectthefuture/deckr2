"""
This module contains player tests.
"""

import unittest

import deckr.game.card
import deckr.game.player
import mock
import proto.game_pb2 as proto_lib
import tests.utils


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

    def test_draw(self):
        """
        Make sure we can draw a card, and we lose if we can't
        """

        self.player.library.append(object())
        self.player.draw()
        self.assertEqual(len(self.player.hand), 1)

        self.player.draw()
        self.assertTrue(self.player.lost)

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
        self.assertEqual(proto.player.lost, self.player.lost)

    def test_play_land(self):
        """
        Make sure we can properly play a land.
        """

        forest = deckr.game.card.create_card_from_dict(
            tests.utils.FOREST_CARD_DATA)
        self.player.hand.append(forest)
        self.player.play_card(forest)
        self.game.battlefield.append.assert_called_with(forest)
