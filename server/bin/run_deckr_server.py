#!/usr/bin/env python

import logging

import yaml

from deckr.services.service_starter import ServiceStarter


def main():
    # Any basic config for logging goes here
    logging.basicConfig(level=logging.DEBUG)

    starter = ServiceStarter(False)
    starter.add_service(yaml.load(open('config/services/deckr_server_service.yml')), {})
    starter.add_service(yaml.load(open('config/services/game_master_service.yml')), {})
    starter.start()
    starter.stop() # At this point we've finished everything, since start should block.



if __name__ == "__main__":
    main()
