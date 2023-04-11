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
