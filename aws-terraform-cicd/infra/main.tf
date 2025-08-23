module "ec2" {
  source            = "../modules/ec2"
  ami               = var.ami
  instance_type     = var.instance_type
  instance_name     = var.instance_name
  subnet_id         = var.subnet_id
  security_group_ids = var.security_group_ids
  key_name          = var.key_name
}
