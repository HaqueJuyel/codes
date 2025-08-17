#!/usr/bin/env python3
from utils import run_cmd

def terraform_plan():
    # create plan file tfplan in terraform dir
    run_cmd("terraform -chdir=terraform plan -input=false -out=tfplan")

if __name__ == "__main__":
    terraform_plan()
