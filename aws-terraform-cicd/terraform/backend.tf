terraform {
  backend "s3" {
    bucket         = "terrform-backend-b"   # <<-- change me
    key            = "terraform/terraform.tfstate"
    region         = "us-east-1"                   # <<-- change me
    dynamodb_table = "terraform-state-lock"        # <<-- change me
    encrypt        = true
  }
}
