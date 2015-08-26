"""
This module provides the base GameObject class.
"""

import proto.game_pb2 as proto_lib


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

        # TODO: Make this raise notimplementederror and actually implement
        # in subcalsses.
        proto.game_object_type = proto_lib.GameObject.CARD
