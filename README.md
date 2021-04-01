# python_security
This repository collects lists of security-relavent Python APIs, along with examples of exploits using those APIs

To work with the code in this repo, you must be in a virtual environment:
```
$ cd /path/to/python_security
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

From there, you can run the tests:
```
(venv) $ python3 -m unittest
```

Or you can launch the server to interactively play with the examples:
```
(venv) $ FASK_APP=webapp.app.py FLASK_ENV=development flask run -h localhost -p 2121
```
