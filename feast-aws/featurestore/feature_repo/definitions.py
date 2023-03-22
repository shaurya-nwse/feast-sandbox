from datetime import timedelta

from feast import Entity, Field, FeatureView, AthenaSource, ValueType
import feast.types

zipcode = Entity(
    name="zipcode",
    value_type=ValueType.INT64,
    description="Zipcode",
    join_keys=["zipcode"],
)

zipcode_source = AthenaSource(
    timestamp_field="event_timestamp",
    table="zipcode_features",
    database="feast",
    created_timestamp_column="created_timestamp",
    data_source="AwsDataCatalog",
    # No partitioning in this but can be added
    description="Zipcode Athena source",
    tags={"source": "athena", "format": "parquet", "team": "slam"},
    owner="shaurya.rawat@new-work.se",
)

zipcode_features = FeatureView(
    name="zipcode_features",
    entities=[zipcode],
    ttl=timedelta(days=3650),  # Computationally expensive, all days
    schema=[
        Field(name="city", dtype=feast.types.String),
        Field(name="state", dtype=feast.types.String),
        Field(name="location_type", dtype=feast.types.String),
        Field(name="tax_returns_filed", dtype=feast.types.Int64),
        Field(name="population", dtype=feast.types.Int64),
        Field(name="total_wages", dtype=feast.types.Int64),
    ],
    source=zipcode_source,
)

# 2nd entity
dob_ssn = Entity(
    name="dob_ssn",
    value_type=ValueType.STRING,
    description="Date of birth and social security",
    join_keys=["dob_ssn"],
)

credit_history_source = AthenaSource(
    timestamp_field="event_timestamp",
    table="credit_history",
    database="feast",
    data_source="AwsDataCatalog",
    created_timestamp_column="created_timestamp",
    description="Credit history athena source",
    tags={"source": "athena", "format": "parquet", "team": "slam"},
    owner="shaurya.rawat@new-work.se",
)

credit_history_features = FeatureView(
    name="credit_history_features",
    entities=[dob_ssn],
    ttl=timedelta(days=3650),
    schema=[
        Field(name="credit_card_due", dtype=feast.types.Int64),
        Field(name="mortgage_due", dtype=feast.types.Int64),
        Field(name="student_loan_due", dtype=feast.types.Int64),
        Field(name="vehicle_loan_due", dtype=feast.types.Int64),
        Field(name="hard_pulls", dtype=feast.types.Int64),
        Field(name="missed_payments_2y", dtype=feast.types.Int64),
        Field(name="missed_payments_1y", dtype=feast.types.Int64),
        Field(name="missed_payments_6m", dtype=feast.types.Int64),
        Field(name="bankruptcies", dtype=feast.types.Int64),
    ],
    source=credit_history_source,
)
