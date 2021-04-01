import os
import shlex
import subprocess
from .execution_base import Exploit


class ShellExploit(Exploit):
    category_name = "Shell Command Execution"
    def generate_payload(shell_command: str) -> str:
        return shell_command


class SubprocessCallExploit(ShellExploit):
    vulnerable_function = subprocess.call

    def run_payload(shell_command: str) -> None:
        split_payload = shlex.split(shell_command)
        subprocess.call(split_payload)
