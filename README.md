# python-companycam

[![Test](https://github.com/ely-as/python-companycam/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/ely-as/python-companycam/actions/workflows/test.yml)
[![Coverage](https://cov.ely.as/github/ely-as/python-companycam/main/badge.svg)](https://cov.ely.as/github/ely-as/python-companycam/main/latest/)
[![Version](https://img.shields.io/pypi/v/companycam-unofficial)](https://pypi.org/project/companycam-unofficial/)
![Python](https://img.shields.io/pypi/pyversions/companycam-unofficial)

## Installation

```sh
python -m pip install companycam-unofficial
```

## Basic usage

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

For more detailed usage see [Usage](https://github.com/ely-as/python-companycam/blob/main/docs/usage.md).

## Contributing

See [Contributing](https://github.com/ely-as/python-companycam/blob/main/docs/contributing.md).

## Resources

- [CompanyCam Docs](https://docs.companycam.com/docs)

## Dependencies

- [HTTPX](https://www.python-httpx.org/) (BSD 3-clause license)
- [pydantic](https://pydantic-docs.helpmanual.io/) (MIT license)

## License

[MIT](https://github.com/ely-as/python-companycam/blob/main/LICENSE).
