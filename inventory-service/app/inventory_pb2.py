# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: inventory.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0finventory.proto\"e\n\rInventoryItem\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x12\n\nproduct_id\x18\x02 \x01(\x05\x12\x12\n\nvariant_id\x18\x03 \x01(\x05\x12\x10\n\x08quantity\x18\x04 \x01(\x05\x12\x0e\n\x06status\x18\x05 \x01(\t*3\n\rOperationType\x12\n\n\x06\x43REATE\x10\x00\x12\n\n\x06UPDATE\x10\x01\x12\n\n\x06\x44\x45LETE\x10\x02\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'inventory_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_OPERATIONTYPE']._serialized_start=122
  _globals['_OPERATIONTYPE']._serialized_end=173
  _globals['_INVENTORYITEM']._serialized_start=19
  _globals['_INVENTORYITEM']._serialized_end=120
# @@protoc_insertion_point(module_scope)
