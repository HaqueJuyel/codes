#!/usr/bin/env python3
from utils import run_cmd

def terraform_init():
    # init with backend config file already in terraform/backend.tf
    run_cmd("terraform -chdir=terraform init -input=false -upgrade")

if __name__ == "__main__":
    terraform_init()
