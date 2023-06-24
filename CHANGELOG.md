## v0.2.0 (2023-06-24)
### Breaking Changes
- Dropped support for Python major versions 3.6 and 3.7. End of life for Python 3.6 was
  2021-12-23 and end of life for Python 3.7 will be 2023-06-27 (see the
  [Status of Python Versions](https://devguide.python.org/versions/)).

### Fixes
- Added `py.typed` file to indicate that package is type-enabled
  ([447cfc1](https://github.com/ely-as/python-companycam/commit/447cfc1)).
- Fixed typing errors
  ([a8abb75](https://github.com/ely-as/python-companycam/commit/a8abb75)).

### Docs
- Use non-localized links in docs
  ([33aa840](https://github.com/ely-as/python-companycam/commit/33aa840)).

### Internal
- Added CHANGELOG.md ([#10](https://github.com/ely-as/python-companycam/issues/10)) by
  @ely-as in [#11](https://github.com/ely-as/python-companycam/pull/11)
- Switched to pyproject.toml for all setuptools and test tool configuration and replaced
  flake8 and isort with ruff for linting and formatting imports by @ely-as in
  [#14](https://github.com/ely-as/python-companycam/pull/14)
- GitHub Actions now uploads coverage reports and added a coverage badge by @ely-as in
  [#15](https://github.com/ely-as/python-companycam/pull/15)
- Updated type annotations
  ([#12](https://github.com/ely-as/python-companycam/issues/12)) by @ely-as in
  [#16](https://github.com/ely-as/python-companycam/pull/16).
  - Applied [PEP 585](https://peps.python.org/pep-0585/) - changed types imported from
    `typing` to ABCs from `collections.abc` and generics.
  - Changed any remaining `typing.Union` type unions to `X | Y` (see
    [PEP 604](https://peps.python.org/pep-0604/))
  - Removed all `from future import __annotations__` imports.
- Enabled pydantic mypy plugin
  ([52e99a7](https://github.com/ely-as/python-companycam/commit/52e99a7)).
- Updated to the latest versions of actions/checkout and actions/setup-python in
  `python-publish.yml`
  ([709da60](https://github.com/ely-as/python-companycam/commit/709da60)).
- Set the minimum required version of tox to `>=4.0`and used the labels feature to tell
  GitHub Actions which testenvs to run
  ([4a8da2c](https://github.com/ely-as/python-companycam/commit/4a8da2c)).

## v0.1.6 (2023-01-31)
### Features
- Update v2 client to conform to CompanyCam/openapi-spec@40543ed.
### Docs
- Fix headings in contributing.md.
### Internal
- Add format [testenv] to apply formatting with one command.

## v0.1.5 (2022-12-17)
### Internal
- Refactor and test redefinition of Model.dict() arg defaults.
- Refactor how aliases for model fields are defined.

## v0.1.4 (2022-12-17)
### Fixes
- Make uri/url interchangeable for Photo and ImageURI models.
- Pass individual params (not an object) when creating photos.
- Pass array of strings (not objects) to Group POST/PUT paths.
- Exclude unset optional fields in HTTP requests.
### Internal
- Modify fixture so Project notepad has set data.
- Use python-jsonschema/jsonschema to validate JSON data in HTTP requests.
- Ensure linting and type tests are run by GitHub Actions.
- Separate mypy out from lint [testenv].

## v0.1.3 (2022-12-16)
### Fixes
- Convert Photo coordinates from list to dict when creating project photo.

## v0.1.2 (2022-12-15)
### Fixes
- Allow Photo model to receive coordinates attr as dict.
- Fix return types for paths which POST Tags.
- Fix how documents are uploaded to projects.
### Docs
- Update docs.
### Internal
- Add comments.

## v0.1.1 (2022-12-14)
### Features
- Initial release.

## v0.1.0 (2022-12-09)
### Features
- Pre-release.
