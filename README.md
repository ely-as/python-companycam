# python-companycam

![Test](https://github.com/ely-as/python-companycam/workflows/Test/badge.svg)
![Python](https://img.shields.io/pypi/pyversions/companycam-unofficial)
![License](https://img.shields.io/pypi/l/companycam-unofficial)

## Installation

```sh
python -m pip install companycam-unofficial
```

## Usage

```py
>>> import companycam
>>> from companycam.v2 import models

>>> api = companycam.API(token="YOUR_TOKEN_HERE")
>>> api.projects.list()
[Project(id='12345678', ...)]

>>> project = models.Project(name="My new project")
>>> api.projects.create(project)
Project(id='23456789', name='My new project', ...)
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

- [HTTPX](https://www.python-httpx.org/) (BSD 3-clause license)
- [pydantic](https://pydantic-docs.helpmanual.io/) (MIT license)

## License

[MIT](LICENSE).
