"""
This module tests the basic functionality of the service wrapper.
"""

import unittest

import deckr.core.service_wrapper
import tests.services


class ServiceWrapperTestCase(unittest.TestCase):
    """
    Test the service config class.
    """

    def setUp(self):
        self.config_for_service = {'foo': 'bar'}
        self.service_wrapper = deckr.core.service_wrapper.ServiceWrapper(tests.services.SERVICE_CONFIG,
                                                                         self.config_for_service)

    def test_create(self):
        """
        Make sure we can create a service instance.
        """

        service = self.service_wrapper.create()
        self.assertIsNotNone(service)
        self.assertTrue(isinstance(service, tests.services.TestService))
        self.assertEqual(service.config, self.config_for_service)
        self.assertEqual(self.service_wrapper.get_instance(), service)
