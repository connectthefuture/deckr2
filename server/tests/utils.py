"""
This file contains a bunch of utilities/common code for the tests.
"""

FOREST_CARD_DATA = {
    "name": "Forest",
    "types": ["Land"],
    "supertypes": ["Basic"],
    "subtypes": ["Forest"],
    "abilities": ["{T}: Add {G} to your mana pool"]
}

GRIZZLY_BEARS = {
    "name": "Grizzly Bears",
    "types": ["Creature"],
    "subtypes": ["Bear"],
    "power": 2,
    "toughness": 2,
    "mana_cost": "1G"
}

SIMPLE_CARD_LIBRARY = {
    "Forest": FOREST_CARD_DATA,
    "Grizzly Bears": GRIZZLY_BEARS
}
