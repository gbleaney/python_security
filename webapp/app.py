# To start this server, run this from the root of the repo:
# FLASK_APP=webapp.app.py FLASK_ENV=development flask run -h localhost -p 2121

import inspect
import io
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Type, Tuple, List
import json

from code_execution.execution_base import (
    Exploit,
    get_exploit,
    get_exploits,
    get_exploits_by_category,
)
from flask import Flask, request, render_template, url_for, send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import FileStorage

app = Flask(__name__)

PAYLOAD_FOLDER = Path(".").resolve() / "payload_files"
PAYLOAD_FOLDER.mkdir(exist_ok=True)


@dataclass
class FormEntry:
    name: str
    input_type: str
    python_type: Type


@app.route("/")
def homepage():
    return render_template(
        "index.html", exploits_by_category=get_exploits_by_category()
    )


@app.route("/demo/<class_name>", methods=["GET"])
def demo(class_name: str):
    exploit = get_exploit(class_name)
    exploit_params = get_exploit_params(exploit)

    return render_template(
        "demo.html",
        demo_title=exploit.get_vulnerable_function_fqn(),
        class_name=class_name,
        exploit_params=exploit_params,
        vulnerable_code=inspect.getsource(exploit.run_payload),
        generation_code=inspect.getsource(exploit.generate_payload),
        exploits_by_category=get_exploits_by_category(),
    )


@app.route("/demo/<class_name>/run_payload/", methods=["POST"])
def run_payload(class_name: str):
    exploit = get_exploit(class_name)
    exploit_params = get_exploit_params(exploit)

    arguments = []
    for param in exploit_params:
        if param.python_type == str:
            arguments.append(request.form[param.name])
        elif param.python_type == FileStorage:
            arguments.append(request.files[param.name])
        else:
            raise Exception(f"Unexpected python type: {param.python_type}")
    if not arguments:
        return "Error!"
    exploit.run_payload(*arguments)
    return "It didn't crash..."


@app.route("/demo/<class_name>/generate_payload/", methods=["POST"])
def generate_payload(class_name: str):
    command = request.form["command"]

    exploit = get_exploit(class_name)
    exploit_params = get_exploit_params(exploit)

    payloads = exploit.generate_payload(command)
    payloads = payloads if isinstance(payloads, (list, tuple)) else [payloads]

    result = []

    for payload in payloads:
        if isinstance(payload, FileStorage):
            payload_folder = PAYLOAD_FOLDER / class_name
            payload_folder.mkdir(exist_ok=True)
            payload.save(payload_folder / payload.filename)
            result.append(
                url_for(
                    "payload_file", class_name=class_name, file_name=payload.filename
                )
            )
        elif isinstance(payload, str):
            result.append(payload)
        else:
            raise Exception(f"Unexpected type present in payload: {payload}")

    return json.dumps(result)


@app.route("/demo/<class_name>/payload_file/<file_name>", methods=["GET"])
def payload_file(class_name: str, file_name: str):
    return send_from_directory(
        PAYLOAD_FOLDER / class_name, file_name, as_attachment=True
    )


def get_exploit_params(exploit: Exploit) -> List[FormEntry]:
    exploit_params = []
    for param_name, param in inspect.signature(exploit.run_payload).parameters.items():
        if param.annotation == str:
            input_type = "text"
        elif param.annotation == FileStorage:
            input_type = "file"
        else:
            raise Exception("Unexpected parameter annotation")
        exploit_params.append(FormEntry(param_name, input_type, param.annotation))

    return exploit_params
