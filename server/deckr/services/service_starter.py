"""
This module provides code that will enable a server to properly start services.
"""


import importlib


class ServiceWrapper(object):
    """
    This class represents a service wrapper. This includes the configuration to actually
    create the service (service_config) and the configuration that should be passed to the
    service (config_for_service).
    """

    def __init__(self, service_config, config_for_service=None):
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


class ServiceStarter(object):
    """
    The service starter is the main entry point into the deckr server. It can take a set of
    services, analyze dependencies, and then make sure that they all start in the proper order.
    """

    def __init__(self, reload_all=False):
        """
        Args:
            reload_all (bool): If true will try to start all services with a reloader. Note that
                individual service configs can still override this.
        """

        #: dict[Name:ServiceWrapper]
        self.services = {}
        #: bool
        self._reload_all = reload_all

    def add_service(self, service_config, config_for_service):
        """
        Register a service that should be added to the services list.

        Args:
            service_config (dict): Configuration needed to create the service
            config_for_service (dict): Configuration to pass to the service upon creation.
        """

        self.services[service_config["name"]] = ServiceWrapper(
            service_config, config_for_service)

    def start(self):
        """
        Start all currently added services.

        Note:
            Most likely this will create a service that takes control of the event loop. Thus,
            if this returns it means it's time to shutdown.
        """

        # Create service instances
        for service in self.services.values():
            service.create()

        # Fix up dependancies
        for service in self.services.values():
            self._satisfy_dependencies(service)

        # Start everything
        start_last = None
        for service in self.services.values():
            if service.requires_event_loop:
                start_last = service
            else:
                service.get_instance().start()
        if start_last is not None:
            start_last.get_instance().start()

    def _satisfy_dependencies(self, service):
        """
        Satisfy the dependencies for a specific service.
        """

        service_instance = service.get_instance()
        for dependancy in service.dependancies:
            service_dep = self.services[dependancy[1]].get_instance()
            getattr(service_instance, 'set_' + dependancy[0])(service_dep)
