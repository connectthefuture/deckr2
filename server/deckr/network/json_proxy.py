"""
This file provides the ability to encode/decode from JSON to deckr protobufs.
"""

import json
import protobuf_to_dict
import proto.server_response_pb2
import proto.client_message_pb2


def encode_to_json(input_proto):
    """
    Encode a proto to JSON. Returns a JSON string
    """

    return json.dumps(protobuf_to_dict.protobuf_to_dict(input_proto))


def _dict_to_protobuf(dict_data, proto):
    """
    Populate a dict from a protobuf.
    """

    for key, value in dict_data.items():
        if isinstance(value, dict):
            # This means we have a sub message
            _dict_to_protobuf(value, getattr(proto, key))
        elif isinstance(value, list):
            repeated_obj = getattr(proto, key)
            for x in value:
                try:  # Deal with litterals
                    repeated_obj.append(x)
                except AttributeError:  # Deal with messages
                    _dict_to_protobuf(x, repeated_obj.add())
        else:
            setattr(proto, key, value)


def decode_from_json(data):
    """
    Decode from JSON. Returns a proto (most likely a client message)
    """

    result = proto.client_message_pb2.ClientMessage()
    dict_data = json.loads(data)
    _dict_to_protobuf(dict_data, result)
    return result
