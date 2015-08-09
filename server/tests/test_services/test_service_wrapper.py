"""
This module tests the basic functionality of the service wrapper.
"""

from unittest import TestCase

from deckr.services.service_wrapper import ServiceWrapper
from tests.test_services.services import SERVICE_CONFIG, TestService


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
