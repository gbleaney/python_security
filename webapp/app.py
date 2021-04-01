import inspect

from flask import Flask, request, render_template

from .code_execution import Exploit, get_exploit, get_exploits, get_exploits_by_category

app = Flask(__name__)


# run with
# env FLAS_APP=app.py FLASK_ENV=development flask run -h localhost -p 2121


@app.route("/")
def homepage():
    return render_template("index.html", exploits_by_category=get_exploits_by_category())


@app.route("/demo/<class_name>", methods=["POST", "GET"])
def demo(class_name):
    exploit = get_exploit(class_name)
    exploit_params = inspect.signature(exploit.run_payload).parameters
    if request.method == "GET":
        return render_template(
            "demo.html",
            demo_title=exploit.get_vulnerable_function_fqn(),
            exploit_params=exploit_params,
            vulnerable_code=inspect.getsource(exploit.run_payload),
            generation_code=inspect.getsource(exploit.generate_payload),
            exploits_by_category=get_exploits_by_category()
        )
        # (TODO) print page to take input
    elif request.method == "POST":
        arguments = [request.form.get(param, None) for param in exploit_params]
        if not arguments:
            return "Error!"
        exploit.run_payload(*arguments)
        return "It didn't crash..."
