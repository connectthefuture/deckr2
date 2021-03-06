"""
This module provides the base GameObject and the Zone and Ability game objects
"""


class GameObject(object):
    """
    A game object is anything in the game (player, card, zone, etc.). These all have game_ids.
    """

    def __init__(self):
        self.game_id = None

    def update_proto(self, proto):
        """
        Get a protobuf representation of this game object.
        """

        proto.game_id = self.game_id

    def add_to_zone(self, zone):
        """
        Called whenever this object is added to a zone. No-op by default.
        """

        pass
