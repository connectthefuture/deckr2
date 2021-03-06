"""
Test the zone.
"""

import unittest

import mock

import deckr.game.game_object
import deckr.game.zone
import proto.game_pb2 as proto_lib


class StackTestCase(unittest.TestCase):
    """
    Test the functionality of the stack.
    """

    def setUp(self):
        self.game = mock.MagicMock()
        self.card = mock.MagicMock()
        self.stack = deckr.game.zone.Stack(name="stack",
                                           owner=None,
                                           game=self.game)

    def test_resolve_permanent(self):
        """
        Make sure that when we resolve a permanent it goes onto the battlefield.
        """

        self.card.is_permanent.return_value = True
        self.stack.append(self.card)
        self.stack.resolve()
        self.game.battlefield.append.assert_called_with(self.card)
        self.assertNotIn(self.card, self.stack)


class ZoneAsContainerTestCase(unittest.TestCase):
    """
    Make sure the zone works as a container.
    """

    def setUp(self):
        self.zone = deckr.game.zone.Zone("test_zone", None)
        self.zone.game_id = 0
        self.object1 = deckr.game.game_object.GameObject()
        self.object2 = deckr.game.game_object.GameObject()
        self.object3 = deckr.game.game_object.GameObject()

        self.object1.game_id = 1
        self.object2.game_id = 2
        self.object3.game_id = 3

    def test_magic(self):
        """
        Make sure the magic functions (len, in, [], iteration) work.
        """

        # Hack the objs directly
        self.zone._objs = [self.object1, self.object2]
        # Test all of the expected functionality
        self.assertIn(self.object1, self.zone)
        self.assertNotIn(self.object3, self.zone)
        self.assertEqual(len(self.zone), 2)
        self.assertEqual(self.zone[0], self.object1)
        count = 0
        for _ in self.zone:
            count += 1
        self.assertEqual(count, 2)

    def test_modification(self):
        """
        Make sure we can modify the zone with append, pop, insert, and remove.
        """

        self.zone.append(self.object1)
        self.zone.append(self.object2)
        self.assertEqual(len(self.zone), 2)
        self.assertIn(self.object1, self.zone)
        self.assertIn(self.object2, self.zone)

        # Zone has both object1 and object2
        result = self.zone.pop()
        self.assertEqual(len(self.zone), 1)
        self.assertIn(self.object1, self.zone)
        self.assertNotIn(self.object2, self.zone)
        self.assertEqual(result, self.object2)

        # Zone has just object 1
        self.zone.insert(0, self.object3)
        self.assertEqual(self.zone[0], self.object3)
        self.assertEqual(self.zone[1], self.object1)

        # Zone has object1 and 3
        self.zone.remove(self.object1)
        self.assertNotIn(self.object1, self.zone)

        # Zone has object 3
        self.zone.append(self.object1)
        result = self.zone.pop(0)
        self.assertEqual(result, self.object3)

    def test_is_empty(self):
        """
        Make sure we can tell if a zone is empty.
        """

        self.assertTrue(self.zone.is_empty())
        self.zone.append(self.object1)
        self.assertFalse(self.zone.is_empty())

    def test_update_proto(self):
        """
        Make sure we can properly update a protobuf.
        """

        proto = proto_lib.Zone()
        self.zone.append(self.object1)
        self.zone.append(self.object2)
        self.zone.update_proto(proto)

        self.assertEqual(len(proto.cards), 2)
        ids = [x.game_id for x in proto.cards]
        self.assertIn(self.object1.game_id, ids)
        self.assertIn(self.object2.game_id, ids)

    def test_triggers_callback(self):
        """
        Make sure we trigger callbacks upon adding to zones.
        """

        obj = mock.MagicMock()
        self.zone.append(obj)
        obj.add_to_zone.assert_called_with(self.zone)
        obj.reset_mock()
        self.zone.insert(0, obj)
        obj.add_to_zone.assert_called_with(self.zone)
