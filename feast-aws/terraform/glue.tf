/*
    Required for Redshift spectrum to query files on S3
*/

resource "aws_glue_catalog_table" "zipcode_features_table" {
  name          = "zipcode_features"
  database_name = aws_athena_database.feast.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.feast_bucket.bucket}/data/zipcode_features/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "feast-aws-serde"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name = "zipcode"
      type = "bigint"
    }

    columns {
      name = "city"
      type = "string"
    }

    columns {
      name = "state"
      type = "string"
    }
    columns {
      name = "location_type"
      type = "string"
    }
    columns {
      name = "tax_returns_filed"
      type = "bigint"
    }
    columns {
      name = "population"
      type = "bigint"
    }
    columns {
      name = "total_wages"
      type = "bigint"
    }
    columns {
      name = "event_timestamp"
      type = "timestamp"
    }
    columns {
      name = "created_timestamp"
      type = "timestamp"
    }
  }

}


resource "aws_glue_catalog_table" "credit_history_table" {
  name          = "credit_history"
  database_name = aws_athena_database.feast.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.feast_bucket.bucket}/data/credit_history/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "feast-aws-serde"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name = "dob_ssn"
      type = "string"
    }

    columns {
      name = "credit_card_due"
      type = "bigint"
    }
    columns {
      name = "mortgage_due"
      type = "bigint"
    }
    columns {
      name = "student_loan_due"
      type = "bigint"
    }
    columns {
      name = "vehicle_loan_due"
      type = "bigint"
    }
    columns {
      name = "hard_pulls"
      type = "bigint"
    }
    columns {
      name = "missed_payments_2y"
      type = "bigint"
    }
    columns {
      name = "missed_payments_1y"
      type = "bigint"
    }
    columns {
      name = "missed_payments_6m"
      type = "bigint"
    }
    columns {
      name = "bankruptcies"
      type = "bigint"
    }
    columns {
      name = "event_timestamp"
      type = "timestamp"
    }
    columns {
      name = "created_timestamp"
      type = "timestamp"
    }
  }
}


# To test Loan table entity df
resource "aws_glue_catalog_table" "loan_entity_df" {
  name          = "entity_df"
  database_name = aws_athena_database.feast.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL              = "TRUE"
    "parquet.compression" = "SNAPPY"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.feast_bucket.bucket}/data/loan_features/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"

    ser_de_info {
      name                  = "feast-aws-serde"
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"

      parameters = {
        "serialization.format" = 1
      }
    }

    columns {
      name = "loan_id"
      type = "bigint"
    }

    columns {
      name = "dob_ssn"
      type = "string"
    }

    columns {
      name = "zipcode"
      type = "bigint"
    }

    columns {
      name = "person_age"
      type = "int"
    }

    columns {
      name = "person_income"
      type = "bigint"
    }

    columns {
      name = "person_home_ownership"
      type = "string"
    }

    columns {
      name = "person_emp_length"
      type = "double"
    }

    columns {
      name = "loan_intent"
      type = "string"
    }

    columns {
      name = "loan_amnt"
      type = "bigint"
    }

    columns {
      name = "loan_int_rate"
      type = "double"
    }

    columns {
      name = "loan_status"
      type = "int" # or boolean
    }

    columns {
      name = "event_timestamp"
      type = "timestamp"
    }

    columns {
      name = "created_timestamp"
      type = "timestamp"
    }
  }
}
