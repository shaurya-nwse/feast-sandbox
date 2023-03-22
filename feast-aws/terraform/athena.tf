resource "aws_athena_workgroup" "feast" {
  name = "feast"

  configuration {
    enforce_workgroup_configuration    = false
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.feast_bucket.id}/output/"

      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }
  }

  force_destroy = true
}

resource "aws_athena_database" "feast" {
  name   = "feast"
  bucket = aws_s3_bucket.feast_bucket.id

  comment       = "Athena workshop"
  force_destroy = true
}
