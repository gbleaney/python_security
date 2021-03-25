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
    if request.method == "GET":
        return render_template(
            "demo.html",
            demo_title=exploit.get_vulnerable_function_fqn(),
            vulnerable_code=inspect.getsource(exploit.run_payload),
            generation_code=inspect.getsource(exploit.generate_payload), exploits_by_category=get_exploits_by_category()
        )
        # (TODO) print page to take input
    elif request.method == "POST":
        payload = request.form.get("payload", None)
        if not payload:
            return "Error!"
        exploit.run_payload(payload)
        return "It didn't crash..."
