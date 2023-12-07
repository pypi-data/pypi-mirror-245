from fameprotobuf import Services_pb2 as _Services_pb2
from fameprotobuf import InputFile_pb2 as _InputFile_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataStorage(_message.Message):
    __slots__ = ["input", "output"]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    input: _InputFile_pb2.InputData
    output: _Services_pb2.Output
    def __init__(self, input: _Optional[_Union[_InputFile_pb2.InputData, _Mapping]] = ..., output: _Optional[_Union[_Services_pb2.Output, _Mapping]] = ...) -> None: ...
