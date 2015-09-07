"""
This module contains player tests.
"""

import unittest

import deckr.game.card
import deckr.game.player
import mock
import proto.game_pb2 as proto_lib
import tests.utils


class ManaPoolTestCase(unittest.TestCase):
    """
    Tests around the mana pool.
    """

    def setUp(self):
        self.mana_pool = deckr.game.player.ManaPool()

    def test_add(self):
        """
        Make sure we can add mana to a mana pool.
        """

        self.mana_pool.add(white=1, blue=2, black=3, red=4, green=5)
        self.assertEqual(self.mana_pool.white, 1)
        self.assertEqual(self.mana_pool.blue, 2)
        self.assertEqual(self.mana_pool.black, 3)
        self.assertEqual(self.mana_pool.red, 4)
        self.assertEqual(self.mana_pool.green, 5)

    def test_update_proto(self):
        """
        Make sure we can properly update a proto.
        """

        proto = proto_lib.GameObject()
        self.mana_pool.game_id = 0
        self.mana_pool.add(white=1, blue=2, black=3, red=4, green=5)
        self.mana_pool.update_proto(proto)
        self.assertEqual(proto.game_object_type,
                         proto_lib.GameObject.MANA_POOL)
        self.assertEqual(proto.mana_pool.white, 1)
        self.assertEqual(proto.mana_pool.blue, 2)
        self.assertEqual(proto.mana_pool.black, 3)
        self.assertEqual(proto.mana_pool.red, 4)
        self.assertEqual(proto.mana_pool.green, 5)


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
        self.player.mana_pool.game_id = 4

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
        self.assertEqual(forest.controller, self.player)

    def test_play_creature(self):
        """
        Make sure we can play a creature (it should go onto the stack).
        """

        grizzly_bears = deckr.game.card.create_card_from_dict(
            tests.utils.GRIZZLY_BEARS)
        self.player.hand.append(grizzly_bears)
        self.player.mana_pool.add(green=2)
        self.player.play_card(grizzly_bears)
        self.game.stack.append.assert_called_with(grizzly_bears)

    def test_activate_ability(self):
        """
        Make sure we can active a card ability.
        """

        card = mock.MagicMock()
        self.player.activate_ability(card, 0)
        card.activate_ability.assert_called_with(0)
