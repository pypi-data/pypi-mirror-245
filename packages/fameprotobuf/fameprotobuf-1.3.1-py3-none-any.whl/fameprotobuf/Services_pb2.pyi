from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduledTime(_message.Message):
    __slots__ = ["timeStep"]
    TIMESTEP_FIELD_NUMBER: _ClassVar[int]
    timeStep: int
    def __init__(self, timeStep: _Optional[int] = ...) -> None: ...

class ProtoSetup(_message.Message):
    __slots__ = ["outputPath", "agentPackageNames", "messagePackageNames", "portablePackageNames", "outputFilePrefix", "outputFileTimeStamp"]
    OUTPUTPATH_FIELD_NUMBER: _ClassVar[int]
    AGENTPACKAGENAMES_FIELD_NUMBER: _ClassVar[int]
    MESSAGEPACKAGENAMES_FIELD_NUMBER: _ClassVar[int]
    PORTABLEPACKAGENAMES_FIELD_NUMBER: _ClassVar[int]
    OUTPUTFILEPREFIX_FIELD_NUMBER: _ClassVar[int]
    OUTPUTFILETIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    outputPath: str
    agentPackageNames: _containers.RepeatedScalarFieldContainer[str]
    messagePackageNames: _containers.RepeatedScalarFieldContainer[str]
    portablePackageNames: _containers.RepeatedScalarFieldContainer[str]
    outputFilePrefix: str
    outputFileTimeStamp: bool
    def __init__(self, outputPath: _Optional[str] = ..., agentPackageNames: _Optional[_Iterable[str]] = ..., messagePackageNames: _Optional[_Iterable[str]] = ..., portablePackageNames: _Optional[_Iterable[str]] = ..., outputFilePrefix: _Optional[str] = ..., outputFileTimeStamp: bool = ...) -> None: ...

class WarmUpMessage(_message.Message):
    __slots__ = ["needed"]
    NEEDED_FIELD_NUMBER: _ClassVar[int]
    needed: bool
    def __init__(self, needed: bool = ...) -> None: ...

class Output(_message.Message):
    __slots__ = ["agentType", "series"]
    class AgentType(_message.Message):
        __slots__ = ["className", "field"]
        class Field(_message.Message):
            __slots__ = ["fieldId", "fieldName", "indexName"]
            FIELDID_FIELD_NUMBER: _ClassVar[int]
            FIELDNAME_FIELD_NUMBER: _ClassVar[int]
            INDEXNAME_FIELD_NUMBER: _ClassVar[int]
            fieldId: int
            fieldName: str
            indexName: _containers.RepeatedScalarFieldContainer[str]
            def __init__(self, fieldId: _Optional[int] = ..., fieldName: _Optional[str] = ..., indexName: _Optional[_Iterable[str]] = ...) -> None: ...
        CLASSNAME_FIELD_NUMBER: _ClassVar[int]
        FIELD_FIELD_NUMBER: _ClassVar[int]
        className: str
        field: _containers.RepeatedCompositeFieldContainer[Output.AgentType.Field]
        def __init__(self, className: _Optional[str] = ..., field: _Optional[_Iterable[_Union[Output.AgentType.Field, _Mapping]]] = ...) -> None: ...
    class Series(_message.Message):
        __slots__ = ["className", "agentId", "line"]
        class Line(_message.Message):
            __slots__ = ["timeStep", "column"]
            class Column(_message.Message):
                __slots__ = ["fieldId", "value", "entry"]
                class Map(_message.Message):
                    __slots__ = ["indexValue", "value"]
                    INDEXVALUE_FIELD_NUMBER: _ClassVar[int]
                    VALUE_FIELD_NUMBER: _ClassVar[int]
                    indexValue: _containers.RepeatedScalarFieldContainer[str]
                    value: str
                    def __init__(self, indexValue: _Optional[_Iterable[str]] = ..., value: _Optional[str] = ...) -> None: ...
                FIELDID_FIELD_NUMBER: _ClassVar[int]
                VALUE_FIELD_NUMBER: _ClassVar[int]
                ENTRY_FIELD_NUMBER: _ClassVar[int]
                fieldId: int
                value: float
                entry: _containers.RepeatedCompositeFieldContainer[Output.Series.Line.Column.Map]
                def __init__(self, fieldId: _Optional[int] = ..., value: _Optional[float] = ..., entry: _Optional[_Iterable[_Union[Output.Series.Line.Column.Map, _Mapping]]] = ...) -> None: ...
            TIMESTEP_FIELD_NUMBER: _ClassVar[int]
            COLUMN_FIELD_NUMBER: _ClassVar[int]
            timeStep: int
            column: _containers.RepeatedCompositeFieldContainer[Output.Series.Line.Column]
            def __init__(self, timeStep: _Optional[int] = ..., column: _Optional[_Iterable[_Union[Output.Series.Line.Column, _Mapping]]] = ...) -> None: ...
        CLASSNAME_FIELD_NUMBER: _ClassVar[int]
        AGENTID_FIELD_NUMBER: _ClassVar[int]
        LINE_FIELD_NUMBER: _ClassVar[int]
        className: str
        agentId: int
        line: _containers.RepeatedCompositeFieldContainer[Output.Series.Line]
        def __init__(self, className: _Optional[str] = ..., agentId: _Optional[int] = ..., line: _Optional[_Iterable[_Union[Output.Series.Line, _Mapping]]] = ...) -> None: ...
    AGENTTYPE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    agentType: _containers.RepeatedCompositeFieldContainer[Output.AgentType]
    series: _containers.RepeatedCompositeFieldContainer[Output.Series]
    def __init__(self, agentType: _Optional[_Iterable[_Union[Output.AgentType, _Mapping]]] = ..., series: _Optional[_Iterable[_Union[Output.Series, _Mapping]]] = ...) -> None: ...

class AddressBook(_message.Message):
    __slots__ = ["processId", "agentId"]
    PROCESSID_FIELD_NUMBER: _ClassVar[int]
    AGENTID_FIELD_NUMBER: _ClassVar[int]
    processId: int
    agentId: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, processId: _Optional[int] = ..., agentId: _Optional[_Iterable[int]] = ...) -> None: ...
