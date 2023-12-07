from fameprotobuf import Field_pb2 as _Field_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProtoContract(_message.Message):
    __slots__ = ["senderId", "receiverId", "productName", "firstDeliveryTime", "deliveryIntervalInSteps", "expirationTime", "field", "metadata"]
    SENDERID_FIELD_NUMBER: _ClassVar[int]
    RECEIVERID_FIELD_NUMBER: _ClassVar[int]
    PRODUCTNAME_FIELD_NUMBER: _ClassVar[int]
    FIRSTDELIVERYTIME_FIELD_NUMBER: _ClassVar[int]
    DELIVERYINTERVALINSTEPS_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONTIME_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    senderId: int
    receiverId: int
    productName: str
    firstDeliveryTime: int
    deliveryIntervalInSteps: int
    expirationTime: int
    field: _containers.RepeatedCompositeFieldContainer[_Field_pb2.NestedField]
    metadata: str
    def __init__(self, senderId: _Optional[int] = ..., receiverId: _Optional[int] = ..., productName: _Optional[str] = ..., firstDeliveryTime: _Optional[int] = ..., deliveryIntervalInSteps: _Optional[int] = ..., expirationTime: _Optional[int] = ..., field: _Optional[_Iterable[_Union[_Field_pb2.NestedField, _Mapping]]] = ..., metadata: _Optional[str] = ...) -> None: ...
