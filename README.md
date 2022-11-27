# python-companycam

![Test](https://github.com/ely-as/python-companycam/workflows/Test/badge.svg)

## Usage

### Installation

```sh
python -m pip install git+https://github.com/ely-as/python-companycam
```

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

## Resources

- [CompanyCam Docs](https://docs.companycam.com/docs)

## Dependencies

- [pydantic](https://pydantic-docs.helpmanual.io/) (MIT license)

## License

[MIT](LICENSE).
