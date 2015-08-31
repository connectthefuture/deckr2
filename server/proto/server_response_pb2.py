# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server_response.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import game_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='server_response.proto',
  package='',
  serialized_pb='\n\x15server_response.proto\x1a\ngame.proto\"\x8a\x03\n\x0eServerResponse\x12\x39\n\rresponse_type\x18\x01 \x02(\x0e\x32\".ServerResponse.ServerResponseType\x12(\n\x0f\x63reate_response\x18\x02 \x01(\x0b\x32\x0f.CreateResponse\x12$\n\rjoin_response\x18\x03 \x01(\x0b\x32\r.JoinResponse\x12&\n\x0e\x65rror_response\x18\x04 \x01(\x0b\x32\x0e.ErrorResponse\x12/\n\x13game_state_response\x18\x05 \x01(\x0b\x32\x12.GameStateResponse\x12\x31\n\x14game_update_response\x18\x06 \x01(\x0b\x32\x13.GameUpdateResponse\"a\n\x12ServerResponseType\x12\n\n\x06\x43REATE\x10\x00\x12\x08\n\x04JOIN\x10\x01\x12\t\n\x05LEAVE\x10\x02\x12\t\n\x05\x45RROR\x10\x03\x12\x0e\n\nGAME_STATE\x10\x04\x12\x0f\n\x0bGAME_UPDATE\x10\x05\"!\n\x0e\x43reateResponse\x12\x0f\n\x07game_id\x18\x01 \x02(\x05\" \n\rErrorResponse\x12\x0f\n\x07message\x18\x01 \x02(\t\"3\n\x11GameStateResponse\x12\x1e\n\ngame_state\x18\x01 \x02(\x0b\x32\n.GameState\"!\n\x0cJoinResponse\x12\x11\n\tplayer_id\x18\x01 \x02(\x05\"F\n\x12GameUpdateResponse\x12 \n\x0bgame_object\x18\x01 \x02(\x0b\x32\x0b.GameObject\x12\x0e\n\x06remove\x18\x02 \x01(\x08')



_SERVERRESPONSE_SERVERRESPONSETYPE = _descriptor.EnumDescriptor(
  name='ServerResponseType',
  full_name='ServerResponse.ServerResponseType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CREATE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JOIN', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEAVE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ERROR', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GAME_STATE', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GAME_UPDATE', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=335,
  serialized_end=432,
)


_SERVERRESPONSE = _descriptor.Descriptor(
  name='ServerResponse',
  full_name='ServerResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response_type', full_name='ServerResponse.response_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='create_response', full_name='ServerResponse.create_response', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='join_response', full_name='ServerResponse.join_response', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_response', full_name='ServerResponse.error_response', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='game_state_response', full_name='ServerResponse.game_state_response', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='game_update_response', full_name='ServerResponse.game_update_response', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SERVERRESPONSE_SERVERRESPONSETYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=38,
  serialized_end=432,
)


_CREATERESPONSE = _descriptor.Descriptor(
  name='CreateResponse',
  full_name='CreateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_id', full_name='CreateResponse.game_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=434,
  serialized_end=467,
)


_ERRORRESPONSE = _descriptor.Descriptor(
  name='ErrorResponse',
  full_name='ErrorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='ErrorResponse.message', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=469,
  serialized_end=501,
)


_GAMESTATERESPONSE = _descriptor.Descriptor(
  name='GameStateResponse',
  full_name='GameStateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_state', full_name='GameStateResponse.game_state', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=503,
  serialized_end=554,
)


_JOINRESPONSE = _descriptor.Descriptor(
  name='JoinResponse',
  full_name='JoinResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='player_id', full_name='JoinResponse.player_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=556,
  serialized_end=589,
)


_GAMEUPDATERESPONSE = _descriptor.Descriptor(
  name='GameUpdateResponse',
  full_name='GameUpdateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_object', full_name='GameUpdateResponse.game_object', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='remove', full_name='GameUpdateResponse.remove', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=591,
  serialized_end=661,
)

_SERVERRESPONSE.fields_by_name['response_type'].enum_type = _SERVERRESPONSE_SERVERRESPONSETYPE
_SERVERRESPONSE.fields_by_name['create_response'].message_type = _CREATERESPONSE
_SERVERRESPONSE.fields_by_name['join_response'].message_type = _JOINRESPONSE
_SERVERRESPONSE.fields_by_name['error_response'].message_type = _ERRORRESPONSE
_SERVERRESPONSE.fields_by_name['game_state_response'].message_type = _GAMESTATERESPONSE
_SERVERRESPONSE.fields_by_name['game_update_response'].message_type = _GAMEUPDATERESPONSE
_SERVERRESPONSE_SERVERRESPONSETYPE.containing_type = _SERVERRESPONSE;
_GAMESTATERESPONSE.fields_by_name['game_state'].message_type = game_pb2._GAMESTATE
_GAMEUPDATERESPONSE.fields_by_name['game_object'].message_type = game_pb2._GAMEOBJECT
DESCRIPTOR.message_types_by_name['ServerResponse'] = _SERVERRESPONSE
DESCRIPTOR.message_types_by_name['CreateResponse'] = _CREATERESPONSE
DESCRIPTOR.message_types_by_name['ErrorResponse'] = _ERRORRESPONSE
DESCRIPTOR.message_types_by_name['GameStateResponse'] = _GAMESTATERESPONSE
DESCRIPTOR.message_types_by_name['JoinResponse'] = _JOINRESPONSE
DESCRIPTOR.message_types_by_name['GameUpdateResponse'] = _GAMEUPDATERESPONSE

class ServerResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SERVERRESPONSE

  # @@protoc_insertion_point(class_scope:ServerResponse)

class CreateResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CREATERESPONSE

  # @@protoc_insertion_point(class_scope:CreateResponse)

class ErrorResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ERRORRESPONSE

  # @@protoc_insertion_point(class_scope:ErrorResponse)

class GameStateResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMESTATERESPONSE

  # @@protoc_insertion_point(class_scope:GameStateResponse)

class JoinResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _JOINRESPONSE

  # @@protoc_insertion_point(class_scope:JoinResponse)

class GameUpdateResponse(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMEUPDATERESPONSE

  # @@protoc_insertion_point(class_scope:GameUpdateResponse)


# @@protoc_insertion_point(module_scope)
