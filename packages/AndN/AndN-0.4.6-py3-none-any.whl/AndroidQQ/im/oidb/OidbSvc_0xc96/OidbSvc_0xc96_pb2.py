# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AndroidQQ/im/oidb/OidbSvc_0xc96/OidbSvc_0xc96.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n3AndroidQQ/im/oidb/OidbSvc_0xc96/OidbSvc_0xc96.proto\x12\x18tencent.im.oidb.cmd0xc96\" \n\tFollowExt\x12\x13\n\x0bsource_from\x18\x01 \x01(\r\"=\n\tFollowReq\x12\x30\n\x03\x65xt\x18\x01 \x01(\x0b\x32#.tencent.im.oidb.cmd0xc96.FollowExt\"\"\n\x0bUnFollowExt\x12\x13\n\x0bsource_from\x18\x01 \x01(\r\"A\n\x0bUnfollowReq\x12\x32\n\x03\x65xt\x18\x01 \x01(\x0b\x32%.tencent.im.oidb.cmd0xc96.UnFollowExt\"\x12\n\x10GetFollowInfoReq\"$\n\x11MGetFollowInfoReq\x12\x0f\n\x07openids\x18\x01 \x03(\t\"\xd4\x02\n\x07ReqBody\x12\r\n\x05\x61ppid\x18\x01 \x01(\x04\x12\x10\n\x08\x61pp_type\x18\x02 \x01(\r\x12\x0c\n\x04puin\x18\x03 \x01(\x04\x12\x10\n\x08\x63md_type\x18\x04 \x01(\r\x12\x37\n\nfollow_req\x18\x0b \x01(\x0b\x32#.tencent.im.oidb.cmd0xc96.FollowReq\x12;\n\x0cunfollow_req\x18\x0c \x01(\x0b\x32%.tencent.im.oidb.cmd0xc96.UnfollowReq\x12G\n\x13get_follow_info_req\x18\r \x01(\x0b\x32*.tencent.im.oidb.cmd0xc96.GetFollowInfoReq\x12I\n\x14mget_follow_info_req\x18\x0e \x01(\x0b\x32+.tencent.im.oidb.cmd0xc96.MGetFollowInfoReq\";\n\x07RspBody\x12\x0f\n\x07wording\x18\x01 \x01(\t\x12\r\n\x05\x61ppid\x18\x03 \x01(\x04\x12\x10\n\x08\x61pp_type\x18\x04 \x01(\x04')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'AndroidQQ.im.oidb.OidbSvc_0xc96.OidbSvc_0xc96_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FOLLOWEXT']._serialized_start=81
  _globals['_FOLLOWEXT']._serialized_end=113
  _globals['_FOLLOWREQ']._serialized_start=115
  _globals['_FOLLOWREQ']._serialized_end=176
  _globals['_UNFOLLOWEXT']._serialized_start=178
  _globals['_UNFOLLOWEXT']._serialized_end=212
  _globals['_UNFOLLOWREQ']._serialized_start=214
  _globals['_UNFOLLOWREQ']._serialized_end=279
  _globals['_GETFOLLOWINFOREQ']._serialized_start=281
  _globals['_GETFOLLOWINFOREQ']._serialized_end=299
  _globals['_MGETFOLLOWINFOREQ']._serialized_start=301
  _globals['_MGETFOLLOWINFOREQ']._serialized_end=337
  _globals['_REQBODY']._serialized_start=340
  _globals['_REQBODY']._serialized_end=680
  _globals['_RSPBODY']._serialized_start=682
  _globals['_RSPBODY']._serialized_end=741
# @@protoc_insertion_point(module_scope)
