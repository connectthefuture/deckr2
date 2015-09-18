#!/usr/bin/env python
"""
A very simple script to run the deckr server.
"""

import argparse
import logging

import yaml

import deckr.core.service

FOREST_CARD_DATA = {
    "name": "Forest",
    "types": ["Land"],
    "supertypes": ["Basic"],
    "subtypes": ["Forest"]
}

SIMPLE_CARD_LIBRARY = {"Forest": FOREST_CARD_DATA}


def parse_arguments():
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(description='Run the deckr server.')
    parser.add_argument('--websockets', action='store_true', help='Run with websocket support')
    parser.add_argument('--base64', action='store_true', help='Run with base64 protobuf encoding/decoding')
    return parser.parse_args()


def main():
    """
    Run main functionality.
    """

    args = parse_arguments()
    # Any basic config for logging goes here
    logging.basicConfig(level=logging.INFO)

    starter = deckr.core.service.ServiceStarter(False)
    starter.add_service(
        yaml.load(open('config/services/deckr_server_service.yml')),
        {'websockets': args.websockets, 'base64': args.base64})
    starter.add_service(
        yaml.load(open('config/services/card_library_service.yml')), {'load_from': 'config/cards.json'})
    starter.add_service(
        yaml.load(open('config/services/action_validator_service.yml')), {})
    starter.add_service(
        yaml.load(open('config/services/game_master_service.yml')), {})
    starter.start()
    starter.stop()  # At this point we've finished everything, since start should block.


if __name__ == "__main__":
    main()
