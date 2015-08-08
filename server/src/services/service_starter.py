"""
This module provides code that will enable a server to properly start services.
"""

class ServiceConfig(object):
    """
    This class represents a service configuration. This includes the configuration to actually
    create the service (service_config) and the configuration that should be passed to the
    service (config_for_service).
    """

    def __init__(self, service_config, config_for_service=None):
        #: dict Everything needed to create the service.
        self._service_config = service_config
        #: dict Configuration that will be passed to the service on creation.
        self._config_for_service = config_for_service

    def create(self):
        """
        Create a new service using this configuration.

        Note:
            All modules will be imported at this point. If running with reloading, make sure
            you fork **before** you call create.
        """

        pass

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

        #: List[ServiceConfig]
        self._services = []
        #: bool
        self._reload_all = reload_all

    def add_service(self, service_config, config_for_service):
		"""
        Register a service that should be added to the services list.

        Args:
            service_config (dict): Configuration needed to create the service
            config_for_service (dict): Configuration to pass to the service upon creation.
        """

	def start(self):
		"""
		Start all currently added services.

        Note:
            Most likely this will create a service that takes control of the event loop. Thus,
            if this returns it means it's time to shutdown.
		"""

		pass
