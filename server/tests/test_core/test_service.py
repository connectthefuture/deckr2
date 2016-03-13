"""
This module provides tests related to the service starter.
"""

import unittest

import deckr.core.service
import deckr.debug.reloader
import tests.services


class BaseServiceTestCase(unittest.TestCase):
    """
    Test the base service class.
    """

    def setUp(self):
        self.service = deckr.core.service.Service()

    def test_start(self):
        """
        Start shouldn't do anything but it shouldn't fail either.
        """

        self.service.start()

    def test_stop(self):
        """
        Stop shouldn't do anything but it shouldn't fail either.
        """

        self.service.stop()


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

    def test_stop(self):
        """
        Make sure we properly stop all services.
        """

        self.service_starter.add_service(tests.services.SERVICE_CONFIG, {})
        self.service_starter.start()
        self.service_starter.stop()
        for service in self.service_starter.services.values():
            self.assertTrue(service._instance.stopped)

    def test_event_loop_service(self):
        """
        Make sure we start a service that requires the event loop last.
        """

        self.service_starter.add_service(tests.services.EVENT_LOOP_CONFIG, {})
        self.service_starter.add_service(tests.services.SERVICE_CONFIG, {})
        self.service_starter.start()
        self.assertTrue(isinstance(tests.services.LAST_STARTED,
                                   tests.services.EventLoopService))

    def test_creates_reloadable(self):
        """
        Make sure that we create reloadabale service wrappers if reload is true.
        """

        self.service_starter._reload_all = True
        self.service_starter.add_service(tests.services.SERVICE_CONFIG, {})
        self.assertIsInstance(self.service_starter.services[
                              'TestService'], deckr.debug.reloader.ReloadingServiceWrapper)
