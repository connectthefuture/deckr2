"""
This module provides code for services.
"""

import logging

import deckr.core.service_wrapper
import deckr.debug.reloader

LOGGER = logging.getLogger(__name__)


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

        if self._reload_all:
            wrapper = deckr.debug.reloader.ReloadingServiceWrapper(
                service_config, config_for_service)
        else:
            wrapper = deckr.core.service_wrapper.ServiceWrapper(
                service_config, config_for_service)
        self.services[service_config["name"]] = wrapper

    def start(self):
        """
        Start all currently added services.

        Note:
            Most likely this will create a service that takes control of the event loop. Thus,
            if this returns it means it's time to shutdown.
        """

        # Create service instances
        LOGGER.info("Creating all services")
        for service in self.services.values():
            service.create()

        # Fix up dependancies
        LOGGER.info("Injecting service dependancies")
        for service in self.services.values():
            self._satisfy_dependencies(service)

        # Start everything
        LOGGER.info("Starting all services")
        start_last = None
        for service in self.services.values():
            if service.requires_event_loop:
                start_last = service
            else:
                service.start()
        if start_last is not None:
            start_last.start()

    def stop(self):
        """
        Stop all of the services.
        """

        LOGGER.info("Stopping all services")
        for service in self.services.values():
            service.stop()

    def _satisfy_dependencies(self, service):
        """
        Satisfy the dependencies for a specific service.
        """

        service_instance = service.get_instance()
        for dependancy in service.dependancies:
            service_dep = self.services[dependancy[1]].get_instance()
            getattr(service_instance, 'set_' + dependancy[0])(service_dep)


class Service(object):
    """
    A service is pretty simple. It just has a start and a stop method. Additionally, it takes an
    optional init argument called 'config'.
    """

    def start(self):
        """
        Start the service.
        """

        pass

    def stop(self):
        """
        Stop the service gracefully.
        """

        pass
