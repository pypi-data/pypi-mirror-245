# openj

Kanban for Lean manufacturing (also called
just-in-time manufacturing, abbreviated JIT).

## Install

### PyPI

Install and update using pip:

```shell
pip install -U openj
```

### Repository

When using git, clone the repository and change your 
present working directory.

```shell
git clone http://github.com/mcpcpc/openj
cd openj/
```

Create and activate a virtual environment.

```shell
python3 -m venv venv
source venv/bin/activate
```

Install LibreHTF to the virtual environment.

```shell
pip install -e .
```

## Deployment

### Flask

Non-production WSGI via waitress for development and
debugging.

```shell
flask --app openj run --debug
```

### Waitress

Production WSGI via waitress.

```shell
pip install waitress
waitress-serve --call openj:create_app
```

## Test

```shell
python3 -m unittest
```

Run with coverage report.

```shell
coverage run -m unittest
coverage report
coverage html  # open htmlcov/index.html in a browser
```

## Resources

* https://en.m.wikipedia.org/wiki/Kanban