from network.proxy import Proxy

class DeckrServer(object):
    """
    An interface for the deckr server.
    """

    def __init__(self):
        self.proxy = Proxy()

    def start(self):
	"""
	At this point the server takes over the event loop.
	"""

	pass

    def stop(self):
	"""
	Shutdown the server. Also relinquish control of the event loop.
	"""
	pass
