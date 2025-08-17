variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "ami" {
  description = "AMI ID to use for EC2 (update per region)"
  type        = string
  default     = "ami-0c02fb55956c7d316" # Amazon Linux 2 (example) - CHANGE per region
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "instance_name" {
  description = "Name tag for EC2 instance"
  type        = string
  default     = "terraform-ec2"
}

variable "subnet_id" {
  description = "Subnet id (optional). If null, EC2 will use default subnet"
  type        = string
  default     = null
}

variable "security_group_ids" {
  description = "List of security group ids"
  type        = list(string)
  default     = []
}

variable "key_name" {
  description = "SSH key name (optional)"
  type        = string
  default     = null
}
