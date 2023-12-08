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

class MetricKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    METRIC_KIND_FEATURE_REQUEST_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_STALENESS: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_VALUE: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_WRITE: _ClassVar[MetricKind]
    METRIC_KIND_FEATURE_NULL_RATIO: _ClassVar[MetricKind]
    METRIC_KIND_RESOLVER_REQUEST_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_RESOLVER_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_RESOLVER_SUCCESS_RATIO: _ClassVar[MetricKind]
    METRIC_KIND_QUERY_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_QUERY_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_QUERY_SUCCESS_RATIO: _ClassVar[MetricKind]
    METRIC_KIND_BILLING_INFERENCE: _ClassVar[MetricKind]
    METRIC_KIND_BILLING_CRON: _ClassVar[MetricKind]
    METRIC_KIND_BILLING_MIGRATION: _ClassVar[MetricKind]
    METRIC_KIND_CRON_COUNT: _ClassVar[MetricKind]
    METRIC_KIND_CRON_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_MESSAGES_PROCESSED: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_MESSAGE_LATENCY: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_WINDOWS_PROCESSED: _ClassVar[MetricKind]
    METRIC_KIND_STREAM_WINDOW_LATENCY: _ClassVar[MetricKind]

class FilterKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    FILTER_KIND_FEATURE_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_FEATURE_NAME: _ClassVar[FilterKind]
    FILTER_KIND_FEATURE_TAG: _ClassVar[FilterKind]
    FILTER_KIND_RESOLVER_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_RESOLVER_NAME: _ClassVar[FilterKind]
    FILTER_KIND_RESOLVER_TAG: _ClassVar[FilterKind]
    FILTER_KIND_CRON_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_MIGRATION_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_ONLINE_OFFLINE: _ClassVar[FilterKind]
    FILTER_KIND_CACHE_HIT: _ClassVar[FilterKind]
    FILTER_KIND_OPERATION_ID: _ClassVar[FilterKind]
    FILTER_KIND_QUERY_NAME: _ClassVar[FilterKind]
    FILTER_KIND_QUERY_STATUS: _ClassVar[FilterKind]
    FILTER_KIND_IS_NULL: _ClassVar[FilterKind]

class ComparatorKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    COMPARATOR_KIND_EQ: _ClassVar[ComparatorKind]
    COMPARATOR_KIND_NEQ: _ClassVar[ComparatorKind]
    COMPARATOR_KIND_ONE_OF: _ClassVar[ComparatorKind]

class WindowFunctionKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    WINDOW_FUNCTION_KIND_COUNT: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_MEAN: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_SUM: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_MIN: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_MAX: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_99: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_95: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_75: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_50: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_25: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_PERCENTILE_5: _ClassVar[WindowFunctionKind]
    WINDOW_FUNCTION_KIND_ALL_PERCENTILES: _ClassVar[WindowFunctionKind]

class GroupByKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    GROUP_BY_KIND_FEATURE_STATUS: _ClassVar[GroupByKind]
    GROUP_BY_KIND_FEATURE_NAME: _ClassVar[GroupByKind]
    GROUP_BY_KIND_IS_NULL: _ClassVar[GroupByKind]
    GROUP_BY_KIND_RESOLVER_STATUS: _ClassVar[GroupByKind]
    GROUP_BY_KIND_RESOLVER_NAME: _ClassVar[GroupByKind]
    GROUP_BY_KIND_QUERY_STATUS: _ClassVar[GroupByKind]
    GROUP_BY_KIND_QUERY_NAME: _ClassVar[GroupByKind]
    GROUP_BY_KIND_ONLINE_OFFLINE: _ClassVar[GroupByKind]
    GROUP_BY_KIND_CACHE_HIT: _ClassVar[GroupByKind]

class MetricFormulaKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    METRIC_FORMULA_KIND_SUM: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_TOTAL_RATIO: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_RATIO: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_PRODUCT: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_ABS: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_KS_STAT: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_KS_TEST: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_KS_THRESHOLD: _ClassVar[MetricFormulaKind]
    METRIC_FORMULA_KIND_TIME_OFFSET: _ClassVar[MetricFormulaKind]

class AlertSeverityKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ALERT_SEVERITY_KIND_CRITICAL: _ClassVar[AlertSeverityKind]
    ALERT_SEVERITY_KIND_ERROR: _ClassVar[AlertSeverityKind]
    ALERT_SEVERITY_KIND_WARNING: _ClassVar[AlertSeverityKind]
    ALERT_SEVERITY_KIND_INFO: _ClassVar[AlertSeverityKind]

class ThresholdKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    THRESHOLD_KIND_ABOVE: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_BELOW: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_GREATER_EQUAL: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_LESS_EQUAL: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_EQUAL: _ClassVar[ThresholdKind]
    THRESHOLD_KIND_NOT_EQUAL: _ClassVar[ThresholdKind]

class GraphLogSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    GRAPH_LOG_SEVERITY_ERROR: _ClassVar[GraphLogSeverity]
    GRAPH_LOG_SEVERITY_WARNING: _ClassVar[GraphLogSeverity]
    GRAPH_LOG_SEVERITY_INFO: _ClassVar[GraphLogSeverity]

class DiagnosticSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DIAGNOSTIC_SEVERITY_ERROR: _ClassVar[DiagnosticSeverity]
    DIAGNOSTIC_SEVERITY_WARNING: _ClassVar[DiagnosticSeverity]
    DIAGNOSTIC_SEVERITY_INFORMATION: _ClassVar[DiagnosticSeverity]
    DIAGNOSTIC_SEVERITY_HINT: _ClassVar[DiagnosticSeverity]

