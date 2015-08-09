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
    logging.warn("Shut it down.")


if __name__ == "__main__":
    main()
