"""
This module provides the base GameObject class.
"""


class GameObject(object):
    """
    A game object is anything in the game (player, card, zone, etc.). These all have game_ids.
    """

    def __init__(self):
        self.game_id = None
