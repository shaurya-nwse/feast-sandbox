from datetime import datetime, timedelta
from google.protobuf.duration_pb2 import Duration
from feast import Entity, Feature, FeatureView, FileSource, ValueType


# Entity - patient in this case
patient = Entity(
    name="patient",
    value_type=ValueType.INT64,
    description="Patient",
    join_keys=["patient_id"],
)

# Declaring file source to later define feature views
source1 = FileSource(
    path="/Users/shaurya.rawat/Documents/mlplatform/feature-store/test_feast_2/feature_repo/data/df1.parquet",
    event_timestamp_column="event_timestamp",
)

feature_view_1 = FeatureView(
    name="source1_feature_view",
    ttl=timedelta(days=7),
)
