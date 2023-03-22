# # Redshift Spectrum role to access S3
# # Needs s3 spectrum role, s3 access, glue console access and Redshift service role
# resource "aws_iam_role" "s3_spectrum_role" {
#   name = "s3_spectrum_role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [{
#       Effect = "Allow"
#       Principal = {
#         Service = "redshift.amazonaws.com"
#       }
#       Action = "sts:AssumeRole"
#     }]
#   })
# }

# # resource "aws_iam_role_policy_attachment" "s3_read" {
# #   policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
# #   role       = aws_iam_role.s3_spectrum_role.name
# # }

# resource "aws_iam_role_policy_attachment" "glue_full" {
#   policy_arn = "arn:aws:iam::aws:policy/AWSGlueConsoleFullAccess"
#   role       = aws_iam_role.s3_spectrum_role.name
# }

# resource "aws_iam_policy" "s3_full_access_policy" {
#   name = "s3_full_access_policy"

#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action   = ["s3:*"]
#         Effect   = "Allow"
#         Resource = "*"
#       }
#     ]
#   })
# }


# resource "aws_iam_role_policy_attachment" "s3_full_access" {
#   policy_arn = aws_iam_policy.s3_full_access_policy.arn
#   role       = aws_iam_role.s3_spectrum_role.name
# }
