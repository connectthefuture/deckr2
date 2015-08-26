"""
Test the zone.
"""

from unittest import TestCase

from deckr.game.game_object import GameObject
from deckr.game.zone import Zone


class ZoneAsContainerTestCase(TestCase):
    """
    Make sure the zone works as a container.
    """

    def setUp(self):
        self.zone = Zone("test_zone", None)
        self.object1 = GameObject()
        self.object2 = GameObject()
        self.object3 = GameObject()

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
