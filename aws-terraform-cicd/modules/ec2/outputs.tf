output "instance_id" {
  description = "EC2 instance id"
  value       = aws_instance.this.id
}

output "public_ip" {
  description = "EC2 public IP"
  value       = aws_instance.this.public_ip
}

output "private_ip" {
  description = "EC2 private IP"
  value       = aws_instance.this.private_ip
}
