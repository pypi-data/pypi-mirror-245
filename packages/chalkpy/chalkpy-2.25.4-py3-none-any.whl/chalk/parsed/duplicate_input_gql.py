import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

import dataclasses_json

from chalk.parsed.proto import graph_pb2


class Protobufable(ABC):
    @abstractmethod
    def to_proto(self) -> Any:
        raise NotImplementedError


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureIdGQL(Protobufable):
    fqn: str
    name: str
    namespace: str
    isPrimary: bool
    className: Optional[str] = None
    attributeName: Optional[str] = None
    explicitNamespace: Optional[bool] = None

    def to_proto(self) -> graph_pb2.FeatureId:
        return graph_pb2.FeatureId(
            fqn=self.fqn,
            name=self.name,
            namespace=self.namespace,
            is_primary=self.isPrimary,
            class_name=self.className,
            attribute_name=self.attributeName,
            explicit_namespace=self.explicitNamespace,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertReferencePathComponentGQL(Protobufable):
    parent: UpsertFeatureIdGQL
    child: UpsertFeatureIdGQL
    parentToChildAttributeName: str

    def to_proto(self) -> graph_pb2.ReferencePathComponent:
        return graph_pb2.ReferencePathComponent(
            parent=self.parent.to_proto(),
            child=self.child.to_proto(),
            parent_to_child_attribute_name=self.parentToChildAttributeName,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertFilterGQL(Protobufable):
    lhs: UpsertFeatureIdGQL
    op: str
    rhs: UpsertFeatureIdGQL

    def to_proto(self) -> graph_pb2.Filter:
        return graph_pb2.Filter(
            lhs=self.lhs.to_proto(),
            op=self.op,
            rhs=self.rhs.to_proto(),
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertDataFrameGQL(Protobufable):
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None

    def to_proto(self) -> graph_pb2.DataFrame:
        columns = [c.to_proto() for c in self.columns] if self.columns is not None else None
        filters = [f.to_proto() for f in self.filters] if self.filters is not None else None
        return graph_pb2.DataFrame(
            columns=columns,
            filters=filters,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureReferenceGQL(Protobufable):
    underlying: UpsertFeatureIdGQL
    path: Optional[List[UpsertReferencePathComponentGQL]] = None

    def to_proto(self) -> graph_pb2.FeatureReference:
        path = [p.to_proto() for p in self.path] if self.path is not None else None
        return graph_pb2.FeatureReference(
            underlying=self.underlying.to_proto(),
            path=path,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertHasOneKindGQL(Protobufable):
    join: UpsertFilterGQL

    def to_proto(self) -> graph_pb2.HasOneKind:
        return graph_pb2.HasOneKind(
            join=self.join.to_proto(),
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertHasManyKindGQL(Protobufable):
    join: UpsertFilterGQL
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None

    def to_proto(self) -> graph_pb2.HasManyKind:
        return graph_pb2.HasManyKind(
            join=self.join.to_proto(),
            columns=[c.to_proto() for c in self.columns] if self.columns is not None else None,
            filters=[f.to_proto() for f in self.filters] if self.filters is not None else None,
        )


@dataclasses_json.dataclass_json
@dataclass
class VersionInfoGQL(Protobufable):
    version: int
    maximum: int
    default: int
    versions: List[str]

    def to_proto(self) -> graph_pb2.VersionInfo:
        return graph_pb2.VersionInfo(
            version=self.version,
            maximum=self.maximum,
            default=self.default,
            versions=self.versions,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertScalarKindGQL(Protobufable):
    primary: bool
    dtype: Optional[str] = None  # The JSON-serialized form of the chalk.features.SerializedDType model
    version: Optional[int] = None  # Deprecated. Use the `versionInfo` instead
    versionInfo: Optional[VersionInfoGQL] = None
    baseClasses: Optional[List[str]] = None  # Deprecated. Use the `dtype` instead
    hasEncoderAndDecoder: bool = False  # Deprecated. Use the `dtype` instead
    scalarKind: Optional[str] = None  # Deprecated. Use the `dtype` instead

    def to_proto(self) -> graph_pb2.ScalarKind:
        return graph_pb2.ScalarKind(
            primary=self.primary,
            dtype=self.dtype,
            version=self.version,
            version_info=self.versionInfo.to_proto() if self.versionInfo else None,
            base_classes=self.baseClasses,
            has_encoder_and_decoder=self.hasEncoderAndDecoder,
            scalar_kind=self.scalarKind,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureTimeKindGQL(Protobufable):
    format: Optional[str] = None

    def to_proto(self) -> graph_pb2.FeatureTimeKind:
        return graph_pb2.FeatureTimeKind(
            format=self.format,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertFeatureGQL(Protobufable):
    id: UpsertFeatureIdGQL

    scalarKind: Optional[UpsertScalarKindGQL] = None
    hasManyKind: Optional[UpsertHasManyKindGQL] = None
    hasOneKind: Optional[UpsertHasOneKindGQL] = None
    featureTimeKind: Optional[UpsertFeatureTimeKindGQL] = None
    etlOfflineToOnline: bool = False
    windowBuckets: Optional[List[float]] = None

    tags: Optional[List[str]] = None
    maxStaleness: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None

    namespacePath: Optional[str] = None
    isSingleton: Optional[bool] = None

    def to_proto(self) -> graph_pb2.Feature:
        scalar_kind = self.scalarKind.to_proto() if self.scalarKind else None
        has_many_kind = self.hasManyKind.to_proto() if self.hasManyKind else None
        has_one_kind = self.hasOneKind.to_proto() if self.hasOneKind else None
        feature_time_kind = self.featureTimeKind.to_proto() if self.featureTimeKind else None
        return graph_pb2.Feature(
            id=self.id.to_proto(),
            scalar_kind=scalar_kind,
            has_many_kind=has_many_kind,
            has_one_kind=has_one_kind,
            feature_time_kind=feature_time_kind,
            etl_offline_to_online=self.etlOfflineToOnline,
            window_buckets=self.windowBuckets,
            tags=self.tags,
            max_staleness=self.maxStaleness,
            description=self.description,
            owner=self.owner,
            namespace_path=self.namespacePath,
            is_singleton=self.isSingleton,
        )


@dataclasses_json.dataclass_json
@dataclass
class KafkaConsumerConfigGQL(Protobufable):
    broker: List[str]
    topic: List[str]
    sslKeystoreLocation: Optional[str]
    clientIdPrefix: Optional[str]
    groupIdPrefix: Optional[str]
    topicMetadataRefreshIntervalMs: Optional[int]
    securityProtocol: Optional[str]

    def to_proto(self) -> graph_pb2.KafkaConsumerConfig:
        return graph_pb2.KafkaConsumerConfig(
            broker=self.broker,
            topic=self.topic,
            ssl_keystore_location=self.sslKeystoreLocation,
            client_id_prefix=self.clientIdPrefix,
            group_id_prefix=self.groupIdPrefix,
            topic_metadata_refresh_interval_ms=self.topicMetadataRefreshIntervalMs,
            security_protocol=self.securityProtocol,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamMessageGQL(Protobufable):
    """
    GQL split union input pattern
    """

    name: str
    typeName: str
    bases: List[str]
    schema: Optional[Any] = None

    def to_proto(self) -> graph_pb2.StreamResolverParamMessage:
        return graph_pb2.StreamResolverParamMessage(
            name=self.name,
            type_name=self.typeName,
            bases=self.bases,
            schema=json.dumps(self.schema),
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamKeyedStateGQL(Protobufable):
    """
    GQL split union input pattern
    """

    name: str
    typeName: str
    bases: List[str]
    schema: Optional[Any] = None
    defaultValue: Optional[Any] = None

    def to_proto(self) -> graph_pb2.StreamResolverParamKeyedState:
        return graph_pb2.StreamResolverParamKeyedState(
            name=self.name,
            type_name=self.typeName,
            bases=self.bases,
            schema=json.dumps(self.schema),
            default_value=json.dumps(self.defaultValue),
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverParamGQL(Protobufable):
    message: Optional[UpsertStreamResolverParamMessageGQL]
    state: Optional[UpsertStreamResolverParamKeyedStateGQL]

    def to_proto(self) -> graph_pb2.StreamResolverParam:
        message = self.message.to_proto() if self.message else None
        state = self.state.to_proto() if self.state else None
        return graph_pb2.StreamResolverParam(
            message=message,
            state=state,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertStreamResolverGQL(Protobufable):
    fqn: str
    kind: str
    functionDefinition: str
    sourceClassName: Optional[str] = None
    sourceConfig: Optional[Any] = None
    machineType: Optional[str] = None
    environment: Optional[List[str]] = None
    output: Optional[List[UpsertFeatureIdGQL]] = None
    inputs: Optional[List[UpsertStreamResolverParamGQL]] = None
    doc: Optional[str] = None
    owner: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None

    def to_proto(self) -> graph_pb2.StreamResolver:
        output = [o.to_proto() for o in self.output] if self.output is not None else None
        inputs = [i.to_proto() for i in self.inputs] if self.inputs is not None else None
        return graph_pb2.StreamResolver(
            fqn=self.fqn,
            kind=self.kind,
            function_definition=self.functionDefinition,
            source_class_name=self.sourceClassName,
            source_config=json.dumps(self.sourceConfig),
            machine_type=self.machineType,
            environment=self.environment,
            output=output,
            inputs=inputs,
            doc=self.doc,
            owner=self.owner,
            filename=self.filename,
            source_line=self.sourceLine,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverOutputGQL(Protobufable):
    features: Optional[List[UpsertFeatureIdGQL]] = None
    dataframes: Optional[List[UpsertDataFrameGQL]] = None

    def to_proto(self) -> graph_pb2.ResolverOutput:
        features = [f.to_proto() for f in self.features] if self.features is not None else None
        dataframes = [d.to_proto() for d in self.dataframes] if self.dataframes is not None else None
        return graph_pb2.ResolverOutput(
            features=features,
            dataframes=dataframes,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverInputUnionGQL(Protobufable):
    feature: Optional[UpsertFeatureReferenceGQL] = None
    dataframe: Optional[UpsertDataFrameGQL] = None
    pseudoFeature: Optional[UpsertFeatureReferenceGQL] = None

    def to_proto(self) -> graph_pb2.ResolverInputUnion:
        feature = self.feature.to_proto() if self.feature else None
        dataframe = self.dataframe.to_proto() if self.dataframe else None
        pseudo_feature = self.pseudoFeature.to_proto() if self.pseudoFeature else None
        return graph_pb2.ResolverInputUnion(
            feature=feature,
            dataframe=dataframe,
            pseudo_feature=pseudo_feature,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertResolverGQL(Protobufable):
    fqn: str
    kind: str
    functionDefinition: str
    output: UpsertResolverOutputGQL
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    cron: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    allInputs: Optional[List[UpsertResolverInputUnionGQL]] = None
    machineType: Optional[str] = None
    owner: Optional[str] = None
    timeout: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None
    dataSources: Optional[List[Any]] = None

    def to_proto(self) -> graph_pb2.Resolver:
        ds = []
        for d in self.dataSources or []:
            if not "name" in d or not "kind" in d:
                raise Exception("Data source must have name and kind")
            ds.append(graph_pb2.DataSource(name=d["name"], kind=d["kind"]))

        return graph_pb2.Resolver(
            fqn=self.fqn,
            kind=self.kind,
            function_definition=self.functionDefinition,
            output=self.output.to_proto(),
            environment=self.environment,
            tags=self.tags,
            doc=self.doc,
            cron=self.cron,
            inputs=[i.to_proto() for i in self.inputs] if self.inputs else None,
            all_inputs=[i.to_proto() for i in self.allInputs] if self.allInputs else None,
            machine_type=self.machineType,
            owner=self.owner,
            timeout=self.timeout,
            filename=self.filename,
            source_line=self.sourceLine,
            data_sources=ds,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertSinkResolverGQL(Protobufable):
    fqn: str
    functionDefinition: str
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    machineType: Optional[str] = None
    bufferSize: Optional[int] = None
    debounce: Optional[str] = None
    maxDelay: Optional[str] = None
    upsert: Optional[bool] = None
    owner: Optional[str] = None
    filename: Optional[str] = None
    sourceLine: Optional[int] = None

    def to_proto(self) -> graph_pb2.SinkResolver:
        return graph_pb2.SinkResolver(
            fqn=self.fqn,
            function_definition=self.functionDefinition,
            environment=self.environment,
            tags=self.tags,
            doc=self.doc,
            inputs=[i.to_proto() for i in self.inputs] if self.inputs is not None else None,
            machine_type=self.machineType,
            buffer_size=self.bufferSize,
            debounce=self.debounce,
            max_delay=self.maxDelay,
            upsert=self.upsert,
            owner=self.owner,
            filename=self.filename,
            source_line=self.sourceLine,
        )


@dataclasses_json.dataclass_json
@dataclass
class MetadataSettings:
    name: str
    missing: str

    def to_proto(self) -> graph_pb2.MetadataSettings:
        return graph_pb2.MetadataSettings(
            name=self.name,
            missing=self.missing,
        )


@dataclasses_json.dataclass_json
@dataclass
class FeatureSettings:
    metadata: Optional[List[MetadataSettings]] = None

    def to_proto(self) -> graph_pb2.FeatureSettings:
        metadata = [m.to_proto() for m in self.metadata] if self.metadata is not None else None
        return graph_pb2.FeatureSettings(
            metadata=metadata,
        )


@dataclasses_json.dataclass_json
@dataclass
class ResolverSettings:
    metadata: Optional[List[MetadataSettings]] = None

    def to_proto(self) -> graph_pb2.ResolverSettings:
        metadata = [m.to_proto() for m in self.metadata] if self.metadata is not None else None
        return graph_pb2.ResolverSettings(
            metadata=metadata,
        )


@dataclasses_json.dataclass_json
@dataclass
class ValidationSettings:
    feature: Optional[FeatureSettings] = None
    resolver: Optional[ResolverSettings] = None

    def to_proto(self) -> graph_pb2.ValidationSettings:
        feature = self.feature.to_proto() if self.feature else None
        resolver = self.resolver.to_proto() if self.resolver else None
        return graph_pb2.ValidationSettings(
            feature=feature,
            resolver=resolver,
        )


@dataclasses_json.dataclass_json
@dataclass
class EnvironmentSettingsGQL(Protobufable):
    id: str
    runtime: Optional[str]
    requirements: Optional[str]
    dockerfile: Optional[str]
    requiresPackages: Optional[List[str]] = None

    def to_proto(self) -> graph_pb2.EnvironmentSettings:
        return graph_pb2.EnvironmentSettings(
            id=self.id,
            runtime=self.runtime,
            requirements=self.requirements,
            dockerfile=self.dockerfile,
            requires_packages=self.requiresPackages,
        )


@dataclasses_json.dataclass_json
@dataclass
class ProjectSettingsGQL(Protobufable):
    project: str
    environments: Optional[List[EnvironmentSettingsGQL]]
    validation: Optional[ValidationSettings] = None

    def to_proto(self) -> graph_pb2.ProjectSettings:
        environments = [e.to_proto() for e in self.environments] if self.environments is not None else None
        validation = self.validation.to_proto() if self.validation else None
        return graph_pb2.ProjectSettings(
            project=self.project,
            environments=environments,
            validation=validation,
        )


@dataclasses_json.dataclass_json
@dataclass
class FailedImport:
    filename: str
    module: str
    traceback: str

    def to_proto(self) -> graph_pb2.FailedImport:
        return graph_pb2.FailedImport(
            filename=self.filename,
            module=self.module,
            traceback=self.traceback,
        )


@dataclasses_json.dataclass_json
@dataclass
class ChalkPYInfo:
    version: str
    python: Optional[str] = None

    def to_proto(self) -> graph_pb2.ChalkPYInfo:
        return graph_pb2.ChalkPYInfo(
            version=self.version,
            python=self.python,
        )


class MetricKindGQL(str, Enum):
    __metaclass__ = Protobufable
    FEATURE_REQUEST_COUNT = "FEATURE_REQUEST_COUNT"
    FEATURE_LATENCY = "FEATURE_LATENCY"
    FEATURE_STALENESS = "FEATURE_STALENESS"
    FEATURE_VALUE = "FEATURE_VALUE"
    FEATURE_WRITE = "FEATURE_WRITE"
    FEATURE_NULL_RATIO = "FEATURE_NULL_RATIO"

    RESOLVER_REQUEST_COUNT = "RESOLVER_REQUEST_COUNT"
    RESOLVER_LATENCY = "RESOLVER_LATENCY"
    RESOLVER_SUCCESS_RATIO = "RESOLVER_SUCCESS_RATIO"

    QUERY_COUNT = "QUERY_COUNT"
    QUERY_LATENCY = "QUERY_LATENCY"
    QUERY_SUCCESS_RATIO = "QUERY_SUCCESS_RATIO"

    BILLING_INFERENCE = "BILLING_INFERENCE"
    BILLING_CRON = "BILLING_CRON"
    BILLING_MIGRATION = "BILLING_MIGRATION"

    CRON_COUNT = "CRON_COUNT"
    CRON_LATENCY = "CRON_LATENCY"

    STREAM_MESSAGES_PROCESSED = "STREAM_MESSAGES_PROCESSED"
    STREAM_MESSAGE_LATENCY = "STREAM_MESSAGE_LATENCY"

    STREAM_WINDOWS_PROCESSED = "STREAM_WINDOWS_PROCESSED"
    STREAM_WINDOW_LATENCY = "STREAM_WINDOW_LATENCY"

    def to_proto(self) -> graph_pb2.MetricKind:
        return graph_pb2.MetricKind.Value("METRIC_KIND_" + self.value.upper())


class FilterKindGQL(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    FEATURE_TAG = "FEATURE_TAG"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"
    RESOLVER_TAG = "RESOLVER_TAG"

    CRON_STATUS = "CRON_STATUS"
    MIGRATION_STATUS = "MIGRATION_STATUS"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"
    OPERATION_ID = "OPERATION_ID"

    QUERY_NAME = "QUERY_NAME"
    QUERY_STATUS = "QUERY_STATUS"

    IS_NULL = "IS_NULL"

    def to_proto(self) -> graph_pb2.FilterKind:
        return graph_pb2.FilterKind.Value("FILTER_KIND_" + self.value.upper())


class ComparatorKindGQL(str, Enum):
    EQ = "EQ"
    NEQ = "NEQ"
    ONE_OF = "ONE_OF"

    def to_proto(self) -> graph_pb2.ComparatorKind:
        return graph_pb2.ComparatorKind.Value("COMPARATOR_KIND_" + self.value.upper())


class WindowFunctionKindGQL(str, Enum):
    COUNT = "COUNT"
    MEAN = "MEAN"
    SUM = "SUM"
    MIN = "MIN"
    MAX = "MAX"

    PERCENTILE_99 = "PERCENTILE_99"
    PERCENTILE_95 = "PERCENTILE_95"
    PERCENTILE_75 = "PERCENTILE_75"
    PERCENTILE_50 = "PERCENTILE_50"
    PERCENTILE_25 = "PERCENTILE_25"
    PERCENTILE_5 = "PERCENTILE_5"

    ALL_PERCENTILES = "ALL_PERCENTILES"

    def to_proto(self) -> graph_pb2.WindowFunctionKind:
        return graph_pb2.WindowFunctionKind.Value("WINDOW_FUNCTION_KIND_" + self.value.upper())


class GroupByKindGQL(str, Enum):
    FEATURE_STATUS = "FEATURE_STATUS"
    FEATURE_NAME = "FEATURE_NAME"
    IS_NULL = "IS_NULL"

    RESOLVER_STATUS = "RESOLVER_STATUS"
    RESOLVER_NAME = "RESOLVER_NAME"

    QUERY_STATUS = "QUERY_STATUS"
    QUERY_NAME = "QUERY_NAME"

    ONLINE_OFFLINE = "ONLINE_OFFLINE"
    CACHE_HIT = "CACHE_HIT"

    def to_proto(self) -> graph_pb2.GroupByKind:
        return graph_pb2.GroupByKind.Value("GROUP_BY_KIND_" + self.value.upper())


class MetricFormulaKindGQL(str, Enum):
    SUM = "SUM"
    TOTAL_RATIO = "TOTAL_RATIO"
    RATIO = "RATIO"
    PRODUCT = "PRODUCT"
    ABS = "ABS"
    KS_STAT = "KS_STAT"
    KS_TEST = "KS_TEST"
    KS_THRESHOLD = "KS_THRESHOLD"
    TIME_OFFSET = "TIME_OFFSET"

    def to_proto(self) -> graph_pb2.MetricFormulaKind:
        return graph_pb2.MetricFormulaKind.Value("METRIC_FORMULA_KIND_" + self.value.upper())


class AlertSeverityKindGQL(str, Enum):
    critical = "critical"
    error = "error"
    warning = "warning"
    info = "info"

    def to_proto(self) -> graph_pb2.AlertSeverityKind:
        return graph_pb2.AlertSeverityKind.Value("ALERT_SEVERITY_KIND_" + self.value.upper())


class ThresholdKindGQL(str, Enum):
    ABOVE = "ABOVE"
    BELOW = "BELOW"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"

    def to_proto(self) -> graph_pb2.ThresholdKind:
        return graph_pb2.ThresholdKind.Value("THRESHOLD_KIND_" + self.value.upper())


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricFilterGQL(Protobufable):
    kind: FilterKindGQL
    comparator: ComparatorKindGQL
    value: List[str]

    def to_proto(self) -> graph_pb2.MetricFilter:
        return graph_pb2.MetricFilter(
            kind=self.kind.to_proto(),
            comparator=self.comparator.to_proto(),
            value=self.value,
        )


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricConfigSeriesGQL(Protobufable):
    metric: MetricKindGQL
    filters: List[CreateMetricFilterGQL]
    name: Optional[str] = None
    windowFunction: Optional[WindowFunctionKindGQL] = None
    groupBy: Optional[List[GroupByKindGQL]] = None

    def to_proto(self) -> graph_pb2.MetricConfigSeries:
        filters = [f.to_proto() for f in self.filters]
        group_by = [g.to_proto() for g in self.groupBy] if self.groupBy is not None else None
        return graph_pb2.MetricConfigSeries(
            metric=self.metric.to_proto(),
            filters=filters,
            name=self.name,
            window_function=self.windowFunction.to_proto() if self.windowFunction else None,
            group_by=group_by,
        )


@dataclasses_json.dataclass_json
@dataclass
class CreateDatasetFeatureOperandGQL(Protobufable):
    """
    Can't do a Tuple[int, str] so we're going to use a wrapper
    """

    dataset: str
    feature: str

    def to_proto(self) -> graph_pb2.DatasetFeatureOperand:
        return graph_pb2.DatasetFeatureOperand(
            dataset=self.dataset,
            feature=self.feature,
        )


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricFormulaGQL(Protobufable):
    """
    No input unions in graphql means we have to use parallel optional input keys
    and do additional validation work ourselves
    """

    kind: MetricFormulaKindGQL
    # ----- Input Union ------
    singleSeriesOperands: Optional[int]  # index of a single series
    multiSeriesOperands: Optional[List[int]]  # index of multiple series
    datasetFeatureOperands: Optional[CreateDatasetFeatureOperandGQL]  # dataset id and feature name
    # ----- End Union  ------
    name: Optional[str] = None

    def to_proto(self) -> graph_pb2.MetricFormula:
        return graph_pb2.MetricFormula(
            kind=self.kind.to_proto(),
            single_series_operands=self.singleSeriesOperands,
            multi_series_operands=self.multiSeriesOperands,
            dataset_feature_operands=self.datasetFeatureOperands.to_proto() if self.datasetFeatureOperands else None,
            name=self.name,
        )


@dataclasses_json.dataclass_json
@dataclass
class CreateAlertTriggerGQL(Protobufable):
    name: str
    severity: AlertSeverityKindGQL
    thresholdPosition: ThresholdKindGQL
    thresholdValue: float
    seriesName: Optional[str] = None
    channelName: Optional[str] = None
    description: Optional[str] = None

    def to_proto(self) -> graph_pb2.AlertTrigger:
        return graph_pb2.AlertTrigger(
            name=self.name,
            severity=self.severity.to_proto(),
            threshold_position=self.thresholdPosition.to_proto(),
            threshold_value=self.thresholdValue,
            series_name=self.seriesName,
            channel_name=self.channelName,
            description=self.description,
        )


@dataclasses_json.dataclass_json
@dataclass
class CreateMetricConfigGQL(Protobufable):
    name: str
    windowPeriod: str
    series: List[CreateMetricConfigSeriesGQL]
    formulas: Optional[List[CreateMetricFormulaGQL]] = None
    trigger: Optional[CreateAlertTriggerGQL] = None

    def to_proto(self) -> graph_pb2.MetricConfig:
        series = [s.to_proto() for s in self.series]
        formulas = [f.to_proto() for f in self.formulas] if self.formulas is not None else None
        trigger = self.trigger.to_proto() if self.trigger else None
        return graph_pb2.MetricConfig(
            name=self.name,
            window_period=self.windowPeriod,
            series=series,
            formulas=formulas,
            trigger=trigger,
        )


@dataclasses_json.dataclass_json
@dataclass
class CreateChartGQL(Protobufable):
    id: str
    config: CreateMetricConfigGQL
    entityKind: str
    entityId: Optional[str] = None

    def to_proto(self) -> graph_pb2.Chart:
        return graph_pb2.Chart(
            id=self.id,
            config=self.config.to_proto(),
            entity_kind=self.entityKind,
            entity_id=self.entityId,
        )


class GraphLogSeverity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"

    def to_proto(self) -> graph_pb2.GraphLogSeverity:
        return graph_pb2.GraphLogSeverity.Value("GRAPH_LOG_SEVERITY_" + self.value)


@dataclasses_json.dataclass_json
@dataclass
class UpdateGraphError:
    header: str
    subheader: str
    severity: GraphLogSeverity

    def to_proto(self) -> graph_pb2.UpdateGraphError:
        return graph_pb2.UpdateGraphError(
            header=self.header,
            subheader=self.subheader,
            severity=self.severity.to_proto(),
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertSQLSourceGQL(Protobufable):
    name: Optional[str]
    kind: str

    def to_proto(self) -> graph_pb2.SQLSource:
        return graph_pb2.SQLSource(
            name=self.name,
            kind=self.kind,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertCDCSourceGQL(Protobufable):
    integrationName: str
    schemaDotTableList: List[str]

    def to_proto(self) -> graph_pb2.CDCSource:
        return graph_pb2.CDCSource(
            integration_name=self.integrationName,
            schema_dot_table_list=self.schemaDotTableList,
        )


@dataclasses_json.dataclass_json
@dataclass
class FeatureClassGQL(Protobufable):
    isSingleton: bool
    doc: Optional[str]
    name: str
    owner: Optional[str]
    tags: List[str]

    def to_proto(self) -> graph_pb2.FeatureClass:
        return graph_pb2.FeatureClass(
            is_singleton=self.isSingleton,
            doc=self.doc,
            name=self.name,
            owner=self.owner,
            tags=self.tags,
        )


@dataclasses_json.dataclass_json
@dataclass
class PositionGQL(Protobufable):
    """Mirrors an LSP Position

    https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#position
    """

    line: int
    """Line position in a document (one-based)."""

    character: int
    """Character offset on a line in a document (zero-based)."""

    def to_proto(self) -> graph_pb2.Position:
        return graph_pb2.Position(
            line=self.line,
            character=self.character,
        )


@dataclasses_json.dataclass_json
@dataclass
class RangeGQL(Protobufable):
    """Mirrors an LSP Range

    https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#range
    """

    start: PositionGQL
    end: PositionGQL

    def to_proto(self) -> graph_pb2.Range:
        return graph_pb2.Range(
            start=self.start.to_proto(),
            end=self.end.to_proto(),
        )


class DiagnosticSeverityGQL(str, Enum):
    """Mirrors an LSP DiagnosticSeverity"""

    Error = "Error"
    Warning = "Warning"
    Information = "Information"
    Hint = "Hint"

    def to_proto(self) -> graph_pb2.DiagnosticSeverity:
        return graph_pb2.DiagnosticSeverity.Value("DIAGNOSTIC_SEVERITY_" + self.value.upper())


@dataclasses_json.dataclass_json
@dataclass
class CodeDescriptionGQL(Protobufable):
    href: str

    def to_proto(self) -> graph_pb2.CodeDescription:
        return graph_pb2.CodeDescription(
            href=self.href,
        )


@dataclasses_json.dataclass_json
@dataclass
class LocationGQL(Protobufable):
    uri: str
    range: RangeGQL

    def to_proto(self) -> graph_pb2.Location:
        return graph_pb2.Location(
            uri=self.uri,
            range=self.range.to_proto(),
        )


@dataclasses_json.dataclass_json
@dataclass
class DiagnosticRelatedInformationGQL(Protobufable):
    location: LocationGQL
    """The location of this related diagnostic information."""

    message: str
    """The message of this related diagnostic information."""

    def to_proto(self) -> graph_pb2.DiagnosticRelatedInformation:
        return graph_pb2.DiagnosticRelatedInformation(
            location=self.location.to_proto(),
            message=self.message,
        )


@dataclasses_json.dataclass_json
@dataclass
class DiagnosticGQL(Protobufable):
    range: RangeGQL
    message: str
    severity: Optional[DiagnosticSeverityGQL]
    code: Optional[str]
    codeDescription: Optional[CodeDescriptionGQL]
    relatedInformation: Optional[List[DiagnosticRelatedInformationGQL]] = None

    def to_proto(self) -> graph_pb2.Diagnostic:
        related_information = (
            [r.to_proto() for r in self.relatedInformation] if self.relatedInformation is not None else None
        )
        return graph_pb2.Diagnostic(
            range=self.range.to_proto(),
            message=self.message,
            severity=self.severity.to_proto() if self.severity else None,
            code=self.code,
            code_description=self.codeDescription.to_proto() if self.codeDescription else None,
            related_information=related_information,
        )


@dataclasses_json.dataclass_json
@dataclass
class PublishDiagnosticsParams:
    """Mirrors an LSP PublishDiagnosticsParams

    https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#publishDiagnosticsParams
    """

    uri: str
    diagnostics: List[DiagnosticGQL]

    def to_proto(self) -> graph_pb2.PublishDiagnosticsParams:
        diagnostics = [d.to_proto() for d in self.diagnostics]
        return graph_pb2.PublishDiagnosticsParams(
            uri=self.uri,
            diagnostics=diagnostics,
        )


@dataclasses_json.dataclass_json
@dataclass
class TextDocumentIdentifierGQL(Protobufable):
    uri: str

    def to_proto(self) -> graph_pb2.TextDocumentIdentifier:
        return graph_pb2.TextDocumentIdentifier(
            uri=self.uri,
        )


@dataclasses_json.dataclass_json
@dataclass
class TextEditGQL(Protobufable):
    range: RangeGQL
    newText: str

    def to_proto(self) -> graph_pb2.TextEdit:
        return graph_pb2.TextEdit(
            range=self.range.to_proto(),
            new_text=self.newText,
        )


@dataclasses_json.dataclass_json
@dataclass
class TextDocumentEditGQL(Protobufable):
    textDocument: TextDocumentIdentifierGQL
    edits: List[TextEditGQL]

    def to_proto(self) -> graph_pb2.TextDocumentEdit:
        edits = [e.to_proto() for e in self.edits]
        return graph_pb2.TextDocumentEdit(
            text_document=self.textDocument.to_proto(),
            edits=edits,
        )


@dataclasses_json.dataclass_json
@dataclass
class WorkspaceEditGQL(Protobufable):
    documentChanges: List[TextDocumentEditGQL]

    def to_proto(self) -> graph_pb2.WorkspaceEdit:
        document_changes = [d.to_proto() for d in self.documentChanges]
        return graph_pb2.WorkspaceEdit(
            document_changes=document_changes,
        )


@dataclasses_json.dataclass_json
@dataclass
class CodeActionGQL(Protobufable):
    title: str
    diagnostics: Optional[List[DiagnosticGQL]]
    edit: WorkspaceEditGQL

    def to_proto(self) -> graph_pb2.CodeAction:
        diagnostics = [d.to_proto() for d in self.diagnostics] if self.diagnostics is not None else None
        return graph_pb2.CodeAction(
            title=self.title,
            diagnostics=diagnostics,
            edit=self.edit.to_proto(),
        )


@dataclasses_json.dataclass_json
@dataclass
class LspGQL(Protobufable):
    diagnostics: List[PublishDiagnosticsParams]
    actions: List[CodeActionGQL]

    def to_proto(self) -> graph_pb2.Lsp:
        diagnostics = [d.to_proto() for d in self.diagnostics]
        actions = [a.to_proto() for a in self.actions]
        return graph_pb2.Lsp(
            diagnostics=diagnostics,
            actions=actions,
        )


@dataclasses_json.dataclass_json
@dataclass
class UpsertGraphGQL(Protobufable):
    resolvers: Optional[List[UpsertResolverGQL]] = None
    features: Optional[List[UpsertFeatureGQL]] = None
    streams: Optional[List[UpsertStreamResolverGQL]] = None
    sinks: Optional[List[UpsertSinkResolverGQL]] = None
    charts: Optional[List[CreateChartGQL]] = None
    config: Optional[ProjectSettingsGQL] = None
    failed: Optional[List[FailedImport]] = None
    chalkpy: Optional[ChalkPYInfo] = None
    validated: Optional[bool] = None
    errors: Optional[List[UpdateGraphError]] = None
    cdcSources: Optional[List[UpsertCDCSourceGQL]] = None
    sqlSources: Optional[List[UpsertSQLSourceGQL]] = None
    featureClasses: Optional[List[FeatureClassGQL]] = None
    lsp: Optional[LspGQL] = None

    def to_proto(self) -> graph_pb2.Graph:
        resolvers = [r.to_proto() for r in self.resolvers] if self.resolvers is not None else None
        features = [f.to_proto() for f in self.features] if self.features is not None else None
        streams = [s.to_proto() for s in self.streams] if self.streams is not None else None
        sinks = [s.to_proto() for s in self.sinks] if self.sinks is not None else None
        charts = [c.to_proto() for c in self.charts] if self.charts is not None else None
        config = self.config.to_proto() if self.config is not None else None
        failed = [f.to_proto() for f in self.failed] if self.failed is not None else None
        chalkpy = self.chalkpy.to_proto() if self.chalkpy else None
        validated = self.validated if self.validated is not None else None
        errors = [e.to_proto() for e in self.errors] if self.errors is not None else None
        cdc_sources = [s.to_proto() for s in self.cdcSources] if self.cdcSources is not None else None
        sql_sources = [s.to_proto() for s in self.sqlSources] if self.sqlSources is not None else None
        feature_classes = [f.to_proto() for f in self.featureClasses] if self.featureClasses is not None else None
        lsp = self.lsp.to_proto() if self.lsp is not None else None
        return graph_pb2.Graph(
            resolvers=resolvers,
            features=features,
            streams=streams,
            sinks=sinks,
            charts=charts,
            config=config,
            failed=failed,
            chalkpy=chalkpy,
            validated=validated,
            errors=errors,
            cdc_sources=cdc_sources,
            sql_sources=sql_sources,
            feature_classes=feature_classes,
            lsp=lsp,
        )
