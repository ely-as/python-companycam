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

This project uses the formatters [black](https://github.com/psf/black) and
[isort](https://pycqa.github.io/isort/).

By default the `tox` command will only check formatting i.e. the `lint` environment,
which is included in the default environment list, will only execute black and isort
with the `--check` and `--diff` flags.

To apply formatting:
```sh
tox -e format
```

### Update Git submodules

```sh
git submodule foreach git pull
```
