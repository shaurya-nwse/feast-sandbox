# data "aws_iam_role" "AWSServiceRoleForRedshift" {
#   name = "AWSServiceRoleForRedshift"
# }


# resource "aws_redshift_cluster" "feast_aws_test_cluster" {
#   cluster_identifier = "${var.application}-test-cluster"
#   iam_roles = [
#     data.aws_iam_role.AWSServiceRoleForRedshift.arn,
#     aws_iam_role.s3_spectrum_role.arn
#   ]

#   database_name     = var.database_name
#   master_username   = var.redshift_admin_user
#   master_password   = var.redshift_admin_password
#   node_type         = var.node_type
#   cluster_type      = var.cluster_type
#   number_of_nodes   = var.number_of_nodes
#   encrypted         = true
#   apply_immediately = true
#   availability_zone = "eu-central-1a"

#   skip_final_snapshot = true

#   # TODO: Enable logging
# }
