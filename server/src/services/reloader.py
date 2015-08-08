"""
This module provides code for relodaing services in development. Essentially we wrap each service
in a seperate process and then proxy between them using queues. This way, we can kill a process and
restart it (forcing a code reload) without anybody else noticing.

Note:
    This is not foolproof. Your milage may vary.
"""

class Reloader(object):
    """
    This handles all of the reloading logic. It handles file watching, process reloading, and
    transparent proxying.
    """

    def __init__(self, service_config):
        """
        Args:
            service_config: A ServiceConfig.
        """

    def create(self):
        """
        Create the service (but does not start it).

        Returns:
            ReloaderProxy: A proxy that can be called as if it were the original class.
        """

        pass

    def start(self):
        """
        Start the service. Since this works in another process, this will return, even if the
        service requires the event loop.
        """

        pass

class ReloaderProxy(object):
    """
    This represents a proxy object. If on the sending end it's returned as a normal object. If
    it's on the reciving end it will invoke _listen and wait until it's killed through KILL
    message.
    """

    def __init__(self, send_queue, recieve_queue, proxy_for=None):
        #: Queue for sending messages
        self._send_queue = send_queue
        #: Queue for recieving responses
        self._recieve_queue = recieve_queue
        #: object Object that we're proxying for
        self._proxy_for = proxy_for

    def _listen(self):
        """
        Block on the recieve_queue. Once you get a message, proxy it to the item and then dump
        the response into the send_queue. If we get a KILL message, leave the loop.
        """

        pass

    def __getattr__(self, name):
        """
        Needed to proxy arbitrary method calls.
        """

        pass
