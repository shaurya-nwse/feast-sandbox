terraform {
}

locals {
  default_tags = {
    application      = "feast-aws"
    environment_type = "preview"
    contact_email    = "shaurya.rawat@new-work.se"
    provisioned_by   = "terraform"
  }
}

provider "aws" {
  region  = "eu-central-1"
  profile = "saml"

  default_tags {
    tags = local.default_tags
  }
}
