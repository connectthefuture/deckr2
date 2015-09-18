# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game_action.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='game_action.proto',
  package='',
  serialized_pb='\n\x11game_action.proto\"\x1a\n\nPlayAction\x12\x0c\n\x04\x63\x61rd\x18\x01 \x02(\x05\"-\n\x0e\x41\x63tivateAction\x12\x0c\n\x04\x63\x61rd\x18\x01 \x02(\x05\x12\r\n\x05index\x18\x02 \x02(\x05\"\x89\x01\n\x16\x44\x65\x63lareAttackersAction\x12:\n\tattackers\x18\x01 \x03(\x0b\x32\'.DeclareAttackersAction.AttackerMapping\x1a\x33\n\x0f\x41ttackerMapping\x12\x10\n\x08\x61ttacker\x18\x01 \x02(\x05\x12\x0e\n\x06target\x18\x02 \x02(\x05\"\x85\x01\n\x15\x44\x65\x63lareBlockersAction\x12\x37\n\x08\x62lockers\x18\x01 \x03(\x0b\x32%.DeclareBlockersAction.BlockerMapping\x1a\x33\n\x0e\x42lockerMapping\x12\x0f\n\x07\x62locker\x18\x01 \x02(\x05\x12\x10\n\x08\x62locking\x18\x02 \x02(\x05')




_PLAYACTION = _descriptor.Descriptor(
  name='PlayAction',
  full_name='PlayAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='card', full_name='PlayAction.card', index=0,
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
  serialized_start=21,
  serialized_end=47,
)


_ACTIVATEACTION = _descriptor.Descriptor(
  name='ActivateAction',
  full_name='ActivateAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='card', full_name='ActivateAction.card', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='index', full_name='ActivateAction.index', index=1,
      number=2, type=5, cpp_type=1, label=2,
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
  serialized_start=49,
  serialized_end=94,
)


_DECLAREATTACKERSACTION_ATTACKERMAPPING = _descriptor.Descriptor(
  name='AttackerMapping',
  full_name='DeclareAttackersAction.AttackerMapping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='attacker', full_name='DeclareAttackersAction.AttackerMapping.attacker', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='target', full_name='DeclareAttackersAction.AttackerMapping.target', index=1,
      number=2, type=5, cpp_type=1, label=2,
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
  serialized_start=183,
  serialized_end=234,
)

_DECLAREATTACKERSACTION = _descriptor.Descriptor(
  name='DeclareAttackersAction',
  full_name='DeclareAttackersAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='attackers', full_name='DeclareAttackersAction.attackers', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DECLAREATTACKERSACTION_ATTACKERMAPPING, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=97,
  serialized_end=234,
)


_DECLAREBLOCKERSACTION_BLOCKERMAPPING = _descriptor.Descriptor(
  name='BlockerMapping',
  full_name='DeclareBlockersAction.BlockerMapping',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blocker', full_name='DeclareBlockersAction.BlockerMapping.blocker', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='blocking', full_name='DeclareBlockersAction.BlockerMapping.blocking', index=1,
      number=2, type=5, cpp_type=1, label=2,
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
  serialized_start=319,
  serialized_end=370,
)

_DECLAREBLOCKERSACTION = _descriptor.Descriptor(
  name='DeclareBlockersAction',
  full_name='DeclareBlockersAction',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blockers', full_name='DeclareBlockersAction.blockers', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_DECLAREBLOCKERSACTION_BLOCKERMAPPING, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=237,
  serialized_end=370,
)

_DECLAREATTACKERSACTION_ATTACKERMAPPING.containing_type = _DECLAREATTACKERSACTION;
_DECLAREATTACKERSACTION.fields_by_name['attackers'].message_type = _DECLAREATTACKERSACTION_ATTACKERMAPPING
_DECLAREBLOCKERSACTION_BLOCKERMAPPING.containing_type = _DECLAREBLOCKERSACTION;
_DECLAREBLOCKERSACTION.fields_by_name['blockers'].message_type = _DECLAREBLOCKERSACTION_BLOCKERMAPPING
DESCRIPTOR.message_types_by_name['PlayAction'] = _PLAYACTION
DESCRIPTOR.message_types_by_name['ActivateAction'] = _ACTIVATEACTION
DESCRIPTOR.message_types_by_name['DeclareAttackersAction'] = _DECLAREATTACKERSACTION
DESCRIPTOR.message_types_by_name['DeclareBlockersAction'] = _DECLAREBLOCKERSACTION

class PlayAction(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PLAYACTION

  # @@protoc_insertion_point(class_scope:PlayAction)

class ActivateAction(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ACTIVATEACTION

  # @@protoc_insertion_point(class_scope:ActivateAction)

class DeclareAttackersAction(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class AttackerMapping(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DECLAREATTACKERSACTION_ATTACKERMAPPING

    # @@protoc_insertion_point(class_scope:DeclareAttackersAction.AttackerMapping)
  DESCRIPTOR = _DECLAREATTACKERSACTION

  # @@protoc_insertion_point(class_scope:DeclareAttackersAction)

class DeclareBlockersAction(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class BlockerMapping(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _DECLAREBLOCKERSACTION_BLOCKERMAPPING

    # @@protoc_insertion_point(class_scope:DeclareBlockersAction.BlockerMapping)
  DESCRIPTOR = _DECLAREBLOCKERSACTION

  # @@protoc_insertion_point(class_scope:DeclareBlockersAction)


# @@protoc_insertion_point(module_scope)
