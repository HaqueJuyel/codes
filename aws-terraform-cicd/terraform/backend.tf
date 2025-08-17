terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"   # <<-- change me
    key            = "terraform/aws-cicd-ec2/terraform.tfstate"
    region         = "us-east-1"                   # <<-- change me
    dynamodb_table = "terraform-state-lock"        # <<-- change me
    encrypt        = true
  }
}
