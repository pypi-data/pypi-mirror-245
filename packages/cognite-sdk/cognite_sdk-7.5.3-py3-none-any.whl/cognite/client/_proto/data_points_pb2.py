# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: data_points.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x64\x61ta_points.proto\x12\x1f\x63om.cognite.v1.timeseries.proto\"4\n\x10NumericDatapoint\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\x01\"Z\n\x11NumericDatapoints\x12\x45\n\ndatapoints\x18\x01 \x03(\x0b\x32\x31.com.cognite.v1.timeseries.proto.NumericDatapoint\"3\n\x0fStringDatapoint\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\t\"X\n\x10StringDatapoints\x12\x44\n\ndatapoints\x18\x01 \x03(\x0b\x32\x30.com.cognite.v1.timeseries.proto.StringDatapoint\"\xee\x01\n\x12\x41ggregateDatapoint\x12\x11\n\ttimestamp\x18\x01 \x01(\x03\x12\x0f\n\x07\x61verage\x18\x02 \x01(\x01\x12\x0b\n\x03max\x18\x03 \x01(\x01\x12\x0b\n\x03min\x18\x04 \x01(\x01\x12\r\n\x05\x63ount\x18\x05 \x01(\x01\x12\x0b\n\x03sum\x18\x06 \x01(\x01\x12\x15\n\rinterpolation\x18\x07 \x01(\x01\x12\x19\n\x11stepInterpolation\x18\x08 \x01(\x01\x12\x1a\n\x12\x63ontinuousVariance\x18\t \x01(\x01\x12\x18\n\x10\x64iscreteVariance\x18\n \x01(\x01\x12\x16\n\x0etotalVariation\x18\x0b \x01(\x01\"^\n\x13\x41ggregateDatapoints\x12G\n\ndatapoints\x18\x01 \x03(\x0b\x32\x33.com.cognite.v1.timeseries.proto.AggregateDatapointB\x02P\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_points_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'P\001'
  _globals['_NUMERICDATAPOINT']._serialized_start=54
  _globals['_NUMERICDATAPOINT']._serialized_end=106
  _globals['_NUMERICDATAPOINTS']._serialized_start=108
  _globals['_NUMERICDATAPOINTS']._serialized_end=198
  _globals['_STRINGDATAPOINT']._serialized_start=200
  _globals['_STRINGDATAPOINT']._serialized_end=251
  _globals['_STRINGDATAPOINTS']._serialized_start=253
  _globals['_STRINGDATAPOINTS']._serialized_end=341
  _globals['_AGGREGATEDATAPOINT']._serialized_start=344
  _globals['_AGGREGATEDATAPOINT']._serialized_end=582
  _globals['_AGGREGATEDATAPOINTS']._serialized_start=584
  _globals['_AGGREGATEDATAPOINTS']._serialized_end=678
# @@protoc_insertion_point(module_scope)
