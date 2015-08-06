class ServiceStarter(object):
    """
    Makes sure that all the services start in the proper order and that they are properly
    connected.
    """

    def add_service(self, config):
		pass
    
	def start(self):
		"""
		Start all currently added services. NOTE: This does not have an event loop; we assume
		one of the services (i.e. the server) will handle the event loop. This will most likely
		be started last.
		"""
	
		pass
