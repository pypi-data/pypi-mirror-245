# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ibc/applications/fee/v1/tx.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from ibc.applications.fee.v1 import fee_pb2 as ibc_dot_applications_dot_fee_dot_v1_dot_fee__pb2
from ibc.core.channel.v1 import channel_pb2 as ibc_dot_core_dot_channel_dot_v1_dot_channel__pb2
from cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n ibc/applications/fee/v1/tx.proto\x12\x17ibc.applications.fee.v1\x1a\x14gogoproto/gogo.proto\x1a!ibc/applications/fee/v1/fee.proto\x1a!ibc/core/channel/v1/channel.proto\x1a\x17\x63osmos/msg/v1/msg.proto\"m\n\x10MsgRegisterPayee\x12\x0f\n\x07port_id\x18\x01 \x01(\t\x12\x12\n\nchannel_id\x18\x02 \x01(\t\x12\x0f\n\x07relayer\x18\x03 \x01(\t\x12\r\n\x05payee\x18\x04 \x01(\t:\x14\x82\xe7\xb0*\x07relayer\xe8\xa0\x1f\x00\x88\xa0\x1f\x00\"\x1a\n\x18MsgRegisterPayeeResponse\"\x86\x01\n\x1cMsgRegisterCounterpartyPayee\x12\x0f\n\x07port_id\x18\x01 \x01(\t\x12\x12\n\nchannel_id\x18\x02 \x01(\t\x12\x0f\n\x07relayer\x18\x03 \x01(\t\x12\x1a\n\x12\x63ounterparty_payee\x18\x04 \x01(\t:\x14\x82\xe7\xb0*\x07relayer\xe8\xa0\x1f\x00\x88\xa0\x1f\x00\"&\n$MsgRegisterCounterpartyPayeeResponse\"\xac\x01\n\x0fMsgPayPacketFee\x12/\n\x03\x66\x65\x65\x18\x01 \x01(\x0b\x32\x1c.ibc.applications.fee.v1.FeeB\x04\xc8\xde\x1f\x00\x12\x16\n\x0esource_port_id\x18\x02 \x01(\t\x12\x19\n\x11source_channel_id\x18\x03 \x01(\t\x12\x0e\n\x06signer\x18\x04 \x01(\t\x12\x10\n\x08relayers\x18\x05 \x03(\t:\x13\x82\xe7\xb0*\x06signer\xe8\xa0\x1f\x00\x88\xa0\x1f\x00\"\x19\n\x17MsgPayPacketFeeResponse\"\xb3\x01\n\x14MsgPayPacketFeeAsync\x12\x36\n\tpacket_id\x18\x01 \x01(\x0b\x32\x1d.ibc.core.channel.v1.PacketIdB\x04\xc8\xde\x1f\x00\x12<\n\npacket_fee\x18\x02 \x01(\x0b\x32\".ibc.applications.fee.v1.PacketFeeB\x04\xc8\xde\x1f\x00:%\x82\xe7\xb0*\x18packet_fee.refundaddress\xe8\xa0\x1f\x00\x88\xa0\x1f\x00\"\x1e\n\x1cMsgPayPacketFeeAsyncResponse2\xf6\x03\n\x03Msg\x12m\n\rRegisterPayee\x12).ibc.applications.fee.v1.MsgRegisterPayee\x1a\x31.ibc.applications.fee.v1.MsgRegisterPayeeResponse\x12\x91\x01\n\x19RegisterCounterpartyPayee\x12\x35.ibc.applications.fee.v1.MsgRegisterCounterpartyPayee\x1a=.ibc.applications.fee.v1.MsgRegisterCounterpartyPayeeResponse\x12j\n\x0cPayPacketFee\x12(.ibc.applications.fee.v1.MsgPayPacketFee\x1a\x30.ibc.applications.fee.v1.MsgPayPacketFeeResponse\x12y\n\x11PayPacketFeeAsync\x12-.ibc.applications.fee.v1.MsgPayPacketFeeAsync\x1a\x35.ibc.applications.fee.v1.MsgPayPacketFeeAsyncResponse\x1a\x05\x80\xe7\xb0*\x01\x42\x37Z5github.com/cosmos/ibc-go/v7/modules/apps/29-fee/typesb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ibc.applications.fee.v1.tx_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z5github.com/cosmos/ibc-go/v7/modules/apps/29-fee/types'
  _MSGREGISTERPAYEE._options = None
  _MSGREGISTERPAYEE._serialized_options = b'\202\347\260*\007relayer\350\240\037\000\210\240\037\000'
  _MSGREGISTERCOUNTERPARTYPAYEE._options = None
  _MSGREGISTERCOUNTERPARTYPAYEE._serialized_options = b'\202\347\260*\007relayer\350\240\037\000\210\240\037\000'
  _MSGPAYPACKETFEE.fields_by_name['fee']._options = None
  _MSGPAYPACKETFEE.fields_by_name['fee']._serialized_options = b'\310\336\037\000'
  _MSGPAYPACKETFEE._options = None
  _MSGPAYPACKETFEE._serialized_options = b'\202\347\260*\006signer\350\240\037\000\210\240\037\000'
  _MSGPAYPACKETFEEASYNC.fields_by_name['packet_id']._options = None
  _MSGPAYPACKETFEEASYNC.fields_by_name['packet_id']._serialized_options = b'\310\336\037\000'
  _MSGPAYPACKETFEEASYNC.fields_by_name['packet_fee']._options = None
  _MSGPAYPACKETFEEASYNC.fields_by_name['packet_fee']._serialized_options = b'\310\336\037\000'
  _MSGPAYPACKETFEEASYNC._options = None
  _MSGPAYPACKETFEEASYNC._serialized_options = b'\202\347\260*\030packet_fee.refundaddress\350\240\037\000\210\240\037\000'
  _MSG._options = None
  _MSG._serialized_options = b'\200\347\260*\001'
  _MSGREGISTERPAYEE._serialized_start=178
  _MSGREGISTERPAYEE._serialized_end=287
  _MSGREGISTERPAYEERESPONSE._serialized_start=289
  _MSGREGISTERPAYEERESPONSE._serialized_end=315
  _MSGREGISTERCOUNTERPARTYPAYEE._serialized_start=318
  _MSGREGISTERCOUNTERPARTYPAYEE._serialized_end=452
  _MSGREGISTERCOUNTERPARTYPAYEERESPONSE._serialized_start=454
  _MSGREGISTERCOUNTERPARTYPAYEERESPONSE._serialized_end=492
  _MSGPAYPACKETFEE._serialized_start=495
  _MSGPAYPACKETFEE._serialized_end=667
  _MSGPAYPACKETFEERESPONSE._serialized_start=669
  _MSGPAYPACKETFEERESPONSE._serialized_end=694
  _MSGPAYPACKETFEEASYNC._serialized_start=697
  _MSGPAYPACKETFEEASYNC._serialized_end=876
  _MSGPAYPACKETFEEASYNCRESPONSE._serialized_start=878
  _MSGPAYPACKETFEEASYNCRESPONSE._serialized_end=908
  _MSG._serialized_start=911
  _MSG._serialized_end=1413
# @@protoc_insertion_point(module_scope)
