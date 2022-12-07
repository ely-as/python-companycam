"""
These exceptions are HTTP status errors which have been mapped to CompanyCam error
types, so they can handled semantically e.g.

```py
try:
    api.projects.list()
except companycam.PaymentRequired as exc:
    ...
except companycam.Forbidden as exc:
    ...
```

The class names, status codes and docstrings used for subclasses of
`BaseCompanyCamException` are based on: https://docs.companycam.com/reference/codes.
"""
from typing import Dict, Type

import httpx


class BaseCompanyCamException(httpx.HTTPStatusError):
    """Subclasses should have unique status codes, and should not themselves be
    subclassed.
    """

    status_code: int


def map_status_codes_to_exceptions() -> Dict[int, Type[BaseCompanyCamException]]:
    # Using `__subclasses__()` relies on all subclasses being defined in this file
    return {exc.status_code: exc for exc in BaseCompanyCamException.__subclasses__()}


class BadRequest(BaseCompanyCamException):
    """The request is invalid"""

    status_code = 400


class Unauthorized(BaseCompanyCamException):
    """The user needs to authenticate or authentication failed"""

    status_code = 401


class PaymentRequired(BaseCompanyCamException):
    """The user's subscription has expired"""

    status_code = 402


class Forbidden(BaseCompanyCamException):
    """The user doesn’t have privilege to access the resource"""

    status_code = 403


class NotFound(BaseCompanyCamException):
    """The specified resource could not be found"""

    status_code = 404


class Conflict(BaseCompanyCamException):
    """The entity is not unique"""

    status_code = 409


class UnprocessableEntity(BaseCompanyCamException):
    """There was an issue persisting your request due to invalid data"""

    status_code = 422


class InternalServerError(BaseCompanyCamException):
    """We had a problem with our server"""

    status_code = 500
