# Run with `python -m unittest` from root of this repo

import asyncio
import inspect
import logging
import pathlib
import tempfile
import unittest
from typing import Type, List
from werkzeug.datastructures import FileStorage

from ..execution_base import get_exploits, Exploit
from ..python_code_execution import PythonExploit
from ..shell_command_execution import ShellExploit

logging.basicConfig(level=logging.DEBUG)


class CodeExecutionMethods(unittest.TestCase):
    def run_exploits(
        self,
        exploit_type: Type[Exploit],
        command: str,
    ):
        exploits = sorted(get_exploits(exploit_type),key=lambda exploit: exploit.__name__)
        for exploit in exploits:
            logging.debug(
                f"Using {exploit} to test {exploit.get_vulnerable_function_fqn()}"
            )
            with tempfile.TemporaryDirectory() as tmpdirname:
                file_to_touch = pathlib.Path(tmpdirname) / "file"
                payload = exploit.generate_payload(
                    command.format(file=file_to_touch.absolute())
                )
                logging.debug(f"Using payload: {payload}")
                if isinstance(payload, (str, bytes, FileStorage)):
                    payload = [payload]
                elif isinstance(payload, (list, tuple)):
                    pass
                else:
                    raise Exception("Unexpected payload")

                logging.debug("Running sync test")
                exploit.run_payload(*payload)

                logging.debug(f"Test status: {file_to_touch.exists()}")

                self.assertTrue(
                    file_to_touch.exists(),
                    f"Expected {exploit} to touch {file_to_touch} when passed {payload}",
                )
            logging.debug(
                f"Finished with {exploit} testing {exploit.get_vulnerable_function_fqn()}"
            )

    def test_shell_command_execution(self):
        self.run_exploits(ShellExploit, "touch {file}")

    def test_python_code_execution(self):
        self.run_exploits(
            PythonExploit,
            """exec("import subprocess; subprocess.call(['touch', '{file}'])")""",
        )


if __name__ == "__main__":
    unittest.main()
