# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


import util_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='game.proto',
  package='',
  serialized_pb='\n\ngame.proto\x1a\nutil.proto\"[\n\tGameState\x12\x15\n\rcurrent_phase\x18\x01 \x02(\t\x12\x14\n\x0c\x63urrent_step\x18\x02 \x02(\t\x12!\n\x0cgame_objects\x18\x03 \x03(\x0b\x32\x0b.GameObject\"\xdf\x01\n\nGameObject\x12\x34\n\x10game_object_type\x18\x01 \x02(\x0e\x32\x1a.GameObject.GameObjectType\x12\x17\n\x06player\x18\x02 \x01(\x0b\x32\x07.Player\x12\x13\n\x04zone\x18\x03 \x01(\x0b\x32\x05.Zone\x12\x13\n\x04\x63\x61rd\x18\x04 \x01(\x0b\x32\x05.Card\x12\x19\n\x07\x63ounter\x18\x05 \x01(\x0b\x32\x08.Counter\"=\n\x0eGameObjectType\x12\n\n\x06PLAYER\x10\x00\x12\x08\n\x04ZONE\x10\x01\x12\x08\n\x04\x43\x41RD\x10\x02\x12\x0b\n\x07\x43OUNTER\x10\x03\"n\n\x06Player\x12\x0f\n\x07game_id\x18\x01 \x02(\x05\x12\x13\n\x04hand\x18\x02 \x02(\x0b\x32\x05.Zone\x12\x18\n\tgraveyard\x18\x03 \x02(\x0b\x32\x05.Zone\x12\x16\n\x07library\x18\x04 \x02(\x0b\x32\x05.Zone\x12\x0c\n\x04life\x18\x05 \x02(\x05\"%\n\x04Zone\x12\x0f\n\x07game_id\x18\x01 \x02(\x05\x12\x0c\n\x04objs\x18\x02 \x03(\x05\"\xe4\x01\n\x04\x43\x61rd\x12\x0f\n\x07game_id\x18\x01 \x02(\x05\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\x11\n\tmana_cost\x18\x03 \x01(\t\x12\r\n\x05\x63olor\x18\x04 \x01(\t\x12\x13\n\x0bsuper_types\x18\x05 \x03(\t\x12\r\n\x05types\x18\x06 \x03(\t\x12\x10\n\x08subtypes\x18\x07 \x03(\t\x12\x11\n\tabilities\x18\x08 \x03(\t\x12\x13\n\x0b\x66lavor_text\x18\t \x01(\t\x12\r\n\x05power\x18\n \x01(\x05\x12\x11\n\ttoughness\x18\x0b \x01(\x05\x12\x1b\n\x04meta\x18\x0c \x03(\x0b\x32\r.KeyValuePair\"(\n\x07\x43ounter\x12\x0f\n\x07game_id\x18\x01 \x02(\x05\x12\x0c\n\x04type\x18\x02 \x02(\t\"E\n\x07\x41\x62ility\x12\x0f\n\x07game_id\x18\x01 \x02(\x05\x12\x12\n\nability_on\x18\x02 \x02(\x05\x12\x15\n\rability_index\x18\x03 \x02(\x05')



_GAMEOBJECT_GAMEOBJECTTYPE = _descriptor.EnumDescriptor(
  name='GameObjectType',
  full_name='GameObject.GameObjectType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PLAYER', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ZONE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CARD', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COUNTER', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=282,
  serialized_end=343,
)


_GAMESTATE = _descriptor.Descriptor(
  name='GameState',
  full_name='GameState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='current_phase', full_name='GameState.current_phase', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='current_step', full_name='GameState.current_step', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='game_objects', full_name='GameState.game_objects', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=26,
  serialized_end=117,
)


_GAMEOBJECT = _descriptor.Descriptor(
  name='GameObject',
  full_name='GameObject',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_object_type', full_name='GameObject.game_object_type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player', full_name='GameObject.player', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='zone', full_name='GameObject.zone', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='card', full_name='GameObject.card', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='counter', full_name='GameObject.counter', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GAMEOBJECT_GAMEOBJECTTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=120,
  serialized_end=343,
)


