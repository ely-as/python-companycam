# Contributing

## Development

### Installation

Clone the repository:
```sh
git clone --recurse-submodules git+https://github.com/ely-as/python-companycam
cd python-companycam
```

Create a virtual environment (recommended):
```sh
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

Install the package:
```sh
python -m pip install -e .
```

### Run tests

Install [tox](https://tox.wiki/en/latest/):
```sh
python -m pip install tox
```

Run tox:
```sh
tox
```

Run specific tox environments (if needed):
```sh
tox -e flake8
tox -e py38-pytest
```

### Apply formatting

The `tox` command will only check formatting.

To apply formatting, install `black` and `isort`:
```sh
python -m pip install black isort
black .
isort .
```
