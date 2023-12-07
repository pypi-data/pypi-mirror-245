# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: injective/auction/v1beta1/query.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from injective.auction.v1beta1 import auction_pb2 as injective_dot_auction_dot_v1beta1_dot_auction__pb2
from injective.auction.v1beta1 import genesis_pb2 as injective_dot_auction_dot_v1beta1_dot_genesis__pb2
from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from cosmos.base.v1beta1 import coin_pb2 as cosmos_dot_base_dot_v1beta1_dot_coin__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%injective/auction/v1beta1/query.proto\x12\x19injective.auction.v1beta1\x1a\x1cgoogle/api/annotations.proto\x1a\'injective/auction/v1beta1/auction.proto\x1a\'injective/auction/v1beta1/genesis.proto\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/base/v1beta1/coin.proto\"\x1b\n\x19QueryAuctionParamsRequest\"U\n\x1aQueryAuctionParamsResponse\x12\x37\n\x06params\x18\x01 \x01(\x0b\x32!.injective.auction.v1beta1.ParamsB\x04\xc8\xde\x1f\x00\"\"\n QueryCurrentAuctionBasketRequest\"\x93\x02\n!QueryCurrentAuctionBasketResponse\x12[\n\x06\x61mount\x18\x01 \x03(\x0b\x32\x19.cosmos.base.v1beta1.CoinB0\xaa\xdf\x1f(github.com/cosmos/cosmos-sdk/types.Coins\xc8\xde\x1f\x00\x12\x14\n\x0c\x61uctionRound\x18\x02 \x01(\x04\x12\x1a\n\x12\x61uctionClosingTime\x18\x03 \x01(\x03\x12\x15\n\rhighestBidder\x18\x04 \x01(\t\x12H\n\x10highestBidAmount\x18\x05 \x01(\tB.\xda\xde\x1f&github.com/cosmos/cosmos-sdk/types.Int\xc8\xde\x1f\x00\"\x19\n\x17QueryModuleStateRequest\"R\n\x18QueryModuleStateResponse\x12\x36\n\x05state\x18\x01 \x01(\x0b\x32\'.injective.auction.v1beta1.GenesisState2\xa1\x04\n\x05Query\x12\xa7\x01\n\rAuctionParams\x12\x34.injective.auction.v1beta1.QueryAuctionParamsRequest\x1a\x35.injective.auction.v1beta1.QueryAuctionParamsResponse\")\x82\xd3\xe4\x93\x02#\x12!/injective/auction/v1beta1/params\x12\xbc\x01\n\x14\x43urrentAuctionBasket\x12;.injective.auction.v1beta1.QueryCurrentAuctionBasketRequest\x1a<.injective.auction.v1beta1.QueryCurrentAuctionBasketResponse\")\x82\xd3\xe4\x93\x02#\x12!/injective/auction/v1beta1/basket\x12\xae\x01\n\x12\x41uctionModuleState\x12\x32.injective.auction.v1beta1.QueryModuleStateRequest\x1a\x33.injective.auction.v1beta1.QueryModuleStateResponse\"/\x82\xd3\xe4\x93\x02)\x12\'/injective/auction/v1beta1/module_stateBOZMgithub.com/InjectiveLabs/injective-core/injective-chain/modules/auction/typesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'injective.auction.v1beta1.query_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'ZMgithub.com/InjectiveLabs/injective-core/injective-chain/modules/auction/types'
  _QUERYAUCTIONPARAMSRESPONSE.fields_by_name['params']._options = None
  _QUERYAUCTIONPARAMSRESPONSE.fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _QUERYCURRENTAUCTIONBASKETRESPONSE.fields_by_name['amount']._options = None
  _QUERYCURRENTAUCTIONBASKETRESPONSE.fields_by_name['amount']._serialized_options = b'\252\337\037(github.com/cosmos/cosmos-sdk/types.Coins\310\336\037\000'
  _QUERYCURRENTAUCTIONBASKETRESPONSE.fields_by_name['highestBidAmount']._options = None
  _QUERYCURRENTAUCTIONBASKETRESPONSE.fields_by_name['highestBidAmount']._serialized_options = b'\332\336\037&github.com/cosmos/cosmos-sdk/types.Int\310\336\037\000'
  _QUERY.methods_by_name['AuctionParams']._options = None
  _QUERY.methods_by_name['AuctionParams']._serialized_options = b'\202\323\344\223\002#\022!/injective/auction/v1beta1/params'
  _QUERY.methods_by_name['CurrentAuctionBasket']._options = None
  _QUERY.methods_by_name['CurrentAuctionBasket']._serialized_options = b'\202\323\344\223\002#\022!/injective/auction/v1beta1/basket'
  _QUERY.methods_by_name['AuctionModuleState']._options = None
  _QUERY.methods_by_name['AuctionModuleState']._serialized_options = b'\202\323\344\223\002)\022\'/injective/auction/v1beta1/module_state'
  _QUERYAUCTIONPARAMSREQUEST._serialized_start=234
  _QUERYAUCTIONPARAMSREQUEST._serialized_end=261
  _QUERYAUCTIONPARAMSRESPONSE._serialized_start=263
  _QUERYAUCTIONPARAMSRESPONSE._serialized_end=348
  _QUERYCURRENTAUCTIONBASKETREQUEST._serialized_start=350
  _QUERYCURRENTAUCTIONBASKETREQUEST._serialized_end=384
  _QUERYCURRENTAUCTIONBASKETRESPONSE._serialized_start=387
  _QUERYCURRENTAUCTIONBASKETRESPONSE._serialized_end=662
  _QUERYMODULESTATEREQUEST._serialized_start=664
  _QUERYMODULESTATEREQUEST._serialized_end=689
  _QUERYMODULESTATERESPONSE._serialized_start=691
  _QUERYMODULESTATERESPONSE._serialized_end=773
  _QUERY._serialized_start=776
  _QUERY._serialized_end=1321
# @@protoc_insertion_point(module_scope)
