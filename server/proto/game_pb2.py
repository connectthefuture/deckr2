# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: game.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import util_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='game.proto',
  package='',
  serialized_pb=_b('\n\ngame.proto\x1a\nutil.proto\"[\n\tGameState\x12\x15\n\rcurrent_phase\x18\x01 \x02(\t\x12\x14\n\x0c\x63urrent_step\x18\x02 \x02(\t\x12!\n\x0cgame_objects\x18\x03 \x03(\x0b\x32\x0b.GameObject\"\x9d\x02\n\nGameObject\x12\x34\n\x10game_object_type\x18\x01 \x02(\x0e\x32\x1a.GameObject.GameObjectType\x12\x0f\n\x07game_id\x18\x02 \x02(\x05\x12\x17\n\x06player\x18\x03 \x01(\x0b\x32\x07.Player\x12\x13\n\x04zone\x18\x04 \x01(\x0b\x32\x05.Zone\x12\x13\n\x04\x63\x61rd\x18\x05 \x01(\x0b\x32\x05.Card\x12\x19\n\x07\x63ounter\x18\x06 \x01(\x0b\x32\x08.Counter\x12\x1c\n\tmana_pool\x18\x07 \x01(\x0b\x32\t.ManaPool\"L\n\x0eGameObjectType\x12\n\n\x06PLAYER\x10\x00\x12\x08\n\x04ZONE\x10\x01\x12\x08\n\x04\x43\x41RD\x10\x02\x12\x0b\n\x07\x43OUNTER\x10\x03\x12\r\n\tMANA_POOL\x10\x04\"i\n\x06Player\x12\x0c\n\x04hand\x18\x01 \x02(\x05\x12\x11\n\tgraveyard\x18\x02 \x02(\x05\x12\x0f\n\x07library\x18\x03 \x02(\x05\x12\x0c\n\x04life\x18\x04 \x02(\x05\x12\x0c\n\x04lost\x18\x05 \x02(\x08\x12\x11\n\tmana_pool\x18\x06 \x02(\x05\"\x14\n\x04Zone\x12\x0c\n\x04objs\x18\x01 \x03(\x05\"\xd3\x01\n\x04\x43\x61rd\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x11\n\tmana_cost\x18\x02 \x01(\t\x12\r\n\x05\x63olor\x18\x03 \x01(\t\x12\x13\n\x0bsuper_types\x18\x04 \x03(\t\x12\r\n\x05types\x18\x05 \x03(\t\x12\x10\n\x08subtypes\x18\x06 \x03(\t\x12\x11\n\tabilities\x18\x07 \x03(\t\x12\x13\n\x0b\x66lavor_text\x18\x08 \x01(\t\x12\r\n\x05power\x18\t \x01(\x05\x12\x11\n\ttoughness\x18\n \x01(\x05\x12\x1b\n\x04meta\x18\x0b \x03(\x0b\x32\r.KeyValuePair\"\x17\n\x07\x43ounter\x12\x0c\n\x04type\x18\x01 \x02(\t\"4\n\x07\x41\x62ility\x12\x12\n\nability_on\x18\x01 \x02(\x05\x12\x15\n\rability_index\x18\x02 \x02(\x05\"R\n\x08ManaPool\x12\r\n\x05white\x18\x01 \x02(\x05\x12\x0c\n\x04\x62lue\x18\x02 \x02(\x05\x12\r\n\x05\x62lack\x18\x03 \x02(\x05\x12\x0b\n\x03red\x18\x04 \x02(\x05\x12\r\n\x05green\x18\x05 \x02(\x05')
  ,
  dependencies=[util_pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



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
    _descriptor.EnumValueDescriptor(
      name='MANA_POOL', index=4, number=4,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=329,
  serialized_end=405,
)
_sym_db.RegisterEnumDescriptor(_GAMEOBJECT_GAMEOBJECTTYPE)


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
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='current_step', full_name='GameState.current_step', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  oneofs=[
  ],
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
      name='game_id', full_name='GameObject.game_id', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='player', full_name='GameObject.player', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='zone', full_name='GameObject.zone', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='card', full_name='GameObject.card', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='counter', full_name='GameObject.counter', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mana_pool', full_name='GameObject.mana_pool', index=6,
      number=7, type=11, cpp_type=10, label=1,
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
  oneofs=[
  ],
  serialized_start=120,
  serialized_end=405,
)


_PLAYER = _descriptor.Descriptor(
  name='Player',
  full_name='Player',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='hand', full_name='Player.hand', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='graveyard', full_name='Player.graveyard', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='library', full_name='Player.library', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='life', full_name='Player.life', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lost', full_name='Player.lost', index=4,
      number=5, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mana_pool', full_name='Player.mana_pool', index=5,
      number=6, type=5, cpp_type=1, label=2,
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
  oneofs=[
  ],
  serialized_start=407,
  serialized_end=512,
)


_ZONE = _descriptor.Descriptor(
  name='Zone',
  full_name='Zone',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='objs', full_name='Zone.objs', index=0,
      number=1, type=5, cpp_type=1, label=3,
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
  oneofs=[
  ],
  serialized_start=514,
  serialized_end=534,
)