METRIC_KIND_FEATURE_REQUEST_COUNT: MetricKind
METRIC_KIND_FEATURE_LATENCY: MetricKind
METRIC_KIND_FEATURE_STALENESS: MetricKind
METRIC_KIND_FEATURE_VALUE: MetricKind
METRIC_KIND_FEATURE_WRITE: MetricKind
METRIC_KIND_FEATURE_NULL_RATIO: MetricKind
METRIC_KIND_RESOLVER_REQUEST_COUNT: MetricKind
METRIC_KIND_RESOLVER_LATENCY: MetricKind
METRIC_KIND_RESOLVER_SUCCESS_RATIO: MetricKind
METRIC_KIND_QUERY_COUNT: MetricKind
METRIC_KIND_QUERY_LATENCY: MetricKind
METRIC_KIND_QUERY_SUCCESS_RATIO: MetricKind
METRIC_KIND_BILLING_INFERENCE: MetricKind
METRIC_KIND_BILLING_CRON: MetricKind
METRIC_KIND_BILLING_MIGRATION: MetricKind
METRIC_KIND_CRON_COUNT: MetricKind
METRIC_KIND_CRON_LATENCY: MetricKind
METRIC_KIND_STREAM_MESSAGES_PROCESSED: MetricKind
METRIC_KIND_STREAM_MESSAGE_LATENCY: MetricKind
METRIC_KIND_STREAM_WINDOWS_PROCESSED: MetricKind
METRIC_KIND_STREAM_WINDOW_LATENCY: MetricKind
FILTER_KIND_FEATURE_STATUS: FilterKind
FILTER_KIND_FEATURE_NAME: FilterKind
FILTER_KIND_FEATURE_TAG: FilterKind
FILTER_KIND_RESOLVER_STATUS: FilterKind
FILTER_KIND_RESOLVER_NAME: FilterKind
FILTER_KIND_RESOLVER_TAG: FilterKind
FILTER_KIND_CRON_STATUS: FilterKind
FILTER_KIND_MIGRATION_STATUS: FilterKind
FILTER_KIND_ONLINE_OFFLINE: FilterKind
FILTER_KIND_CACHE_HIT: FilterKind
FILTER_KIND_OPERATION_ID: FilterKind
FILTER_KIND_QUERY_NAME: FilterKind
FILTER_KIND_QUERY_STATUS: FilterKind
FILTER_KIND_IS_NULL: FilterKind
COMPARATOR_KIND_EQ: ComparatorKind
COMPARATOR_KIND_NEQ: ComparatorKind
COMPARATOR_KIND_ONE_OF: ComparatorKind
WINDOW_FUNCTION_KIND_COUNT: WindowFunctionKind
WINDOW_FUNCTION_KIND_MEAN: WindowFunctionKind
WINDOW_FUNCTION_KIND_SUM: WindowFunctionKind
WINDOW_FUNCTION_KIND_MIN: WindowFunctionKind
WINDOW_FUNCTION_KIND_MAX: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_99: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_95: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_75: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_50: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_25: WindowFunctionKind
WINDOW_FUNCTION_KIND_PERCENTILE_5: WindowFunctionKind
WINDOW_FUNCTION_KIND_ALL_PERCENTILES: WindowFunctionKind
GROUP_BY_KIND_FEATURE_STATUS: GroupByKind
GROUP_BY_KIND_FEATURE_NAME: GroupByKind
GROUP_BY_KIND_IS_NULL: GroupByKind
GROUP_BY_KIND_RESOLVER_STATUS: GroupByKind
GROUP_BY_KIND_RESOLVER_NAME: GroupByKind
GROUP_BY_KIND_QUERY_STATUS: GroupByKind
GROUP_BY_KIND_QUERY_NAME: GroupByKind
GROUP_BY_KIND_ONLINE_OFFLINE: GroupByKind
GROUP_BY_KIND_CACHE_HIT: GroupByKind
METRIC_FORMULA_KIND_SUM: MetricFormulaKind
METRIC_FORMULA_KIND_TOTAL_RATIO: MetricFormulaKind
METRIC_FORMULA_KIND_RATIO: MetricFormulaKind
METRIC_FORMULA_KIND_PRODUCT: MetricFormulaKind
METRIC_FORMULA_KIND_ABS: MetricFormulaKind
METRIC_FORMULA_KIND_KS_STAT: MetricFormulaKind
METRIC_FORMULA_KIND_KS_TEST: MetricFormulaKind
METRIC_FORMULA_KIND_KS_THRESHOLD: MetricFormulaKind
METRIC_FORMULA_KIND_TIME_OFFSET: MetricFormulaKind
ALERT_SEVERITY_KIND_CRITICAL: AlertSeverityKind
ALERT_SEVERITY_KIND_ERROR: AlertSeverityKind
ALERT_SEVERITY_KIND_WARNING: AlertSeverityKind
ALERT_SEVERITY_KIND_INFO: AlertSeverityKind
THRESHOLD_KIND_ABOVE: ThresholdKind
THRESHOLD_KIND_BELOW: ThresholdKind
THRESHOLD_KIND_GREATER_EQUAL: ThresholdKind
THRESHOLD_KIND_LESS_EQUAL: ThresholdKind
THRESHOLD_KIND_EQUAL: ThresholdKind
THRESHOLD_KIND_NOT_EQUAL: ThresholdKind
GRAPH_LOG_SEVERITY_ERROR: GraphLogSeverity
GRAPH_LOG_SEVERITY_WARNING: GraphLogSeverity
GRAPH_LOG_SEVERITY_INFO: GraphLogSeverity
DIAGNOSTIC_SEVERITY_ERROR: DiagnosticSeverity
DIAGNOSTIC_SEVERITY_WARNING: DiagnosticSeverity
DIAGNOSTIC_SEVERITY_INFORMATION: DiagnosticSeverity
DIAGNOSTIC_SEVERITY_HINT: DiagnosticSeverity

