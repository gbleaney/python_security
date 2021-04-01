# Run with `python -m unittest` from root of this repo

import logging
import pathlib
import tempfile
import unittest
from typing import Type

from ..execution_base import get_exploits, Exploit
from ..filesystem_python_code_execution import FilesystemPythonExploit
from ..python_code_execution import SimplePythonExploit
from ..shell_command_execution import ShellExploit

logging.basicConfig(level=logging.DEBUG)


class CodeExecutionMethods(unittest.TestCase):
    def run_exploits(self, exploit_type: Type[Exploit], command: str):
        exploits = get_exploits(exploit_type)
        for exploit in exploits:
            logging.debug(
                f"Using {exploit} to test {exploit.get_vulnerable_function_fqn()}"
            )
            with tempfile.TemporaryDirectory() as tmpdirname:
                file_to_touch = pathlib.Path(tmpdirname) / "file"
                payload = exploit.generate_payload(
                    command.format(file=file_to_touch.absolute())
                )
                logging.debug(payload)
                if isinstance(payload, (str, bytes)):
                    exploit.run_payload(payload)
                elif isinstance(payload, list):
                    exploit.run_payload(*payload)
                else:
                    raise Exception("Unexpected payload")
                # import time
                # time.sleep(1)
                logging.debug(f"Test status: {file_to_touch.exists()}")
                # if not file_to_touch.exists():
                #     time.sleep(60)
                self.assertTrue(
                    file_to_touch.exists(),
                    f"Expected {exploit} to touch {file_to_touch} when passed {payload}",
                )
            logging.debug(
                f"Finished with {exploit} testing {exploit.get_vulnerable_function_fqn()}"
            )

    def test_shell_command_execution(self):
        self.run_exploits(ShellExploit, "touch {file}")

    def test_simple_python_code_execution(self):
        self.run_exploits(
            SimplePythonExploit,
            """exec("import subprocess; subprocess.run(['touch', '{file}'])")""",
        )

    def test_filesystem_python_code_execution(self):
        self.run_exploits(
            FilesystemPythonExploit,
            """exec("import subprocess; subprocess.run(['touch', '{file}'])")""",
        )


if __name__ == "__main__":
    unittest.main()
