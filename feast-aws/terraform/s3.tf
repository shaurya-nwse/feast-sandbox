resource "aws_s3_bucket" "feast_bucket" {
  bucket        = "${var.application}-bucket"
  acl           = "private"
  force_destroy = true

  lifecycle_rule {
    id      = "raw-data"
    enabled = true

    prefix = "/"
    tags = {
      "rule"    = "raw-data"
      autoclean = "true"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 200
    }
  }
}

# Upload data
resource "aws_s3_bucket_object" "upload_zipcode_data" {
  bucket = aws_s3_bucket.feast_bucket.bucket
  key    = "data/zipcode_features/table.parquet"
  source = "${path.root}/../data/zipcode_table.parquet"
}

resource "aws_s3_bucket_object" "upload_credit_history" {
  bucket = aws_s3_bucket.feast_bucket.bucket
  key    = "data/credit_history/table.parquet"
  source = "${path.root}/../data/credit_history.parquet"
}

resource "aws_s3_bucket_object" "upload_loan_table" {
  bucket = aws_s3_bucket.feast_bucket.bucket
  key    = "data/loan_features/table.parquet"
  source = "${path.root}/../data/loan_table.parquet"
}

