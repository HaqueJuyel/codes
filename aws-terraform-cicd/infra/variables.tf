variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
}

variable "ami_id" {
  description = "AMI to use"
  type        = string
}

variable "key_name" {
  description = "SSH key name"
  type        = string
}
