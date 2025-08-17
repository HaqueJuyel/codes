#!/usr/bin/env python3
from utils import run_cmd

def terraform_destroy():
    run_cmd("terraform -chdir=terraform destroy -auto-approve")

if __name__ == "__main__":
    terraform_destroy()
