"""
This module provides tests related to the service starter.
"""

import unittest

import deckr.core.service
import tests.services


class ServiceStarterTestCase(unittest.TestCase):
    """
    Test the service starter.
    """

    def setUp(self):
        self.service_starter = deckr.core.service.ServiceStarter(False)

    def test_add_service(self):
        """
        Make sure we can create a new service.
        """

        self.service_starter.add_service(tests.services.SERVICE_CONFIG, {})
        self.assertEqual(len(self.service_starter.services), 1)

    def test_start_simple(self):
        """
        Make sure that we can create and start a single service.
        """

        previous_count = tests.services.TIMES_STARTED
        self.service_starter.add_service(tests.services.SERVICE_CONFIG, {})
        self.service_starter.start()
        self.assertEqual(tests.services.TIMES_STARTED, previous_count + 1)

    def test_start_dependancy(self):
        """
        Make sure that we can do dependancy checking.
        """

        previous_count = tests.services.TIMES_STARTED
        self.service_starter.add_service(tests.services.SERVICE_CONFIG, {})
        self.service_starter.add_service(tests.services.DEPENDENT_CONFIG, {})
        self.service_starter.start()
        # Note that we have other assertions in dependent service start.
        self.assertEqual(tests.services.TIMES_STARTED, previous_count + 1)

    def test_event_loop_service(self):
        """
        Make sure we start a service that requires the event loop last.
        """

        self.service_starter.add_service(tests.services.EVENT_LOOP_CONFIG, {})
        self.service_starter.add_service(tests.services.SERVICE_CONFIG, {})
        self.service_starter.start()
        self.assertTrue(isinstance(tests.services.LAST_STARTED,
                                   tests.services.EventLoopService))
