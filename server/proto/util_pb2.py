# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/util.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/util.proto',
  package='',
  serialized_pb=_b('\n\x10proto/util.proto\"*\n\x0cKeyValuePair\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_KEYVALUEPAIR = _descriptor.Descriptor(
  name='KeyValuePair',
  full_name='KeyValuePair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='KeyValuePair.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='KeyValuePair.value', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  oneofs=[
  ],
  serialized_start=20,
  serialized_end=62,
)

DESCRIPTOR.message_types_by_name['KeyValuePair'] = _KEYVALUEPAIR

KeyValuePair = _reflection.GeneratedProtocolMessageType('KeyValuePair', (_message.Message,), dict(
  DESCRIPTOR = _KEYVALUEPAIR,
  __module__ = 'proto.util_pb2'
  # @@protoc_insertion_point(class_scope:KeyValuePair)
  ))
_sym_db.RegisterMessage(KeyValuePair)


# @@protoc_insertion_point(module_scope)
