"""
This module provides tests related to the service starter.
"""

from unittest import TestCase

from deckr.services.service import Service
from deckr.services.service_starter import ServiceStarter, ServiceWrapper

# Incemented whenever a service starts
TIMES_STARTED = 0
LAST_STARTED = None

SERVICE_CONFIG = {
    'name': 'TestService',
    'module': 'tests.test_services.test_service_starter',
    'class': 'TestService',
}

DEPENDENT_CONFIG = {
    'name': 'DependentService',
    'module': 'tests.test_services.test_service_starter',
    'class': 'DependentService',
    'dependancies': [['test_service', 'TestService']]
}

EVENT_LOOP_CONFIG = {
    'name': 'EventLoopService',
    'module': 'tests.test_services.test_service_starter',
    'class': 'EventLoopService',
    'requires_event_loop': True,
}

class TestService(Service):
    """
    A very simple test service.
    """

    def __init__(self, config):
        self.config = config

    def start(self):
        global TIMES_STARTED, LAST_STARTED
        TIMES_STARTED += 1
        LAST_STARTED = self

class DependentService(Service):
    """
    A service that depends on a test service.
    """

    def __init__(self, config):
        self._test_service = None

    def set_test_service(self, test_service):
        self._test_service = test_service

    def start(self):
        assert self._test_service is not None
        assert isinstance(self._test_service, TestService)

class EventLoopService(Service):
    """
    A service that is marked as requiring the event loop.
    """

    def __init__(self, config):
        pass

    def start(self):
        global LAST_STARTED
        LAST_STARTED = self

class ServiceWrapperTestCase(TestCase):
    """
    Test the service config class.
    """

    def setUp(self):
        self.config_for_service = {'foo': 'bar'}
        self.service_wrapper = ServiceWrapper(SERVICE_CONFIG,
                                              self.config_for_service)

    def test_create(self):
        """
        Make sure we can create a service instance.
        """

        service = self.service_wrapper.create()
        self.assertIsNotNone(service)
        self.assertTrue(isinstance(service, TestService))
        self.assertEqual(service.config, self.config_for_service)
        self.assertEqual(self.service_wrapper.get_instance(), service)

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

        self.service_starter.add_service(SERVICE_CONFIG, {})
        self.assertEqual(len(self.service_starter.services), 1)

    def test_start_simple(self):
        """
        Make sure that we can create and start a single service.
        """

        previous_count = TIMES_STARTED
        self.service_starter.add_service(SERVICE_CONFIG, {})
        self.service_starter.start()
        self.assertEqual(TIMES_STARTED, previous_count + 1)

    def test_start_dependancy(self):
        """
        Make sure that we can do dependancy checking.
        """

        previous_count = TIMES_STARTED
        self.service_starter.add_service(SERVICE_CONFIG, {})
        self.service_starter.add_service(DEPENDENT_CONFIG, {})
        self.service_starter.start()
        # Note that we have other assertions in dependent service start.
        self.assertEqual(TIMES_STARTED, previous_count + 1)

    def test_event_loop_service(self):
        """
        Make sure we start a service that requires the event loop last.
        """

        self.service_starter.add_service(EVENT_LOOP_CONFIG, {})
        self.service_starter.add_service(SERVICE_CONFIG, {})
        self.service_starter.start()
        self.assertTrue(isinstance(LAST_STARTED, EventLoopService))
