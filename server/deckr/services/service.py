"""
This module provides the service interface.
"""


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
