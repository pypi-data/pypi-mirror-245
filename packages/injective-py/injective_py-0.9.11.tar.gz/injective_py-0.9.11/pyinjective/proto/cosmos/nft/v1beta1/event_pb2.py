# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/nft/v1beta1/event.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x63osmos/nft/v1beta1/event.proto\x12\x12\x63osmos.nft.v1beta1\"K\n\tEventSend\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\x0e\n\x06sender\x18\x03 \x01(\t\x12\x10\n\x08receiver\x18\x04 \x01(\t\"8\n\tEventMint\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\r\n\x05owner\x18\x03 \x01(\t\"8\n\tEventBurn\x12\x10\n\x08\x63lass_id\x18\x01 \x01(\t\x12\n\n\x02id\x18\x02 \x01(\t\x12\r\n\x05owner\x18\x03 \x01(\tB$Z\"github.com/cosmos/cosmos-sdk/x/nftb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.nft.v1beta1.event_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\"github.com/cosmos/cosmos-sdk/x/nft'
  _EVENTSEND._serialized_start=54
  _EVENTSEND._serialized_end=129
  _EVENTMINT._serialized_start=131
  _EVENTMINT._serialized_end=187
  _EVENTBURN._serialized_start=189
  _EVENTBURN._serialized_end=245
# @@protoc_insertion_point(module_scope)
