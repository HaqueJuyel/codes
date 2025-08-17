variable "ami" {
  description = "AMI id for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "instance_name" {
  description = "Tag Name for instance"
  type        = string
  default     = "terraform-ec2"
}

variable "subnet_id" {
  description = "Subnet ID to launch the instance into"
  type        = string
  default     = null
}

variable "security_group_ids" {
  description = "List of security group ids"
  type        = list(string)
  default     = []
}

variable "key_name" {
  description = "SSH key name to attach (optional)"
  type        = string
  default     = null
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}
