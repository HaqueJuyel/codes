#!/usr/bin/env python3
import subprocess
import shlex
import sys

def run_cmd(cmd, cwd=None, env=None, capture_output=False):
    """Run a shell command and stream output; raise on non-zero exit."""
    print(f">>> running: {cmd}")
    proc = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd=cwd,
        env=env,
        text=True,
        bufsize=1
    )
    # stream stdout
    for line in proc.stdout:
        print(line, end="")
    proc.stdout.close()
    return_code = proc.wait()
    if return_code != 0:
        raise SystemExit(f"Command failed with exit code {return_code}: {cmd}")
    return return_code

if __name__ == "__main__":
    print("utils module - not intended to be run directly")
