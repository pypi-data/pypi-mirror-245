# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Services.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eServices.proto\x12\rcommunication\"!\n\rScheduledTime\x12\x10\n\x08timeStep\x18\x01 \x02(\x03\"\xad\x01\n\nProtoSetup\x12\x12\n\noutputPath\x18\x01 \x02(\t\x12\x19\n\x11\x61gentPackageNames\x18\x02 \x03(\t\x12\x1b\n\x13messagePackageNames\x18\x03 \x03(\t\x12\x1c\n\x14portablePackageNames\x18\x04 \x03(\t\x12\x18\n\x10outputFilePrefix\x18\x05 \x01(\t\x12\x1b\n\x13outputFileTimeStamp\x18\x06 \x01(\x08\"\x1f\n\rWarmUpMessage\x12\x0e\n\x06needed\x18\x01 \x02(\x08\"\xc8\x04\n\x06Output\x12\x32\n\tagentType\x18\x01 \x03(\x0b\x32\x1f.communication.Output.AgentType\x12,\n\x06series\x18\x02 \x03(\x0b\x32\x1c.communication.Output.Series\x1a\x94\x01\n\tAgentType\x12\x11\n\tclassName\x18\x01 \x02(\t\x12\x34\n\x05\x66ield\x18\x02 \x03(\x0b\x32%.communication.Output.AgentType.Field\x1a>\n\x05\x46ield\x12\x0f\n\x07\x66ieldId\x18\x01 \x02(\x05\x12\x11\n\tfieldName\x18\x02 \x02(\t\x12\x11\n\tindexName\x18\x03 \x03(\t\x1a\xc4\x02\n\x06Series\x12\x11\n\tclassName\x18\x01 \x02(\t\x12\x0f\n\x07\x61gentId\x18\x02 \x02(\x03\x12/\n\x04line\x18\x03 \x03(\x0b\x32!.communication.Output.Series.Line\x1a\xe4\x01\n\x04Line\x12\x10\n\x08timeStep\x18\x01 \x02(\x03\x12\x38\n\x06\x63olumn\x18\x02 \x03(\x0b\x32(.communication.Output.Series.Line.Column\x1a\x8f\x01\n\x06\x43olumn\x12\x0f\n\x07\x66ieldId\x18\x01 \x02(\x05\x12\r\n\x05value\x18\x02 \x01(\x01\x12;\n\x05\x65ntry\x18\x03 \x03(\x0b\x32,.communication.Output.Series.Line.Column.Map\x1a(\n\x03Map\x12\x12\n\nindexValue\x18\x01 \x03(\t\x12\r\n\x05value\x18\x02 \x02(\t\"1\n\x0b\x41\x64\x64ressBook\x12\x11\n\tprocessId\x18\x01 \x02(\x05\x12\x0f\n\x07\x61gentId\x18\x02 \x03(\x03\x42\'\n\x1b\x64\x65.dlr.gitlab.fame.protobufB\x08Services')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Services_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\033de.dlr.gitlab.fame.protobufB\010Services'
  _globals['_SCHEDULEDTIME']._serialized_start=33
  _globals['_SCHEDULEDTIME']._serialized_end=66
  _globals['_PROTOSETUP']._serialized_start=69
  _globals['_PROTOSETUP']._serialized_end=242
  _globals['_WARMUPMESSAGE']._serialized_start=244
  _globals['_WARMUPMESSAGE']._serialized_end=275
  _globals['_OUTPUT']._serialized_start=278
  _globals['_OUTPUT']._serialized_end=862
  _globals['_OUTPUT_AGENTTYPE']._serialized_start=387
  _globals['_OUTPUT_AGENTTYPE']._serialized_end=535
  _globals['_OUTPUT_AGENTTYPE_FIELD']._serialized_start=473
  _globals['_OUTPUT_AGENTTYPE_FIELD']._serialized_end=535
  _globals['_OUTPUT_SERIES']._serialized_start=538
  _globals['_OUTPUT_SERIES']._serialized_end=862
  _globals['_OUTPUT_SERIES_LINE']._serialized_start=634
  _globals['_OUTPUT_SERIES_LINE']._serialized_end=862
  _globals['_OUTPUT_SERIES_LINE_COLUMN']._serialized_start=719
  _globals['_OUTPUT_SERIES_LINE_COLUMN']._serialized_end=862
  _globals['_OUTPUT_SERIES_LINE_COLUMN_MAP']._serialized_start=822
  _globals['_OUTPUT_SERIES_LINE_COLUMN_MAP']._serialized_end=862
  _globals['_ADDRESSBOOK']._serialized_start=864
  _globals['_ADDRESSBOOK']._serialized_end=913
# @@protoc_insertion_point(module_scope)
