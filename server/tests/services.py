import deckr.core.service

# pylint: skip-file
# Incemented whenever a service starts
TIMES_STARTED = 0
LAST_STARTED = None

SERVICE_CONFIG = {
    'name': 'TestService',
    'module': 'tests.services',
    'class': 'TestService',
}

DEPENDENT_CONFIG = {
    'name': 'DependentService',
    'module': 'tests.services',
    'class': 'DependentService',
    'dependancies': [['test_service', 'TestService']]
}

EVENT_LOOP_CONFIG = {
    'name': 'EventLoopService',
    'module': 'tests.services',
    'class': 'EventLoopService',
    'requires_event_loop': True,
}

ECHO_SERVICE = {
    'name': 'EchoService',
    'module': 'tests.services',
    'class': 'EchoService',
}


class TestService(deckr.core.service.Service):
    """
    A very simple test service.
    """

    def __init__(self, config):
        self.config = config

    def start(self):
        global TIMES_STARTED, LAST_STARTED
        TIMES_STARTED += 1
        LAST_STARTED = self


class DependentService(deckr.core.service.Service):
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


class EventLoopService(deckr.core.service.Service):
    """
    A service that is marked as requiring the event loop.
    """

    def __init__(self, config):
        pass

    def start(self):
        global LAST_STARTED
        LAST_STARTED = self


class EchoService(deckr.core.service.Service):
    """
    A simple service that exports a single method.
    """

    def __init__(self, config):
        pass

    def echo(self, msg):
        return "Echo: " + msg
