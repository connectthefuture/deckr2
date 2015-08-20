"""
This module provides tests related to the service starter.
"""

from unittest import TestCase

import tests.test_services.services as test_services
from deckr.services.service_starter import ServiceStarter


class ServiceStarterTestCase(TestCase):
    """
    Test the service starter.
    """

    def setUp(self):
        self.service_starter = ServiceStarter(False)

    def test_add_service(self):
        """
        Make sure we can create a new service.
        """

        self.service_starter.add_service(test_services.SERVICE_CONFIG, {})
        self.assertEqual(len(self.service_starter.services), 1)

    def test_start_simple(self):
        """
        Make sure that we can create and start a single service.
        """

        previous_count = test_services.TIMES_STARTED
        self.service_starter.add_service(test_services.SERVICE_CONFIG, {})
        self.service_starter.start()
        self.assertEqual(test_services.TIMES_STARTED, previous_count + 1)

    def test_start_dependancy(self):
        """
        Make sure that we can do dependancy checking.
        """

        previous_count = test_services.TIMES_STARTED
        self.service_starter.add_service(test_services.SERVICE_CONFIG, {})
        self.service_starter.add_service(test_services.DEPENDENT_CONFIG, {})
        self.service_starter.start()
        # Note that we have other assertions in dependent service start.
        self.assertEqual(test_services.TIMES_STARTED, previous_count + 1)

    def test_event_loop_service(self):
        """
        Make sure we start a service that requires the event loop last.
        """

        self.service_starter.add_service(test_services.EVENT_LOOP_CONFIG, {})
        self.service_starter.add_service(test_services.SERVICE_CONFIG, {})
        self.service_starter.start()
        self.assertTrue(isinstance(test_services.LAST_STARTED,
                                   test_services.EventLoopService))
