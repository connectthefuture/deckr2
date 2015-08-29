#!/usr/bin/env python

import logging

import yaml

import deckr.core.service


def main():
    # Any basic config for logging goes here
    logging.basicConfig(level=logging.DEBUG)

    starter = deckr.core.service.ServiceStarter(False)
    starter.add_service(yaml.load(open('config/services/deckr_server_service.yml')), {})
    starter.add_service(yaml.load(open('config/services/card_library_service.yml')), {})
    starter.add_service(yaml.load(open('config/services/action_validator_service.yml')), {})
    starter.add_service(yaml.load(open('config/services/game_master_service.yml')), {})
    starter.start()
    starter.stop() # At this point we've finished everything, since start should block.



if __name__ == "__main__":
    main()