_CARD = _descriptor.Descriptor(
  name='Card',
  full_name='Card',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Card.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mana_cost', full_name='Card.mana_cost', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='color', full_name='Card.color', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='super_types', full_name='Card.super_types', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='types', full_name='Card.types', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subtypes', full_name='Card.subtypes', index=5,
      number=6, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='abilities', full_name='Card.abilities', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='flavor_text', full_name='Card.flavor_text', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='power', full_name='Card.power', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='toughness', full_name='Card.toughness', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='meta', full_name='Card.meta', index=10,
      number=11, type=11, cpp_type=10, label=3,
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
  oneofs=[
  ],
  serialized_start=537,
  serialized_end=748,
)


_COUNTER = _descriptor.Descriptor(
  name='Counter',
  full_name='Counter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='Counter.type', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=750,
  serialized_end=773,
)


_ABILITY = _descriptor.Descriptor(
  name='Ability',
  full_name='Ability',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ability_on', full_name='Ability.ability_on', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ability_index', full_name='Ability.ability_index', index=1,
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
  oneofs=[
  ],
  serialized_start=775,
  serialized_end=827,
)


_MANAPOOL = _descriptor.Descriptor(
  name='ManaPool',
  full_name='ManaPool',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='white', full_name='ManaPool.white', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='blue', full_name='ManaPool.blue', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='black', full_name='ManaPool.black', index=2,
      number=3, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='red', full_name='ManaPool.red', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='green', full_name='ManaPool.green', index=4,
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
  oneofs=[
  ],
  serialized_start=829,
  serialized_end=911,
)

_GAMESTATE.fields_by_name['game_objects'].message_type = _GAMEOBJECT
_GAMEOBJECT.fields_by_name['game_object_type'].enum_type = _GAMEOBJECT_GAMEOBJECTTYPE
_GAMEOBJECT.fields_by_name['player'].message_type = _PLAYER
_GAMEOBJECT.fields_by_name['zone'].message_type = _ZONE
_GAMEOBJECT.fields_by_name['card'].message_type = _CARD
_GAMEOBJECT.fields_by_name['counter'].message_type = _COUNTER
_GAMEOBJECT.fields_by_name['mana_pool'].message_type = _MANAPOOL
_GAMEOBJECT_GAMEOBJECTTYPE.containing_type = _GAMEOBJECT
_CARD.fields_by_name['meta'].message_type = util_pb2._KEYVALUEPAIR
DESCRIPTOR.message_types_by_name['GameState'] = _GAMESTATE
DESCRIPTOR.message_types_by_name['GameObject'] = _GAMEOBJECT
DESCRIPTOR.message_types_by_name['Player'] = _PLAYER
DESCRIPTOR.message_types_by_name['Zone'] = _ZONE
DESCRIPTOR.message_types_by_name['Card'] = _CARD
DESCRIPTOR.message_types_by_name['Counter'] = _COUNTER
DESCRIPTOR.message_types_by_name['Ability'] = _ABILITY
DESCRIPTOR.message_types_by_name['ManaPool'] = _MANAPOOL

GameState = _reflection.GeneratedProtocolMessageType('GameState', (_message.Message,), dict(
  DESCRIPTOR = _GAMESTATE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:GameState)
  ))
_sym_db.RegisterMessage(GameState)

GameObject = _reflection.GeneratedProtocolMessageType('GameObject', (_message.Message,), dict(
  DESCRIPTOR = _GAMEOBJECT,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:GameObject)
  ))
_sym_db.RegisterMessage(GameObject)

Player = _reflection.GeneratedProtocolMessageType('Player', (_message.Message,), dict(
  DESCRIPTOR = _PLAYER,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:Player)
  ))
_sym_db.RegisterMessage(Player)

Zone = _reflection.GeneratedProtocolMessageType('Zone', (_message.Message,), dict(
  DESCRIPTOR = _ZONE,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:Zone)
  ))
_sym_db.RegisterMessage(Zone)

Card = _reflection.GeneratedProtocolMessageType('Card', (_message.Message,), dict(
  DESCRIPTOR = _CARD,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:Card)
  ))
_sym_db.RegisterMessage(Card)

Counter = _reflection.GeneratedProtocolMessageType('Counter', (_message.Message,), dict(
  DESCRIPTOR = _COUNTER,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:Counter)
  ))
_sym_db.RegisterMessage(Counter)

Ability = _reflection.GeneratedProtocolMessageType('Ability', (_message.Message,), dict(
  DESCRIPTOR = _ABILITY,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:Ability)
  ))
_sym_db.RegisterMessage(Ability)

ManaPool = _reflection.GeneratedProtocolMessageType('ManaPool', (_message.Message,), dict(
  DESCRIPTOR = _MANAPOOL,
  __module__ = 'game_pb2'
  # @@protoc_insertion_point(class_scope:ManaPool)
  ))
_sym_db.RegisterMessage(ManaPool)


# @@protoc_insertion_point(module_scope)
