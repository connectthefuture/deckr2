"""
This file contains a bunch of utilities/common code for the tests.
"""

FOREST_CARD_DATA = {
    "name": "Forest",
    "types": ["Land"],
    "supertypes": ["Basic"],
    "subtypes": ["Forest"]
}

GRIZZLY_BEARS = {
    "name": "Grizzly Bears",
    "types": ["Creature"],
    "subtypes": ["Bear"],
    "power": 2,
    "toughness": 2
}

SIMPLE_CARD_LIBRARY = {
    "Forest": FOREST_CARD_DATA,
    "Grizzly Bears": GRIZZLY_BEARS
}
