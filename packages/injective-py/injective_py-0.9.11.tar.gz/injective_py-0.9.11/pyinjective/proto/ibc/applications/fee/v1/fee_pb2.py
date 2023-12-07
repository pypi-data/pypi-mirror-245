# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ibc/applications/fee/v1/fee.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2
from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ibc.core.channel.v1 import channel_pb2 as ibc_dot_core_dot_channel_dot_v1_dot_channel__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!ibc/applications/fee/v1/fee.proto\x12\x17ibc.applications.fee.v1\x1a\x1e\x63osmos/base/v1beta1/coin.proto\x1a\x14gogoproto/gogo.proto\x1a!ibc/core/channel/v1/channel.proto\"\xa4\x02\n\x03\x46\x65\x65\x12]\n\x08recv_fee\x18\x01 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12\\\n\x07\x61\x63k_fee\x18\x02 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\x12`\n\x0btimeout_fee\x18\x03 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB0\xc8\xde\x1f\x00\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\"f\n\tPacketFee\x12/\n\x03\x66\x65\x65\x18\x01 \x01(\x0b\x32\x1c.ibc.applications.fee.v1.FeeB\x04\xc8\xde\x1f\x00\x12\x16\n\x0erefund_address\x18\x02 \x01(\t\x12\x10\n\x08relayers\x18\x03 \x03(\t\"K\n\nPacketFees\x12=\n\x0bpacket_fees\x18\x01 \x03(\x0b\x32\".ibc.applications.fee.v1.PacketFeeB\x04\xc8\xde\x1f\x00\"\x8d\x01\n\x14IdentifiedPacketFees\x12\x36\n\tpacket_id\x18\x01 \x01(\x0b\x32\x1d.ibc.core.channel.v1.PacketIdB\x04\xc8\xde\x1f\x00\x12=\n\x0bpacket_fees\x18\x02 \x03(\x0b\x32\".ibc.applications.fee.v1.PacketFeeB\x04\xc8\xde\x1f\x00\x42\x37Z5github.com/cosmos/ibc-go/v7/modules/apps/29-fee/typesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ibc.applications.fee.v1.fee_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z5github.com/cosmos/ibc-go/v7/modules/apps/29-fee/types'
  _FEE.fields_by_name['recv_fee']._options = None
  _FEE.fields_by_name['recv_fee']._serialized_options = b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins'
  _FEE.fields_by_name['ack_fee']._options = None
  _FEE.fields_by_name['ack_fee']._serialized_options = b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins'
  _FEE.fields_by_name['timeout_fee']._options = None
  _FEE.fields_by_name['timeout_fee']._serialized_options = b'\310\336\037\000\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins'
  _PACKETFEE.fields_by_name['fee']._options = None
  _PACKETFEE.fields_by_name['fee']._serialized_options = b'\310\336\037\000'
  _PACKETFEES.fields_by_name['packet_fees']._options = None
  _PACKETFEES.fields_by_name['packet_fees']._serialized_options = b'\310\336\037\000'
  _IDENTIFIEDPACKETFEES.fields_by_name['packet_id']._options = None
  _IDENTIFIEDPACKETFEES.fields_by_name['packet_id']._serialized_options = b'\310\336\037\000'
  _IDENTIFIEDPACKETFEES.fields_by_name['packet_fees']._options = None
  _IDENTIFIEDPACKETFEES.fields_by_name['packet_fees']._serialized_options = b'\310\336\037\000'
  _FEE._serialized_start=152
  _FEE._serialized_end=444
  _PACKETFEE._serialized_start=446
  _PACKETFEE._serialized_end=548
  _PACKETFEES._serialized_start=550
  _PACKETFEES._serialized_end=625
  _IDENTIFIEDPACKETFEES._serialized_start=628
  _IDENTIFIEDPACKETFEES._serialized_end=769
# @@protoc_insertion_point(module_scope)
