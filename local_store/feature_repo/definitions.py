from datetime import datetime, timedelta
from google.protobuf.duration_pb2 import Duration
from feast import Entity, Field, FeatureView, FileSource, ValueType
from feast.types import Float64, Int32, Int64

# Entity - patient in this case
patient = Entity(
    name="patient",
    value_type=ValueType.INT64,
    description="Patient",
    join_keys=["patient_id"],
)

# Declaring file source to later define feature views
source1 = FileSource(
    path="data/df1.parquet",
    event_timestamp_column="event_timestamp",
)

feature_view_1 = FeatureView(
    name="source1_feature_view",
    ttl=timedelta(days=90),
    entities=[patient],
    schema=[
        Field(name="mean radius", dtype=Float64),
        Field(name="mean texture", dtype=Float64),
        Field(name="mean perimeter", dtype=Float64),
        Field(name="mean area", dtype=Float64),
        Field(name="mean smoothness", dtype=Float64),
    ],
    source=source1,
)

source2 = FileSource(
    path="data/df2.parquet",
    event_timestamp_column="event_timestamp",
)


feature_view_2 = FeatureView(
    name="source2_feature_view",
    ttl=timedelta(days=90),
    entities=[patient],
    schema=[
        Field(name="mean compactness", dtype=Float64),
        Field(name="mean concavity", dtype=Float64),
        Field(name="mean concave points", dtype=Float64),
        Field(name="mean symmetry", dtype=Float64),
        Field(name="mean fractal dimension", dtype=Float64),
    ],
    source=source2,
)

source3 = FileSource(
    path="data/df3.parquet",
    event_timestamp_column="event_timestamp",
)

feature_view_3 = FeatureView(
    name="source3_feature_view",
    ttl=timedelta(days=90),
    entities=[patient],
    schema=[
        Field(name="radius error", dtype=Float64),
        Field(name="texture error", dtype=Float64),
        Field(name="perimeter error", dtype=Float64),
        Field(name="area error", dtype=Float64),
        Field(name="smoothness error", dtype=Float64),
        Field(name="compactness error", dtype=Float64),
        Field(name="concavity error", dtype=Float64),
    ],
    source=source3,
)

source4 = FileSource(
    path="data/df4.parquet",
    event_timestamp_column="event_timestamp",
)

feature_view_4 = FeatureView(
    name="source4_feature_view",
    ttl=timedelta(days=90),
    entities=[patient],
    schema=[
        Field(name="concave points error", dtype=Float64),
        Field(name="symmetry error", dtype=Float64),
        Field(name="fractal dimension error", dtype=Float64),
        Field(name="worst radius", dtype=Float64),
        Field(name="worst texture", dtype=Float64),
        Field(name="worst perimeter", dtype=Float64),
        Field(name="worst area", dtype=Float64),
        Field(name="worst smoothness", dtype=Float64),
        Field(name="worst compactness", dtype=Float64),
        Field(name="worst concavity", dtype=Float64),
        Field(name="worst concave points", dtype=Float64),
        Field(name="worst symmetry", dtype=Float64),
        Field(name="worst fractal dimension", dtype=Float64),
    ],
    source=source4,
)

target_source = FileSource(
    path="data/target.parquet",
    event_timestamp_column="event_timestamp",
)

target_feature_view = FeatureView(
    name="target_feature_view",
    entities=[patient],
    ttl=timedelta(days=90),
    schema=[Field(name="target", dtype=Int32)],
    source=target_source,
)
