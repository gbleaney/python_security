# To start this server, run this from the root of the repo:
# FLASK_APP=webapp.app.py FLASK_ENV=development flask run -h localhost -p 2121

import inspect
from dataclasses import dataclass
from werkzeug.datastructures import FileStorage


from code_execution.execution_base import (
    Exploit,
    get_exploit,
    get_exploits,
    get_exploits_by_category,
)
from flask import Flask, request, render_template

app = Flask(__name__)


@dataclass
class FormEntry:
    name: str
    input_type: str


@app.route("/")
def homepage():
    return render_template(
        "index.html", exploits_by_category=get_exploits_by_category()
    )


@app.route("/demo/<class_name>", methods=["POST", "GET"])
def demo(class_name):
    exploit = get_exploit(class_name)
    exploit_params = []
    for param_name, param in inspect.signature(exploit.run_payload).parameters.items():
        if param.annotation == str:
            input_type = "text"
        elif param.annotation == FileStorage:
            input_type = "file"
        else:
            raise Exception("Unexpected parameter annotation")
        exploit_params.append(FormEntry(param_name, input_type))

    print(exploit_params)
    if request.method == "GET":
        return render_template(
            "demo.html",
            demo_title=exploit.get_vulnerable_function_fqn(),
            exploit_params=exploit_params,
            vulnerable_code=inspect.getsource(exploit.run_payload),
            generation_code=inspect.getsource(exploit.generate_payload),
            exploits_by_category=get_exploits_by_category(),
        )
        # (TODO) print page to take input
    elif request.method == "POST":
        arguments = []
        for param in exploit_params:
            if param.input_type == "text":
                arguments.append(request.form[param.name])
            elif param.input_type == "file":
                arguments.append(request.files[param.name])
            else:
                raise Exception("Unexpected input type")
        if not arguments:
            return "Error!"
        exploit.run_payload(*arguments)
        return "It didn't crash..."
