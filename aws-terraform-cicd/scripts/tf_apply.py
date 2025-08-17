#!/usr/bin/env python3
from utils import run_cmd

def terraform_apply():
    # apply using generated plan
    run_cmd("terraform -chdir=terraform apply -input=false -auto-approve tfplan")

if __name__ == "__main__":
    terraform_apply()
