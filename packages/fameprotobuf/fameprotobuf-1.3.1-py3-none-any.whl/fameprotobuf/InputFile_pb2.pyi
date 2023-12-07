from fameprotobuf import Contract_pb2 as _Contract_pb2
from fameprotobuf import Field_pb2 as _Field_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InputData(_message.Message):
    __slots__ = ["runId", "simulation", "output", "timeSeries", "agent", "contract", "schema"]
    class SimulationParam(_message.Message):
        __slots__ = ["startTime", "stopTime", "randomSeed"]
        STARTTIME_FIELD_NUMBER: _ClassVar[int]
        STOPTIME_FIELD_NUMBER: _ClassVar[int]
        RANDOMSEED_FIELD_NUMBER: _ClassVar[int]
        startTime: int
        stopTime: int
        randomSeed: int
        def __init__(self, startTime: _Optional[int] = ..., stopTime: _Optional[int] = ..., randomSeed: _Optional[int] = ...) -> None: ...
    class OutputParam(_message.Message):
        __slots__ = ["interval", "process", "activeClassName"]
        INTERVAL_FIELD_NUMBER: _ClassVar[int]
        PROCESS_FIELD_NUMBER: _ClassVar[int]
        ACTIVECLASSNAME_FIELD_NUMBER: _ClassVar[int]
        interval: int
        process: int
        activeClassName: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, interval: _Optional[int] = ..., process: _Optional[int] = ..., activeClassName: _Optional[_Iterable[str]] = ...) -> None: ...
    class TimeSeriesDao(_message.Message):
        __slots__ = ["seriesId", "seriesName", "row"]
        class Row(_message.Message):
            __slots__ = ["timeStep", "value"]
            TIMESTEP_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            timeStep: int
            value: float
            def __init__(self, timeStep: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
        SERIESID_FIELD_NUMBER: _ClassVar[int]
        SERIESNAME_FIELD_NUMBER: _ClassVar[int]
        ROW_FIELD_NUMBER: _ClassVar[int]
        seriesId: int
        seriesName: str
        row: _containers.RepeatedCompositeFieldContainer[InputData.TimeSeriesDao.Row]
        def __init__(self, seriesId: _Optional[int] = ..., seriesName: _Optional[str] = ..., row: _Optional[_Iterable[_Union[InputData.TimeSeriesDao.Row, _Mapping]]] = ...) -> None: ...
    class AgentDao(_message.Message):
        __slots__ = ["id", "className", "field", "metadata"]
        ID_FIELD_NUMBER: _ClassVar[int]
        CLASSNAME_FIELD_NUMBER: _ClassVar[int]
        FIELD_FIELD_NUMBER: _ClassVar[int]
        METADATA_FIELD_NUMBER: _ClassVar[int]
        id: int
        className: str
        field: _containers.RepeatedCompositeFieldContainer[_Field_pb2.NestedField]
        metadata: str
        def __init__(self, id: _Optional[int] = ..., className: _Optional[str] = ..., field: _Optional[_Iterable[_Union[_Field_pb2.NestedField, _Mapping]]] = ..., metadata: _Optional[str] = ...) -> None: ...
    RUNID_FIELD_NUMBER: _ClassVar[int]
    SIMULATION_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TIMESERIES_FIELD_NUMBER: _ClassVar[int]
    AGENT_FIELD_NUMBER: _ClassVar[int]
    CONTRACT_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    runId: int
    simulation: InputData.SimulationParam
    output: InputData.OutputParam
    timeSeries: _containers.RepeatedCompositeFieldContainer[InputData.TimeSeriesDao]
    agent: _containers.RepeatedCompositeFieldContainer[InputData.AgentDao]
    contract: _containers.RepeatedCompositeFieldContainer[_Contract_pb2.ProtoContract]
    schema: str
    def __init__(self, runId: _Optional[int] = ..., simulation: _Optional[_Union[InputData.SimulationParam, _Mapping]] = ..., output: _Optional[_Union[InputData.OutputParam, _Mapping]] = ..., timeSeries: _Optional[_Iterable[_Union[InputData.TimeSeriesDao, _Mapping]]] = ..., agent: _Optional[_Iterable[_Union[InputData.AgentDao, _Mapping]]] = ..., contract: _Optional[_Iterable[_Union[_Contract_pb2.ProtoContract, _Mapping]]] = ..., schema: _Optional[str] = ...) -> None: ...
