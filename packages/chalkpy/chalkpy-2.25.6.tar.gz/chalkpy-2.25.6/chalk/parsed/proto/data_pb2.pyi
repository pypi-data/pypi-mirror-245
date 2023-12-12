from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class DateUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Day: _ClassVar[DateUnit]
    DateMillisecond: _ClassVar[DateUnit]

class TimeUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Second: _ClassVar[TimeUnit]
    Millisecond: _ClassVar[TimeUnit]
    Microsecond: _ClassVar[TimeUnit]
    Nanosecond: _ClassVar[TimeUnit]

class IntervalUnit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    YearMonth: _ClassVar[IntervalUnit]
    DayTime: _ClassVar[IntervalUnit]
    MonthDayNano: _ClassVar[IntervalUnit]

class UnionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    sparse: _ClassVar[UnionMode]
    dense: _ClassVar[UnionMode]

Day: DateUnit
DateMillisecond: DateUnit
Second: TimeUnit
Millisecond: TimeUnit
Microsecond: TimeUnit
Nanosecond: TimeUnit
YearMonth: IntervalUnit
DayTime: IntervalUnit
MonthDayNano: IntervalUnit
sparse: UnionMode
dense: UnionMode

class Schema(_message.Message):
    __slots__ = ["columns", "metadata"]

    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[Field]
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        columns: _Optional[_Iterable[_Union[Field, _Mapping]]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class Field(_message.Message):
    __slots__ = ["name", "arrow_type", "nullable", "children", "metadata"]

    class MetadataEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARROW_TYPE_FIELD_NUMBER: _ClassVar[int]
    NULLABLE_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    name: str
    arrow_type: ArrowType
    nullable: bool
    children: _containers.RepeatedCompositeFieldContainer[Field]
    metadata: _containers.ScalarMap[str, str]
    def __init__(
        self,
        name: _Optional[str] = ...,
        arrow_type: _Optional[_Union[ArrowType, _Mapping]] = ...,
        nullable: bool = ...,
        children: _Optional[_Iterable[_Union[Field, _Mapping]]] = ...,
        metadata: _Optional[_Mapping[str, str]] = ...,
    ) -> None: ...

class FixedSizeBinary(_message.Message):
    __slots__ = ["length"]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    length: int
    def __init__(self, length: _Optional[int] = ...) -> None: ...

class Timestamp(_message.Message):
    __slots__ = ["time_unit", "timezone"]
    TIME_UNIT_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    time_unit: TimeUnit
    timezone: str
    def __init__(self, time_unit: _Optional[_Union[TimeUnit, str]] = ..., timezone: _Optional[str] = ...) -> None: ...

class Decimal(_message.Message):
    __slots__ = ["precision", "scale"]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    precision: int
    scale: int
    def __init__(self, precision: _Optional[int] = ..., scale: _Optional[int] = ...) -> None: ...

class List(_message.Message):
    __slots__ = ["field_type"]
    FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
    field_type: Field
    def __init__(self, field_type: _Optional[_Union[Field, _Mapping]] = ...) -> None: ...

class FixedSizeList(_message.Message):
    __slots__ = ["field_type", "list_size"]
    FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
    LIST_SIZE_FIELD_NUMBER: _ClassVar[int]
    field_type: Field
    list_size: int
    def __init__(
        self, field_type: _Optional[_Union[Field, _Mapping]] = ..., list_size: _Optional[int] = ...
    ) -> None: ...

class Dictionary(_message.Message):
    __slots__ = ["key", "value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: ArrowType
    value: ArrowType
    def __init__(
        self, key: _Optional[_Union[ArrowType, _Mapping]] = ..., value: _Optional[_Union[ArrowType, _Mapping]] = ...
    ) -> None: ...

class Struct(_message.Message):
    __slots__ = ["sub_field_types"]
    SUB_FIELD_TYPES_FIELD_NUMBER: _ClassVar[int]
    sub_field_types: _containers.RepeatedCompositeFieldContainer[Field]
    def __init__(self, sub_field_types: _Optional[_Iterable[_Union[Field, _Mapping]]] = ...) -> None: ...

class Map(_message.Message):
    __slots__ = ["field_type", "keys_sorted"]
    FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
    KEYS_SORTED_FIELD_NUMBER: _ClassVar[int]
    field_type: Field
    keys_sorted: bool
    def __init__(self, field_type: _Optional[_Union[Field, _Mapping]] = ..., keys_sorted: bool = ...) -> None: ...

class Union(_message.Message):
    __slots__ = ["union_types", "union_mode", "type_ids"]
    UNION_TYPES_FIELD_NUMBER: _ClassVar[int]
    UNION_MODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_IDS_FIELD_NUMBER: _ClassVar[int]
    union_types: _containers.RepeatedCompositeFieldContainer[Field]
    union_mode: UnionMode
    type_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(
        self,
        union_types: _Optional[_Iterable[_Union[Field, _Mapping]]] = ...,
        union_mode: _Optional[_Union[UnionMode, str]] = ...,
        type_ids: _Optional[_Iterable[int]] = ...,
    ) -> None: ...

class ScalarListValue(_message.Message):
    __slots__ = ["ipc_message", "arrow_data", "schema"]
    IPC_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    ARROW_DATA_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    ipc_message: bytes
    arrow_data: bytes
    schema: Schema
    def __init__(
        self,
        ipc_message: _Optional[bytes] = ...,
        arrow_data: _Optional[bytes] = ...,
        schema: _Optional[_Union[Schema, _Mapping]] = ...,
    ) -> None: ...

class ScalarTime32Value(_message.Message):
    __slots__ = ["time32_second_value", "time32_millisecond_value"]
    TIME32_SECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME32_MILLISECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    time32_second_value: int
    time32_millisecond_value: int
    def __init__(
        self, time32_second_value: _Optional[int] = ..., time32_millisecond_value: _Optional[int] = ...
    ) -> None: ...

class ScalarTime64Value(_message.Message):
    __slots__ = ["time64_microsecond_value", "time64_nanosecond_value"]
    TIME64_MICROSECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME64_NANOSECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    time64_microsecond_value: int
    time64_nanosecond_value: int
    def __init__(
        self, time64_microsecond_value: _Optional[int] = ..., time64_nanosecond_value: _Optional[int] = ...
    ) -> None: ...

class ScalarTimestampValue(_message.Message):
    __slots__ = [
        "time_microsecond_value",
        "time_nanosecond_value",
        "time_second_value",
        "time_millisecond_value",
        "timezone",
    ]
    TIME_MICROSECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME_NANOSECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME_SECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME_MILLISECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMEZONE_FIELD_NUMBER: _ClassVar[int]
    time_microsecond_value: int
    time_nanosecond_value: int
    time_second_value: int
    time_millisecond_value: int
    timezone: str
    def __init__(
        self,
        time_microsecond_value: _Optional[int] = ...,
        time_nanosecond_value: _Optional[int] = ...,
        time_second_value: _Optional[int] = ...,
        time_millisecond_value: _Optional[int] = ...,
        timezone: _Optional[str] = ...,
    ) -> None: ...

class ScalarDictionaryValue(_message.Message):
    __slots__ = ["index_type", "value"]
    INDEX_TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    index_type: ArrowType
    value: ScalarValue
    def __init__(
        self,
        index_type: _Optional[_Union[ArrowType, _Mapping]] = ...,
        value: _Optional[_Union[ScalarValue, _Mapping]] = ...,
    ) -> None: ...

class IntervalMonthDayNanoValue(_message.Message):
    __slots__ = ["months", "days", "nanos"]
    MONTHS_FIELD_NUMBER: _ClassVar[int]
    DAYS_FIELD_NUMBER: _ClassVar[int]
    NANOS_FIELD_NUMBER: _ClassVar[int]
    months: int
    days: int
    nanos: int
    def __init__(
        self, months: _Optional[int] = ..., days: _Optional[int] = ..., nanos: _Optional[int] = ...
    ) -> None: ...

class StructValue(_message.Message):
    __slots__ = ["field_values", "fields"]
    FIELD_VALUES_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    field_values: _containers.RepeatedCompositeFieldContainer[ScalarValue]
    fields: _containers.RepeatedCompositeFieldContainer[Field]
    def __init__(
        self,
        field_values: _Optional[_Iterable[_Union[ScalarValue, _Mapping]]] = ...,
        fields: _Optional[_Iterable[_Union[Field, _Mapping]]] = ...,
    ) -> None: ...

class ScalarFixedSizeBinary(_message.Message):
    __slots__ = ["values", "length"]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    values: bytes
    length: int
    def __init__(self, values: _Optional[bytes] = ..., length: _Optional[int] = ...) -> None: ...

class ScalarValue(_message.Message):
    __slots__ = [
        "null_value",
        "bool_value",
        "utf8_value",
        "large_utf8_value",
        "int8_value",
        "int16_value",
        "int32_value",
        "int64_value",
        "uint8_value",
        "uint16_value",
        "uint32_value",
        "uint64_value",
        "float32_value",
        "float64_value",
        "date_32_value",
        "time32_value",
        "list_value",
        "decimal128_value",
        "decimal256_value",
        "date_64_value",
        "interval_yearmonth_value",
        "interval_daytime_value",
        "duration_second_value",
        "duration_millisecond_value",
        "duration_microsecond_value",
        "duration_nanosecond_value",
        "timestamp_value",
        "dictionary_value",
        "binary_value",
        "large_binary_value",
        "time64_value",
        "interval_month_day_nano",
        "struct_value",
        "fixed_size_binary_value",
    ]
    NULL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    UTF8_VALUE_FIELD_NUMBER: _ClassVar[int]
    LARGE_UTF8_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT8_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT16_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT8_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT16_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    DATE_32_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME32_VALUE_FIELD_NUMBER: _ClassVar[int]
    LIST_VALUE_FIELD_NUMBER: _ClassVar[int]
    DECIMAL128_VALUE_FIELD_NUMBER: _ClassVar[int]
    DECIMAL256_VALUE_FIELD_NUMBER: _ClassVar[int]
    DATE_64_VALUE_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_YEARMONTH_VALUE_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_DAYTIME_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_SECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_MILLISECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_MICROSECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_NANOSECOND_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_VALUE_FIELD_NUMBER: _ClassVar[int]
    DICTIONARY_VALUE_FIELD_NUMBER: _ClassVar[int]
    BINARY_VALUE_FIELD_NUMBER: _ClassVar[int]
    LARGE_BINARY_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME64_VALUE_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_MONTH_DAY_NANO_FIELD_NUMBER: _ClassVar[int]
    STRUCT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FIXED_SIZE_BINARY_VALUE_FIELD_NUMBER: _ClassVar[int]
    null_value: ArrowType
    bool_value: bool
    utf8_value: str
    large_utf8_value: str
    int8_value: int
    int16_value: int
    int32_value: int
    int64_value: int
    uint8_value: int
    uint16_value: int
    uint32_value: int
    uint64_value: int
    float32_value: float
    float64_value: float
    date_32_value: int
    time32_value: ScalarTime32Value
    list_value: ScalarListValue
    decimal128_value: Decimal128
    decimal256_value: Decimal256
    date_64_value: int
    interval_yearmonth_value: int
    interval_daytime_value: int
    duration_second_value: int
    duration_millisecond_value: int
    duration_microsecond_value: int
    duration_nanosecond_value: int
    timestamp_value: ScalarTimestampValue
    dictionary_value: ScalarDictionaryValue
    binary_value: bytes
    large_binary_value: bytes
    time64_value: ScalarTime64Value
    interval_month_day_nano: IntervalMonthDayNanoValue
    struct_value: StructValue
    fixed_size_binary_value: ScalarFixedSizeBinary
    def __init__(
        self,
        null_value: _Optional[_Union[ArrowType, _Mapping]] = ...,
        bool_value: bool = ...,
        utf8_value: _Optional[str] = ...,
        large_utf8_value: _Optional[str] = ...,
        int8_value: _Optional[int] = ...,
        int16_value: _Optional[int] = ...,
        int32_value: _Optional[int] = ...,
        int64_value: _Optional[int] = ...,
        uint8_value: _Optional[int] = ...,
        uint16_value: _Optional[int] = ...,
        uint32_value: _Optional[int] = ...,
        uint64_value: _Optional[int] = ...,
        float32_value: _Optional[float] = ...,
        float64_value: _Optional[float] = ...,
        date_32_value: _Optional[int] = ...,
        time32_value: _Optional[_Union[ScalarTime32Value, _Mapping]] = ...,
        list_value: _Optional[_Union[ScalarListValue, _Mapping]] = ...,
        decimal128_value: _Optional[_Union[Decimal128, _Mapping]] = ...,
        decimal256_value: _Optional[_Union[Decimal256, _Mapping]] = ...,
        date_64_value: _Optional[int] = ...,
        interval_yearmonth_value: _Optional[int] = ...,
        interval_daytime_value: _Optional[int] = ...,
        duration_second_value: _Optional[int] = ...,
        duration_millisecond_value: _Optional[int] = ...,
        duration_microsecond_value: _Optional[int] = ...,
        duration_nanosecond_value: _Optional[int] = ...,
        timestamp_value: _Optional[_Union[ScalarTimestampValue, _Mapping]] = ...,
        dictionary_value: _Optional[_Union[ScalarDictionaryValue, _Mapping]] = ...,
        binary_value: _Optional[bytes] = ...,
        large_binary_value: _Optional[bytes] = ...,
        time64_value: _Optional[_Union[ScalarTime64Value, _Mapping]] = ...,
        interval_month_day_nano: _Optional[_Union[IntervalMonthDayNanoValue, _Mapping]] = ...,
        struct_value: _Optional[_Union[StructValue, _Mapping]] = ...,
        fixed_size_binary_value: _Optional[_Union[ScalarFixedSizeBinary, _Mapping]] = ...,
    ) -> None: ...

class Decimal128(_message.Message):
    __slots__ = ["value", "p", "s"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    p: int
    s: int
    def __init__(self, value: _Optional[bytes] = ..., p: _Optional[int] = ..., s: _Optional[int] = ...) -> None: ...

class Decimal256(_message.Message):
    __slots__ = ["value", "p", "s"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    value: bytes
    p: int
    s: int
    def __init__(self, value: _Optional[bytes] = ..., p: _Optional[int] = ..., s: _Optional[int] = ...) -> None: ...

class ArrowType(_message.Message):
    __slots__ = [
        "NONE",
        "BOOL",
        "UINT8",
        "INT8",
        "UINT16",
        "INT16",
        "UINT32",
        "INT32",
        "UINT64",
        "INT64",
        "FLOAT16",
        "FLOAT32",
        "FLOAT64",
        "UTF8",
        "LARGE_UTF8",
        "BINARY",
        "FIXED_SIZE_BINARY",
        "LARGE_BINARY",
        "DATE32",
        "DATE64",
        "DURATION",
        "TIMESTAMP",
        "TIME32",
        "TIME64",
        "INTERVAL",
        "DECIMAL",
        "LIST",
        "LARGE_LIST",
        "FIXED_SIZE_LIST",
        "STRUCT",
        "UNION",
        "DICTIONARY",
        "MAP",
    ]
    NONE_FIELD_NUMBER: _ClassVar[int]
    BOOL_FIELD_NUMBER: _ClassVar[int]
    UINT8_FIELD_NUMBER: _ClassVar[int]
    INT8_FIELD_NUMBER: _ClassVar[int]
    UINT16_FIELD_NUMBER: _ClassVar[int]
    INT16_FIELD_NUMBER: _ClassVar[int]
    UINT32_FIELD_NUMBER: _ClassVar[int]
    INT32_FIELD_NUMBER: _ClassVar[int]
    UINT64_FIELD_NUMBER: _ClassVar[int]
    INT64_FIELD_NUMBER: _ClassVar[int]
    FLOAT16_FIELD_NUMBER: _ClassVar[int]
    FLOAT32_FIELD_NUMBER: _ClassVar[int]
    FLOAT64_FIELD_NUMBER: _ClassVar[int]
    UTF8_FIELD_NUMBER: _ClassVar[int]
    LARGE_UTF8_FIELD_NUMBER: _ClassVar[int]
    BINARY_FIELD_NUMBER: _ClassVar[int]
    FIXED_SIZE_BINARY_FIELD_NUMBER: _ClassVar[int]
    LARGE_BINARY_FIELD_NUMBER: _ClassVar[int]
    DATE32_FIELD_NUMBER: _ClassVar[int]
    DATE64_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TIME32_FIELD_NUMBER: _ClassVar[int]
    TIME64_FIELD_NUMBER: _ClassVar[int]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    DECIMAL_FIELD_NUMBER: _ClassVar[int]
    LIST_FIELD_NUMBER: _ClassVar[int]
    LARGE_LIST_FIELD_NUMBER: _ClassVar[int]
    FIXED_SIZE_LIST_FIELD_NUMBER: _ClassVar[int]
    STRUCT_FIELD_NUMBER: _ClassVar[int]
    UNION_FIELD_NUMBER: _ClassVar[int]
    DICTIONARY_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    NONE: EmptyMessage
    BOOL: EmptyMessage
    UINT8: EmptyMessage
    INT8: EmptyMessage
    UINT16: EmptyMessage
    INT16: EmptyMessage
    UINT32: EmptyMessage
    INT32: EmptyMessage
    UINT64: EmptyMessage
    INT64: EmptyMessage
    FLOAT16: EmptyMessage
    FLOAT32: EmptyMessage
    FLOAT64: EmptyMessage
    UTF8: EmptyMessage
    LARGE_UTF8: EmptyMessage
    BINARY: EmptyMessage
    FIXED_SIZE_BINARY: int
    LARGE_BINARY: EmptyMessage
    DATE32: EmptyMessage
    DATE64: EmptyMessage
    DURATION: TimeUnit
    TIMESTAMP: Timestamp
    TIME32: TimeUnit
    TIME64: TimeUnit
    INTERVAL: IntervalUnit
    DECIMAL: Decimal
    LIST: List
    LARGE_LIST: List
    FIXED_SIZE_LIST: FixedSizeList
    STRUCT: Struct
    UNION: Union
    DICTIONARY: Dictionary
    MAP: Map
    def __init__(
        self,
        NONE: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        BOOL: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        UINT8: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        INT8: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        UINT16: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        INT16: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        UINT32: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        INT32: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        UINT64: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        INT64: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        FLOAT16: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        FLOAT32: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        FLOAT64: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        UTF8: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        LARGE_UTF8: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        BINARY: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        FIXED_SIZE_BINARY: _Optional[int] = ...,
        LARGE_BINARY: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        DATE32: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        DATE64: _Optional[_Union[EmptyMessage, _Mapping]] = ...,
        DURATION: _Optional[_Union[TimeUnit, str]] = ...,
        TIMESTAMP: _Optional[_Union[Timestamp, _Mapping]] = ...,
        TIME32: _Optional[_Union[TimeUnit, str]] = ...,
        TIME64: _Optional[_Union[TimeUnit, str]] = ...,
        INTERVAL: _Optional[_Union[IntervalUnit, str]] = ...,
        DECIMAL: _Optional[_Union[Decimal, _Mapping]] = ...,
        LIST: _Optional[_Union[List, _Mapping]] = ...,
        LARGE_LIST: _Optional[_Union[List, _Mapping]] = ...,
        FIXED_SIZE_LIST: _Optional[_Union[FixedSizeList, _Mapping]] = ...,
        STRUCT: _Optional[_Union[Struct, _Mapping]] = ...,
        UNION: _Optional[_Union[Union, _Mapping]] = ...,
        DICTIONARY: _Optional[_Union[Dictionary, _Mapping]] = ...,
        MAP: _Optional[_Union[Map, _Mapping]] = ...,
    ) -> None: ...

class EmptyMessage(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
