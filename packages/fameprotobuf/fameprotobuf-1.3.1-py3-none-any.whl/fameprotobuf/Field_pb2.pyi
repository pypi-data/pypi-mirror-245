from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NestedField(_message.Message):
    __slots__ = ["fieldName", "seriesId", "intValue", "stringValue", "doubleValue", "field", "longValue"]
    FIELDNAME_FIELD_NUMBER: _ClassVar[int]
    SERIESID_FIELD_NUMBER: _ClassVar[int]
    INTVALUE_FIELD_NUMBER: _ClassVar[int]
    STRINGVALUE_FIELD_NUMBER: _ClassVar[int]
    DOUBLEVALUE_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    LONGVALUE_FIELD_NUMBER: _ClassVar[int]
    fieldName: str
    seriesId: int
    intValue: _containers.RepeatedScalarFieldContainer[int]
    stringValue: _containers.RepeatedScalarFieldContainer[str]
    doubleValue: _containers.RepeatedScalarFieldContainer[float]
    field: _containers.RepeatedCompositeFieldContainer[NestedField]
    longValue: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, fieldName: _Optional[str] = ..., seriesId: _Optional[int] = ..., intValue: _Optional[_Iterable[int]] = ..., stringValue: _Optional[_Iterable[str]] = ..., doubleValue: _Optional[_Iterable[float]] = ..., field: _Optional[_Iterable[_Union[NestedField, _Mapping]]] = ..., longValue: _Optional[_Iterable[int]] = ...) -> None: ...
