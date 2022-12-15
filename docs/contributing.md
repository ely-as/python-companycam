# Contributing

## Development

### Installation

```sh
git clone --recurse-submodules git+https://github.com/ely-as/python-companycam
cd python-companycam
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

Run a specific tox environment:
```sh
tox -e flake8
```

### Update Git submodules

```sh
git submodule foreach git pull
```