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

Install the package in editable mode with the optional `test` dependencies:
```sh
python -m pip install -e ".[test]"
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

### Apply formatting

This project uses [black](https://github.com/psf/black) and
[isort](https://pycqa.github.io/isort/) formatting.

By default the `tox` command will only check formatting. To apply formatting:
```sh
tox -e format
```

### Update Git submodules

```sh
git submodule foreach git pull
```