_PLAYER = _descriptor.Descriptor(
  name='Player',
  full_name='Player',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_id', full_name='Player.game_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hand', full_name='Player.hand', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='graveyard', full_name='Player.graveyard', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='library', full_name='Player.library', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='life', full_name='Player.life', index=4,
      number=5, type=5, cpp_type=1, label=2,
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
  serialized_start=345,
  serialized_end=455,
)


_ZONE = _descriptor.Descriptor(
  name='Zone',
  full_name='Zone',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_id', full_name='Zone.game_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='objs', full_name='Zone.objs', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=457,
  serialized_end=494,
)


_CARD = _descriptor.Descriptor(
  name='Card',
  full_name='Card',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_id', full_name='Card.game_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='Card.name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mana_cost', full_name='Card.mana_cost', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='color', full_name='Card.color', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='super_types', full_name='Card.super_types', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='types', full_name='Card.types', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subtypes', full_name='Card.subtypes', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='abilities', full_name='Card.abilities', index=7,
      number=8, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flavor_text', full_name='Card.flavor_text', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='power', full_name='Card.power', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='toughness', full_name='Card.toughness', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='meta', full_name='Card.meta', index=11,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=497,
  serialized_end=725,
)


_COUNTER = _descriptor.Descriptor(
  name='Counter',
  full_name='Counter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_id', full_name='Counter.game_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='type', full_name='Counter.type', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=727,
  serialized_end=767,
)


_ABILITY = _descriptor.Descriptor(
  name='Ability',
  full_name='Ability',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='game_id', full_name='Ability.game_id', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ability_on', full_name='Ability.ability_on', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ability_index', full_name='Ability.ability_index', index=2,
      number=3, type=5, cpp_type=1, label=2,
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
  serialized_start=769,
  serialized_end=838,
)

_GAMESTATE.fields_by_name['game_objects'].message_type = _GAMEOBJECT
_GAMEOBJECT.fields_by_name['game_object_type'].enum_type = _GAMEOBJECT_GAMEOBJECTTYPE
_GAMEOBJECT.fields_by_name['player'].message_type = _PLAYER
_GAMEOBJECT.fields_by_name['zone'].message_type = _ZONE
_GAMEOBJECT.fields_by_name['card'].message_type = _CARD
_GAMEOBJECT.fields_by_name['counter'].message_type = _COUNTER
_GAMEOBJECT_GAMEOBJECTTYPE.containing_type = _GAMEOBJECT;
_PLAYER.fields_by_name['hand'].message_type = _ZONE
_PLAYER.fields_by_name['graveyard'].message_type = _ZONE
_PLAYER.fields_by_name['library'].message_type = _ZONE
_CARD.fields_by_name['meta'].message_type = util_pb2._KEYVALUEPAIR
DESCRIPTOR.message_types_by_name['GameState'] = _GAMESTATE
DESCRIPTOR.message_types_by_name['GameObject'] = _GAMEOBJECT
DESCRIPTOR.message_types_by_name['Player'] = _PLAYER
DESCRIPTOR.message_types_by_name['Zone'] = _ZONE
DESCRIPTOR.message_types_by_name['Card'] = _CARD
DESCRIPTOR.message_types_by_name['Counter'] = _COUNTER
DESCRIPTOR.message_types_by_name['Ability'] = _ABILITY

class GameState(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMESTATE

  # @@protoc_insertion_point(class_scope:GameState)

class GameObject(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _GAMEOBJECT

  # @@protoc_insertion_point(class_scope:GameObject)

class Player(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PLAYER

  # @@protoc_insertion_point(class_scope:Player)

class Zone(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ZONE

  # @@protoc_insertion_point(class_scope:Zone)

class Card(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CARD

  # @@protoc_insertion_point(class_scope:Card)

class Counter(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _COUNTER

  # @@protoc_insertion_point(class_scope:Counter)

class Ability(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _ABILITY

  # @@protoc_insertion_point(class_scope:Ability)


# @@protoc_insertion_point(module_scope)
