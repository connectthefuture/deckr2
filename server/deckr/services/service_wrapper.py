"""
This module provides the code for a simple service wrapper.
"""

import importlib


class ServiceWrapper(object):
    """
    This class represents a service wrapper. This includes the configuration to actually
    create the service (service_config) and the configuration that should be passed to the
    service (config_for_service).
    """

    def __init__(self, service_config, config_for_service=None):
        super(ServiceWrapper, self).__init__()
        self.name = service_config["name"]
        self.dependancies = service_config.get("dependancies", [])
        self.requires_event_loop = service_config.get(
            "requires_event_loop", False)
        self._module = service_config["module"]
        self._class = service_config["class"]

        self._instance = None
        #: dict Configuration that will be passed to the service on creation.
        self.config_for_service = config_for_service

    def create(self):
        """
        Create a new service using this configuration.

        Note:
            All modules will be imported at this point. If running with reloading, make sure
            you fork **before** you call create.

        Returns:
            object The newly created instance
        """

        mod = importlib.import_module(self._module)
        service_class = getattr(mod, self._class)
        self._instance = service_class(config=self.config_for_service)
        return self._instance

    def get_instance(self):
        """
        Get the current instance of the service. Should only be called after
        create.
        """

        return self._instance
