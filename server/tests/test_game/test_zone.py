"""
Test the zone.
"""

from unittest import TestCase

import proto.game_pb2 as proto_lib
from deckr.game.game_object import GameObject
from deckr.game.zone import Zone


class ZoneAsContainerTestCase(TestCase):
    """
    Make sure the zone works as a container.
    """

    def setUp(self):
        self.zone = Zone("test_zone", None)
        self.zone.game_id = 0
        self.object1 = GameObject()
        self.object2 = GameObject()
        self.object3 = GameObject()

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
        for obj in self.zone:
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

        result = self.zone.pop()
        self.assertEqual(len(self.zone), 1)
        self.assertIn(self.object1, self.zone)
        self.assertNotIn(self.object2, self.zone)
        self.assertEqual(result, self.object2)

        self.zone.insert(0, self.object3)
        self.assertEqual(self.zone[0], self.object3)
        self.assertEqual(self.zone[1], self.object1)

        self.zone.remove(self.object1)
        self.assertNotIn(self.object1, self.zone)

    def test_update_proto(self):
        """
        Make sure we can properly update a protobuf.
        """

        proto = proto_lib.GameObject()
        self.zone.append(self.object1)
        self.zone.append(self.object2)
        self.zone.update_proto(proto)

        self.assertEqual(proto.game_object_type, proto_lib.GameObject.ZONE)
        self.assertEqual(len(proto.zone.objs), 2)
        self.assertIn(self.object1.game_id, proto.zone.objs)
        self.assertIn(self.object2.game_id, proto.zone.objs)
