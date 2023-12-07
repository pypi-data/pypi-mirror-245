from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoDataItem(_message.Message):
    __slots__ = ["dataTypeId", "boolValue", "intValue", "longValue", "floatValue", "doubleValue", "stringValue"]
    DATATYPEID_FIELD_NUMBER: _ClassVar[int]
    BOOLVALUE_FIELD_NUMBER: _ClassVar[int]
    INTVALUE_FIELD_NUMBER: _ClassVar[int]
    LONGVALUE_FIELD_NUMBER: _ClassVar[int]
    FLOATVALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLEVALUE_FIELD_NUMBER: _ClassVar[int]
    STRINGVALUE_FIELD_NUMBER: _ClassVar[int]
    dataTypeId: int
    boolValue: _containers.RepeatedScalarFieldContainer[bool]
    intValue: _containers.RepeatedScalarFieldContainer[int]
    longValue: _containers.RepeatedScalarFieldContainer[int]
    floatValue: _containers.RepeatedScalarFieldContainer[float]
    doubleValue: _containers.RepeatedScalarFieldContainer[float]
    stringValue: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dataTypeId: _Optional[int] = ..., boolValue: _Optional[_Iterable[bool]] = ..., intValue: _Optional[_Iterable[int]] = ..., longValue: _Optional[_Iterable[int]] = ..., floatValue: _Optional[_Iterable[float]] = ..., doubleValue: _Optional[_Iterable[float]] = ..., stringValue: _Optional[_Iterable[str]] = ...) -> None: ...

class NestedItem(_message.Message):
    __slots__ = ["dataTypeId", "boolValue", "intValue", "longValue", "floatValue", "doubleValue", "stringValue", "timeSeriesId", "component"]
    DATATYPEID_FIELD_NUMBER: _ClassVar[int]
    BOOLVALUE_FIELD_NUMBER: _ClassVar[int]
    INTVALUE_FIELD_NUMBER: _ClassVar[int]
    LONGVALUE_FIELD_NUMBER: _ClassVar[int]
    FLOATVALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLEVALUE_FIELD_NUMBER: _ClassVar[int]
    STRINGVALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESERIESID_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_FIELD_NUMBER: _ClassVar[int]
    dataTypeId: int
    boolValue: _containers.RepeatedScalarFieldContainer[bool]
    intValue: _containers.RepeatedScalarFieldContainer[int]
    longValue: _containers.RepeatedScalarFieldContainer[int]
    floatValue: _containers.RepeatedScalarFieldContainer[float]
    doubleValue: _containers.RepeatedScalarFieldContainer[float]
    stringValue: _containers.RepeatedScalarFieldContainer[str]
    timeSeriesId: _containers.RepeatedScalarFieldContainer[int]
    component: _containers.RepeatedCompositeFieldContainer[NestedItem]
    def __init__(self, dataTypeId: _Optional[int] = ..., boolValue: _Optional[_Iterable[bool]] = ..., intValue: _Optional[_Iterable[int]] = ..., longValue: _Optional[_Iterable[int]] = ..., floatValue: _Optional[_Iterable[float]] = ..., doubleValue: _Optional[_Iterable[float]] = ..., stringValue: _Optional[_Iterable[str]] = ..., timeSeriesId: _Optional[_Iterable[int]] = ..., component: _Optional[_Iterable[_Union[NestedItem, _Mapping]]] = ...) -> None: ...

class ProtoMessage(_message.Message):
    __slots__ = ["senderId", "receiverId", "dataItem", "nestedItem"]
    SENDERID_FIELD_NUMBER: _ClassVar[int]
    RECEIVERID_FIELD_NUMBER: _ClassVar[int]
    DATAITEM_FIELD_NUMBER: _ClassVar[int]
    NESTEDITEM_FIELD_NUMBER: _ClassVar[int]
    senderId: int
    receiverId: int
    dataItem: _containers.RepeatedCompositeFieldContainer[ProtoDataItem]
    nestedItem: _containers.RepeatedCompositeFieldContainer[NestedItem]
    def __init__(self, senderId: _Optional[int] = ..., receiverId: _Optional[int] = ..., dataItem: _Optional[_Iterable[_Union[ProtoDataItem, _Mapping]]] = ..., nestedItem: _Optional[_Iterable[_Union[NestedItem, _Mapping]]] = ...) -> None: ...
