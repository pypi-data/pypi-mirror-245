from fameprotobuf import AgentMessage_pb2 as _AgentMessage_pb2
from fameprotobuf import Services_pb2 as _Services_pb2
from fameprotobuf import InputFile_pb2 as _InputFile_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MpiMessage(_message.Message):
    __slots__ = ["scheduledTime", "warmUp", "addressBook", "input", "output", "message", "setup"]
    SCHEDULEDTIME_FIELD_NUMBER: _ClassVar[int]
    WARMUP_FIELD_NUMBER: _ClassVar[int]
    ADDRESSBOOK_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SETUP_FIELD_NUMBER: _ClassVar[int]
    scheduledTime: _Services_pb2.ScheduledTime
    warmUp: _Services_pb2.WarmUpMessage
    addressBook: _Services_pb2.AddressBook
    input: _InputFile_pb2.InputData
    output: _Services_pb2.Output
    message: _AgentMessage_pb2.ProtoMessage
    setup: _Services_pb2.ProtoSetup
    def __init__(self, scheduledTime: _Optional[_Union[_Services_pb2.ScheduledTime, _Mapping]] = ..., warmUp: _Optional[_Union[_Services_pb2.WarmUpMessage, _Mapping]] = ..., addressBook: _Optional[_Union[_Services_pb2.AddressBook, _Mapping]] = ..., input: _Optional[_Union[_InputFile_pb2.InputData, _Mapping]] = ..., output: _Optional[_Union[_Services_pb2.Output, _Mapping]] = ..., message: _Optional[_Union[_AgentMessage_pb2.ProtoMessage, _Mapping]] = ..., setup: _Optional[_Union[_Services_pb2.ProtoSetup, _Mapping]] = ...) -> None: ...

class Bundle(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: _containers.RepeatedCompositeFieldContainer[MpiMessage]
    def __init__(self, message: _Optional[_Iterable[_Union[MpiMessage, _Mapping]]] = ...) -> None: ...
