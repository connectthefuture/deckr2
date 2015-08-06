class Connection(object):
    """
    This represents a single client connection. Each connection can be associated with at most
    1 game (or 0 games).
    """

    def send_response(self, response):
    	"""
    	Response should be a protobuf. This will encode it and send it out over the wire.
    	"""

    	pass

    def recieve_message(self, message):
    	"""
    	Message should be a raw string that this connection has recieved. This function will
    	decode it to a protobuf and route it appropriatly.
    	"""

    	pass
