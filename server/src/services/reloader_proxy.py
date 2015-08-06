"""
NOTE: These will block. Only use these in development. You may seen unexpected interaction with other
libraries (i.e. twisted).
"""

class ReloaderProxyCaller(object):
    """
    The reloader will probably use multiprocessing to restart services. This class allows other services
    to continue running even if services they rely on are restarted. All function calls are intercepted,
    and passed through a queue to teh other side. The other side is constantly reading off of this
    queue and sending back the response. This will probably only handle traffic going one way (hopefully
    our service graph is a DAG).
    """

    def __init__(self, queue):
        self._queue = queue

    def __getattr__(self, name):
        """
        Needed to proxy arbitrary method calls.
        """

        pass

class ReloaderProxyCallee(object):
    """
    This should be passed to the subprocess.
    """

    def __init__(self, queue, proxy_for):
        eslf._queue = queue
        self._proxy_for = proxy_for

    def listen(self):
        """
        Start waiting for requests to come in.
        """

        pass