class FeatureId(_message.Message):
    __slots__ = ["fqn", "name", "namespace", "is_primary", "class_name", "attribute_name", "explicit_namespace"]
    FQN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    IS_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    EXPLICIT_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    name: str
    namespace: str
    is_primary: bool
    class_name: str
    attribute_name: str
    explicit_namespace: bool
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        name: _Optional[str] = ...,
        namespace: _Optional[str] = ...,
        is_primary: bool = ...,
        class_name: _Optional[str] = ...,
        attribute_name: _Optional[str] = ...,
        explicit_namespace: bool = ...,
    ) -> None: ...

class ReferencePathComponent(_message.Message):
    __slots__ = ["parent", "child", "parent_to_child_attribute_name"]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    CHILD_FIELD_NUMBER: _ClassVar[int]
    PARENT_TO_CHILD_ATTRIBUTE_NAME_FIELD_NUMBER: _ClassVar[int]
    parent: FeatureId
    child: FeatureId
    parent_to_child_attribute_name: str
    def __init__(
        self,
        parent: _Optional[_Union[FeatureId, _Mapping]] = ...,
        child: _Optional[_Union[FeatureId, _Mapping]] = ...,
        parent_to_child_attribute_name: _Optional[str] = ...,
    ) -> None: ...

class Filter(_message.Message):
    __slots__ = ["lhs", "op", "rhs"]
    LHS_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    RHS_FIELD_NUMBER: _ClassVar[int]
    lhs: FeatureId
    op: str
    rhs: FeatureId
    def __init__(
        self,
        lhs: _Optional[_Union[FeatureId, _Mapping]] = ...,
        op: _Optional[str] = ...,
        rhs: _Optional[_Union[FeatureId, _Mapping]] = ...,
    ) -> None: ...

class DataFrame(_message.Message):
    __slots__ = ["columns", "filters"]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    columns: _containers.RepeatedCompositeFieldContainer[FeatureId]
    filters: _containers.RepeatedCompositeFieldContainer[Filter]
    def __init__(
        self,
        columns: _Optional[_Iterable[_Union[FeatureId, _Mapping]]] = ...,
        filters: _Optional[_Iterable[_Union[Filter, _Mapping]]] = ...,
    ) -> None: ...

class FeatureReference(_message.Message):
    __slots__ = ["underlying", "path"]
    UNDERLYING_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    underlying: FeatureId
    path: _containers.RepeatedCompositeFieldContainer[ReferencePathComponent]
    def __init__(
        self,
        underlying: _Optional[_Union[FeatureId, _Mapping]] = ...,
        path: _Optional[_Iterable[_Union[ReferencePathComponent, _Mapping]]] = ...,
    ) -> None: ...

class HasOneKind(_message.Message):
    __slots__ = ["join"]
    JOIN_FIELD_NUMBER: _ClassVar[int]
    join: Filter
    def __init__(self, join: _Optional[_Union[Filter, _Mapping]] = ...) -> None: ...

class HasManyKind(_message.Message):
    __slots__ = ["join", "columns", "filters"]
    JOIN_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    join: Filter
    columns: _containers.RepeatedCompositeFieldContainer[FeatureId]
    filters: _containers.RepeatedCompositeFieldContainer[Filter]
    def __init__(
        self,
        join: _Optional[_Union[Filter, _Mapping]] = ...,
        columns: _Optional[_Iterable[_Union[FeatureId, _Mapping]]] = ...,
        filters: _Optional[_Iterable[_Union[Filter, _Mapping]]] = ...,
    ) -> None: ...

class VersionInfo(_message.Message):
    __slots__ = ["version", "maximum", "default", "versions"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    VERSIONS_FIELD_NUMBER: _ClassVar[int]
    version: int
    maximum: int
    default: int
    versions: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        version: _Optional[int] = ...,
        maximum: _Optional[int] = ...,
        default: _Optional[int] = ...,
        versions: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ScalarKind(_message.Message):
    __slots__ = [
        "primary",
        "dtype",
        "version",
        "version_info",
        "base_classes",
        "has_encoder_and_decoder",
        "scalar_kind",
    ]
    PRIMARY_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    VERSION_INFO_FIELD_NUMBER: _ClassVar[int]
    BASE_CLASSES_FIELD_NUMBER: _ClassVar[int]
    HAS_ENCODER_AND_DECODER_FIELD_NUMBER: _ClassVar[int]
    SCALAR_KIND_FIELD_NUMBER: _ClassVar[int]
    primary: bool
    dtype: str
    version: int
    version_info: VersionInfo
    base_classes: _containers.RepeatedScalarFieldContainer[str]
    has_encoder_and_decoder: bool
    scalar_kind: str
    def __init__(
        self,
        primary: bool = ...,
        dtype: _Optional[str] = ...,
        version: _Optional[int] = ...,
        version_info: _Optional[_Union[VersionInfo, _Mapping]] = ...,
        base_classes: _Optional[_Iterable[str]] = ...,
        has_encoder_and_decoder: bool = ...,
        scalar_kind: _Optional[str] = ...,
    ) -> None: ...

class FeatureTimeKind(_message.Message):
    __slots__ = ["format"]
    FORMAT_FIELD_NUMBER: _ClassVar[int]
    format: str
    def __init__(self, format: _Optional[str] = ...) -> None: ...

class Feature(_message.Message):
    __slots__ = [
        "id",
        "scalar_kind",
        "has_many_kind",
        "has_one_kind",
        "feature_time_kind",
        "etl_offline_to_online",
        "window_buckets",
        "tags",
        "max_staleness",
        "description",
        "owner",
        "namespace_path",
        "is_singleton",
    ]
    ID_FIELD_NUMBER: _ClassVar[int]
    SCALAR_KIND_FIELD_NUMBER: _ClassVar[int]
    HAS_MANY_KIND_FIELD_NUMBER: _ClassVar[int]
    HAS_ONE_KIND_FIELD_NUMBER: _ClassVar[int]
    FEATURE_TIME_KIND_FIELD_NUMBER: _ClassVar[int]
    ETL_OFFLINE_TO_ONLINE_FIELD_NUMBER: _ClassVar[int]
    WINDOW_BUCKETS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    MAX_STALENESS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_PATH_FIELD_NUMBER: _ClassVar[int]
    IS_SINGLETON_FIELD_NUMBER: _ClassVar[int]
    id: FeatureId
    scalar_kind: ScalarKind
    has_many_kind: HasManyKind
    has_one_kind: HasOneKind
    feature_time_kind: FeatureTimeKind
    etl_offline_to_online: bool
    window_buckets: _containers.RepeatedScalarFieldContainer[float]
    tags: _containers.RepeatedScalarFieldContainer[str]
    max_staleness: str
    description: str
    owner: str
    namespace_path: str
    is_singleton: bool
    def __init__(
        self,
        id: _Optional[_Union[FeatureId, _Mapping]] = ...,
        scalar_kind: _Optional[_Union[ScalarKind, _Mapping]] = ...,
        has_many_kind: _Optional[_Union[HasManyKind, _Mapping]] = ...,
        has_one_kind: _Optional[_Union[HasOneKind, _Mapping]] = ...,
        feature_time_kind: _Optional[_Union[FeatureTimeKind, _Mapping]] = ...,
        etl_offline_to_online: bool = ...,
        window_buckets: _Optional[_Iterable[float]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        max_staleness: _Optional[str] = ...,
        description: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        namespace_path: _Optional[str] = ...,
        is_singleton: bool = ...,
    ) -> None: ...

class KafkaConsumerConfig(_message.Message):
    __slots__ = [
        "broker",
        "topic",
        "ssl_keystore_location",
        "client_id_prefix",
        "group_id_prefix",
        "topic_metadata_refresh_interval_ms",
        "security_protocol",
    ]
    BROKER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    SSL_KEYSTORE_LOCATION_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_PREFIX_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_PREFIX_FIELD_NUMBER: _ClassVar[int]
    TOPIC_METADATA_REFRESH_INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    SECURITY_PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    broker: _containers.RepeatedScalarFieldContainer[str]
    topic: _containers.RepeatedScalarFieldContainer[str]
    ssl_keystore_location: str
    client_id_prefix: str
    group_id_prefix: str
    topic_metadata_refresh_interval_ms: int
    security_protocol: str
    def __init__(
        self,
        broker: _Optional[_Iterable[str]] = ...,
        topic: _Optional[_Iterable[str]] = ...,
        ssl_keystore_location: _Optional[str] = ...,
        client_id_prefix: _Optional[str] = ...,
        group_id_prefix: _Optional[str] = ...,
        topic_metadata_refresh_interval_ms: _Optional[int] = ...,
        security_protocol: _Optional[str] = ...,
    ) -> None: ...

class StreamResolverParamMessage(_message.Message):
    __slots__ = ["name", "type_name", "bases", "schema"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    BASES_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    name: str
    type_name: str
    bases: _containers.RepeatedScalarFieldContainer[str]
    schema: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        type_name: _Optional[str] = ...,
        bases: _Optional[_Iterable[str]] = ...,
        schema: _Optional[str] = ...,
    ) -> None: ...

class StreamResolverParamKeyedState(_message.Message):
    __slots__ = ["name", "type_name", "bases", "schema", "default_value"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    BASES_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type_name: str
    bases: _containers.RepeatedScalarFieldContainer[str]
    schema: str
    default_value: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        type_name: _Optional[str] = ...,
        bases: _Optional[_Iterable[str]] = ...,
        schema: _Optional[str] = ...,
        default_value: _Optional[str] = ...,
    ) -> None: ...

class StreamResolverParam(_message.Message):
    __slots__ = ["message", "state"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    message: StreamResolverParamMessage
    state: StreamResolverParamKeyedState
    def __init__(
        self,
        message: _Optional[_Union[StreamResolverParamMessage, _Mapping]] = ...,
        state: _Optional[_Union[StreamResolverParamKeyedState, _Mapping]] = ...,
    ) -> None: ...

class StreamResolver(_message.Message):
    __slots__ = [
        "fqn",
        "kind",
        "function_definition",
        "source_class_name",
        "source_config",
        "machine_type",
        "environment",
        "output",
        "inputs",
        "doc",
        "owner",
        "filename",
        "source_line",
    ]
    FQN_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CONFIG_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_LINE_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    kind: str
    function_definition: str
    source_class_name: str
    source_config: str
    machine_type: str
    environment: _containers.RepeatedScalarFieldContainer[str]
    output: _containers.RepeatedCompositeFieldContainer[FeatureId]
    inputs: _containers.RepeatedCompositeFieldContainer[StreamResolverParam]
    doc: str
    owner: str
    filename: str
    source_line: int
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        function_definition: _Optional[str] = ...,
        source_class_name: _Optional[str] = ...,
        source_config: _Optional[str] = ...,
        machine_type: _Optional[str] = ...,
        environment: _Optional[_Iterable[str]] = ...,
        output: _Optional[_Iterable[_Union[FeatureId, _Mapping]]] = ...,
        inputs: _Optional[_Iterable[_Union[StreamResolverParam, _Mapping]]] = ...,
        doc: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        filename: _Optional[str] = ...,
        source_line: _Optional[int] = ...,
    ) -> None: ...

class ResolverOutput(_message.Message):
    __slots__ = ["features", "dataframes"]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    DATAFRAMES_FIELD_NUMBER: _ClassVar[int]
    features: _containers.RepeatedCompositeFieldContainer[FeatureId]
    dataframes: _containers.RepeatedCompositeFieldContainer[DataFrame]
    def __init__(
        self,
        features: _Optional[_Iterable[_Union[FeatureId, _Mapping]]] = ...,
        dataframes: _Optional[_Iterable[_Union[DataFrame, _Mapping]]] = ...,
    ) -> None: ...

class ResolverInputUnion(_message.Message):
    __slots__ = ["feature", "dataframe", "pseudo_feature"]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    DATAFRAME_FIELD_NUMBER: _ClassVar[int]
    PSEUDO_FEATURE_FIELD_NUMBER: _ClassVar[int]
    feature: FeatureReference
    dataframe: DataFrame
    pseudo_feature: FeatureReference
    def __init__(
        self,
        feature: _Optional[_Union[FeatureReference, _Mapping]] = ...,
        dataframe: _Optional[_Union[DataFrame, _Mapping]] = ...,
        pseudo_feature: _Optional[_Union[FeatureReference, _Mapping]] = ...,
    ) -> None: ...

class DataSource(_message.Message):
    __slots__ = ["name", "kind"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: str
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...

class Resolver(_message.Message):
    __slots__ = [
        "fqn",
        "kind",
        "function_definition",
        "output",
        "environment",
        "tags",
        "doc",
        "cron",
        "inputs",
        "all_inputs",
        "machine_type",
        "owner",
        "timeout",
        "filename",
        "source_line",
        "data_sources",
    ]
    FQN_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    CRON_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    ALL_INPUTS_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_LINE_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCES_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    kind: str
    function_definition: str
    output: ResolverOutput
    environment: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedScalarFieldContainer[str]
    doc: str
    cron: str
    inputs: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    all_inputs: _containers.RepeatedCompositeFieldContainer[ResolverInputUnion]
    machine_type: str
    owner: str
    timeout: str
    filename: str
    source_line: int
    data_sources: _containers.RepeatedCompositeFieldContainer[DataSource]
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        kind: _Optional[str] = ...,
        function_definition: _Optional[str] = ...,
        output: _Optional[_Union[ResolverOutput, _Mapping]] = ...,
        environment: _Optional[_Iterable[str]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        doc: _Optional[str] = ...,
        cron: _Optional[str] = ...,
        inputs: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        all_inputs: _Optional[_Iterable[_Union[ResolverInputUnion, _Mapping]]] = ...,
        machine_type: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        timeout: _Optional[str] = ...,
        filename: _Optional[str] = ...,
        source_line: _Optional[int] = ...,
        data_sources: _Optional[_Iterable[_Union[DataSource, _Mapping]]] = ...,
    ) -> None: ...

class SinkResolver(_message.Message):
    __slots__ = [
        "fqn",
        "function_definition",
        "environment",
        "tags",
        "doc",
        "inputs",
        "machine_type",
        "buffer_size",
        "debounce",
        "max_delay",
        "upsert",
        "owner",
        "filename",
        "source_line",
    ]
    FQN_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_DEFINITION_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    MACHINE_TYPE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_SIZE_FIELD_NUMBER: _ClassVar[int]
    DEBOUNCE_FIELD_NUMBER: _ClassVar[int]
    MAX_DELAY_FIELD_NUMBER: _ClassVar[int]
    UPSERT_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_LINE_FIELD_NUMBER: _ClassVar[int]
    fqn: str
    function_definition: str
    environment: _containers.RepeatedScalarFieldContainer[str]
    tags: _containers.RepeatedScalarFieldContainer[str]
    doc: str
    inputs: _containers.RepeatedCompositeFieldContainer[FeatureReference]
    machine_type: str
    buffer_size: int
    debounce: str
    max_delay: str
    upsert: bool
    owner: str
    filename: str
    source_line: int
    def __init__(
        self,
        fqn: _Optional[str] = ...,
        function_definition: _Optional[str] = ...,
        environment: _Optional[_Iterable[str]] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        doc: _Optional[str] = ...,
        inputs: _Optional[_Iterable[_Union[FeatureReference, _Mapping]]] = ...,
        machine_type: _Optional[str] = ...,
        buffer_size: _Optional[int] = ...,
        debounce: _Optional[str] = ...,
        max_delay: _Optional[str] = ...,
        upsert: bool = ...,
        owner: _Optional[str] = ...,
        filename: _Optional[str] = ...,
        source_line: _Optional[int] = ...,
    ) -> None: ...

class MetadataSettings(_message.Message):
    __slots__ = ["name", "missing"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MISSING_FIELD_NUMBER: _ClassVar[int]
    name: str
    missing: str
    def __init__(self, name: _Optional[str] = ..., missing: _Optional[str] = ...) -> None: ...

class FeatureSettings(_message.Message):
    __slots__ = ["metadata"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[MetadataSettings]
    def __init__(self, metadata: _Optional[_Iterable[_Union[MetadataSettings, _Mapping]]] = ...) -> None: ...

class ResolverSettings(_message.Message):
    __slots__ = ["metadata"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    metadata: _containers.RepeatedCompositeFieldContainer[MetadataSettings]
    def __init__(self, metadata: _Optional[_Iterable[_Union[MetadataSettings, _Mapping]]] = ...) -> None: ...

class ValidationSettings(_message.Message):
    __slots__ = ["feature", "resolver"]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    RESOLVER_FIELD_NUMBER: _ClassVar[int]
    feature: FeatureSettings
    resolver: ResolverSettings
    def __init__(
        self,
        feature: _Optional[_Union[FeatureSettings, _Mapping]] = ...,
        resolver: _Optional[_Union[ResolverSettings, _Mapping]] = ...,
    ) -> None: ...

class EnvironmentSettings(_message.Message):
    __slots__ = ["id", "runtime", "requirements", "dockerfile", "requires_packages"]
    ID_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    DOCKERFILE_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    id: str
    runtime: str
    requirements: str
    dockerfile: str
    requires_packages: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        runtime: _Optional[str] = ...,
        requirements: _Optional[str] = ...,
        dockerfile: _Optional[str] = ...,
        requires_packages: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class ProjectSettings(_message.Message):
    __slots__ = ["project", "environments", "validation"]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    VALIDATION_FIELD_NUMBER: _ClassVar[int]
    project: str
    environments: _containers.RepeatedCompositeFieldContainer[EnvironmentSettings]
    validation: ValidationSettings
    def __init__(
        self,
        project: _Optional[str] = ...,
        environments: _Optional[_Iterable[_Union[EnvironmentSettings, _Mapping]]] = ...,
        validation: _Optional[_Union[ValidationSettings, _Mapping]] = ...,
    ) -> None: ...

class FailedImport(_message.Message):
    __slots__ = ["filename", "module", "traceback"]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    TRACEBACK_FIELD_NUMBER: _ClassVar[int]
    filename: str
    module: str
    traceback: str
    def __init__(
        self, filename: _Optional[str] = ..., module: _Optional[str] = ..., traceback: _Optional[str] = ...
    ) -> None: ...

class ChalkPYInfo(_message.Message):
    __slots__ = ["version", "python"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PYTHON_FIELD_NUMBER: _ClassVar[int]
    version: str
    python: str
    def __init__(self, version: _Optional[str] = ..., python: _Optional[str] = ...) -> None: ...

class MetricFilter(_message.Message):
    __slots__ = ["kind", "comparator", "value"]
    KIND_FIELD_NUMBER: _ClassVar[int]
    COMPARATOR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    kind: FilterKind
    comparator: ComparatorKind
    value: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        kind: _Optional[_Union[FilterKind, str]] = ...,
        comparator: _Optional[_Union[ComparatorKind, str]] = ...,
        value: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class MetricConfigSeries(_message.Message):
    __slots__ = ["metric", "filters", "name", "window_function", "group_by"]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_BY_FIELD_NUMBER: _ClassVar[int]
    metric: MetricKind
    filters: _containers.RepeatedCompositeFieldContainer[MetricFilter]
    name: str
    window_function: WindowFunctionKind
    group_by: _containers.RepeatedScalarFieldContainer[GroupByKind]
    def __init__(
        self,
        metric: _Optional[_Union[MetricKind, str]] = ...,
        filters: _Optional[_Iterable[_Union[MetricFilter, _Mapping]]] = ...,
        name: _Optional[str] = ...,
        window_function: _Optional[_Union[WindowFunctionKind, str]] = ...,
        group_by: _Optional[_Iterable[_Union[GroupByKind, str]]] = ...,
    ) -> None: ...

class DatasetFeatureOperand(_message.Message):
    __slots__ = ["dataset", "feature"]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FIELD_NUMBER: _ClassVar[int]
    dataset: str
    feature: str
    def __init__(self, dataset: _Optional[str] = ..., feature: _Optional[str] = ...) -> None: ...

class MetricFormula(_message.Message):
    __slots__ = ["kind", "single_series_operands", "multi_series_operands", "dataset_feature_operands", "name"]
    KIND_FIELD_NUMBER: _ClassVar[int]
    SINGLE_SERIES_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    MULTI_SERIES_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    DATASET_FEATURE_OPERANDS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    kind: MetricFormulaKind
    single_series_operands: int
    multi_series_operands: _containers.RepeatedScalarFieldContainer[int]
    dataset_feature_operands: DatasetFeatureOperand
    name: str
    def __init__(
        self,
        kind: _Optional[_Union[MetricFormulaKind, str]] = ...,
        single_series_operands: _Optional[int] = ...,
        multi_series_operands: _Optional[_Iterable[int]] = ...,
        dataset_feature_operands: _Optional[_Union[DatasetFeatureOperand, _Mapping]] = ...,
        name: _Optional[str] = ...,
    ) -> None: ...

class AlertTrigger(_message.Message):
    __slots__ = [
        "name",
        "severity",
        "threshold_position",
        "threshold_value",
        "series_name",
        "channel_name",
        "description",
    ]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_POSITION_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_VALUE_FIELD_NUMBER: _ClassVar[int]
    SERIES_NAME_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    severity: AlertSeverityKind
    threshold_position: ThresholdKind
    threshold_value: float
    series_name: str
    channel_name: str
    description: str
    def __init__(
        self,
        name: _Optional[str] = ...,
        severity: _Optional[_Union[AlertSeverityKind, str]] = ...,
        threshold_position: _Optional[_Union[ThresholdKind, str]] = ...,
        threshold_value: _Optional[float] = ...,
        series_name: _Optional[str] = ...,
        channel_name: _Optional[str] = ...,
        description: _Optional[str] = ...,
    ) -> None: ...

class MetricConfig(_message.Message):
    __slots__ = ["name", "window_period", "series", "formulas", "trigger"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    FORMULAS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    name: str
    window_period: str
    series: _containers.RepeatedCompositeFieldContainer[MetricConfigSeries]
    formulas: _containers.RepeatedCompositeFieldContainer[MetricFormula]
    trigger: AlertTrigger
    def __init__(
        self,
        name: _Optional[str] = ...,
        window_period: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[MetricConfigSeries, _Mapping]]] = ...,
        formulas: _Optional[_Iterable[_Union[MetricFormula, _Mapping]]] = ...,
        trigger: _Optional[_Union[AlertTrigger, _Mapping]] = ...,
    ) -> None: ...

class Chart(_message.Message):
    __slots__ = ["id", "config", "entity_kind", "entity_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    ENTITY_KIND_FIELD_NUMBER: _ClassVar[int]
    ENTITY_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    config: MetricConfig
    entity_kind: str
    entity_id: str
    def __init__(
        self,
        id: _Optional[str] = ...,
        config: _Optional[_Union[MetricConfig, _Mapping]] = ...,
        entity_kind: _Optional[str] = ...,
        entity_id: _Optional[str] = ...,
    ) -> None: ...

class UpdateGraphError(_message.Message):
    __slots__ = ["header", "subheader", "severity"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUBHEADER_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    header: str
    subheader: str
    severity: GraphLogSeverity
    def __init__(
        self,
        header: _Optional[str] = ...,
        subheader: _Optional[str] = ...,
        severity: _Optional[_Union[GraphLogSeverity, str]] = ...,
    ) -> None: ...

class SQLSource(_message.Message):
    __slots__ = ["name", "kind"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: str
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...

class CDCSource(_message.Message):
    __slots__ = ["integration_name", "schema_dot_table_list"]
    INTEGRATION_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_DOT_TABLE_LIST_FIELD_NUMBER: _ClassVar[int]
    integration_name: str
    schema_dot_table_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self, integration_name: _Optional[str] = ..., schema_dot_table_list: _Optional[_Iterable[str]] = ...
    ) -> None: ...

class FeatureClass(_message.Message):
    __slots__ = ["is_singleton", "doc", "name", "owner", "tags"]
    IS_SINGLETON_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    is_singleton: bool
    doc: str
    name: str
    owner: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        is_singleton: bool = ...,
        doc: _Optional[str] = ...,
        name: _Optional[str] = ...,
        owner: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class Position(_message.Message):
    __slots__ = ["line", "character"]
    LINE_FIELD_NUMBER: _ClassVar[int]
    CHARACTER_FIELD_NUMBER: _ClassVar[int]
    line: int
    character: int
    def __init__(self, line: _Optional[int] = ..., character: _Optional[int] = ...) -> None: ...

class Range(_message.Message):
    __slots__ = ["start", "end"]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    start: Position
    end: Position
    def __init__(
        self, start: _Optional[_Union[Position, _Mapping]] = ..., end: _Optional[_Union[Position, _Mapping]] = ...
    ) -> None: ...

class CodeDescription(_message.Message):
    __slots__ = ["href"]
    HREF_FIELD_NUMBER: _ClassVar[int]
    href: str
    def __init__(self, href: _Optional[str] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ["uri", "range"]
    URI_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    uri: str
    range: Range
    def __init__(self, uri: _Optional[str] = ..., range: _Optional[_Union[Range, _Mapping]] = ...) -> None: ...

class DiagnosticRelatedInformation(_message.Message):
    __slots__ = ["location", "message"]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    location: Location
    message: str
    def __init__(
        self, location: _Optional[_Union[Location, _Mapping]] = ..., message: _Optional[str] = ...
    ) -> None: ...

class Diagnostic(_message.Message):
    __slots__ = ["range", "message", "severity", "code", "code_description", "related_information"]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CODE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RELATED_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    range: Range
    message: str
    severity: DiagnosticSeverity
    code: str
    code_description: CodeDescription
    related_information: _containers.RepeatedCompositeFieldContainer[DiagnosticRelatedInformation]
    def __init__(
        self,
        range: _Optional[_Union[Range, _Mapping]] = ...,
        message: _Optional[str] = ...,
        severity: _Optional[_Union[DiagnosticSeverity, str]] = ...,
        code: _Optional[str] = ...,
        code_description: _Optional[_Union[CodeDescription, _Mapping]] = ...,
        related_information: _Optional[_Iterable[_Union[DiagnosticRelatedInformation, _Mapping]]] = ...,
    ) -> None: ...

class PublishDiagnosticsParams(_message.Message):
    __slots__ = ["uri", "diagnostics"]
    URI_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    uri: str
    diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
    def __init__(
        self, uri: _Optional[str] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping]]] = ...
    ) -> None: ...

class TextDocumentIdentifier(_message.Message):
    __slots__ = ["uri"]
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class TextEdit(_message.Message):
    __slots__ = ["range", "new_text"]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    NEW_TEXT_FIELD_NUMBER: _ClassVar[int]
    range: Range
    new_text: str
    def __init__(self, range: _Optional[_Union[Range, _Mapping]] = ..., new_text: _Optional[str] = ...) -> None: ...

class TextDocumentEdit(_message.Message):
    __slots__ = ["text_document", "edits"]
    TEXT_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    EDITS_FIELD_NUMBER: _ClassVar[int]
    text_document: TextDocumentIdentifier
    edits: _containers.RepeatedCompositeFieldContainer[TextEdit]
    def __init__(
        self,
        text_document: _Optional[_Union[TextDocumentIdentifier, _Mapping]] = ...,
        edits: _Optional[_Iterable[_Union[TextEdit, _Mapping]]] = ...,
    ) -> None: ...

class WorkspaceEdit(_message.Message):
    __slots__ = ["document_changes"]
    DOCUMENT_CHANGES_FIELD_NUMBER: _ClassVar[int]
    document_changes: _containers.RepeatedCompositeFieldContainer[TextDocumentEdit]
    def __init__(self, document_changes: _Optional[_Iterable[_Union[TextDocumentEdit, _Mapping]]] = ...) -> None: ...

class CodeAction(_message.Message):
    __slots__ = ["title", "diagnostics", "edit"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    EDIT_FIELD_NUMBER: _ClassVar[int]
    title: str
    diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
    edit: WorkspaceEdit
    def __init__(
        self,
        title: _Optional[str] = ...,
        diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping]]] = ...,
        edit: _Optional[_Union[WorkspaceEdit, _Mapping]] = ...,
    ) -> None: ...

class Lsp(_message.Message):
    __slots__ = ["diagnostics", "actions"]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    diagnostics: _containers.RepeatedCompositeFieldContainer[PublishDiagnosticsParams]
    actions: _containers.RepeatedCompositeFieldContainer[CodeAction]
    def __init__(
        self,
        diagnostics: _Optional[_Iterable[_Union[PublishDiagnosticsParams, _Mapping]]] = ...,
        actions: _Optional[_Iterable[_Union[CodeAction, _Mapping]]] = ...,
    ) -> None: ...

class Graph(_message.Message):
    __slots__ = [
        "resolvers",
        "features",
        "streams",
        "sinks",
        "charts",
        "config",
        "failed",
        "chalkpy",
        "validated",
        "errors",
        "cdc_sources",
        "sql_sources",
        "feature_classes",
        "lsp",
    ]
    RESOLVERS_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    STREAMS_FIELD_NUMBER: _ClassVar[int]
    SINKS_FIELD_NUMBER: _ClassVar[int]
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    CHALKPY_FIELD_NUMBER: _ClassVar[int]
    VALIDATED_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    CDC_SOURCES_FIELD_NUMBER: _ClassVar[int]
    SQL_SOURCES_FIELD_NUMBER: _ClassVar[int]
    FEATURE_CLASSES_FIELD_NUMBER: _ClassVar[int]
    LSP_FIELD_NUMBER: _ClassVar[int]
    resolvers: _containers.RepeatedCompositeFieldContainer[Resolver]
    features: _containers.RepeatedCompositeFieldContainer[Feature]
    streams: _containers.RepeatedCompositeFieldContainer[StreamResolver]
    sinks: _containers.RepeatedCompositeFieldContainer[SinkResolver]
    charts: _containers.RepeatedCompositeFieldContainer[Chart]
    config: ProjectSettings
    failed: _containers.RepeatedCompositeFieldContainer[FailedImport]
    chalkpy: ChalkPYInfo
    validated: bool
    errors: _containers.RepeatedCompositeFieldContainer[UpdateGraphError]
    cdc_sources: _containers.RepeatedCompositeFieldContainer[CDCSource]
    sql_sources: _containers.RepeatedCompositeFieldContainer[SQLSource]
    feature_classes: _containers.RepeatedCompositeFieldContainer[FeatureClass]
    lsp: Lsp
    def __init__(
        self,
        resolvers: _Optional[_Iterable[_Union[Resolver, _Mapping]]] = ...,
        features: _Optional[_Iterable[_Union[Feature, _Mapping]]] = ...,
        streams: _Optional[_Iterable[_Union[StreamResolver, _Mapping]]] = ...,
        sinks: _Optional[_Iterable[_Union[SinkResolver, _Mapping]]] = ...,
        charts: _Optional[_Iterable[_Union[Chart, _Mapping]]] = ...,
        config: _Optional[_Union[ProjectSettings, _Mapping]] = ...,
        failed: _Optional[_Iterable[_Union[FailedImport, _Mapping]]] = ...,
        chalkpy: _Optional[_Union[ChalkPYInfo, _Mapping]] = ...,
        validated: bool = ...,
        errors: _Optional[_Iterable[_Union[UpdateGraphError, _Mapping]]] = ...,
        cdc_sources: _Optional[_Iterable[_Union[CDCSource, _Mapping]]] = ...,
        sql_sources: _Optional[_Iterable[_Union[SQLSource, _Mapping]]] = ...,
        feature_classes: _Optional[_Iterable[_Union[FeatureClass, _Mapping]]] = ...,
        lsp: _Optional[_Union[Lsp, _Mapping]] = ...,
    ) -> None: ...
