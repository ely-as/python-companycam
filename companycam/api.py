from __future__ import annotations

import typing

import httpx

from companycam import v2
from companycam.client import LazyClient
from companycam.exceptions import map_status_codes_to_exceptions

STATUS_CODES_TO_EXCEPTIONS = map_status_codes_to_exceptions()
SUPPORTED_VERSIONS: typing.List[str] = ["v2"]


def raise_on_4xx_5xx(response: httpx.Response) -> None:
    """Raise a custom CompanyCam exception if the response has a status code which
    matches a code used by CompanyCam.

    See https://docs.companycam.com/reference/codes for a list of status codes used by
    CompanyCam.
    """
    if companycam_exc := STATUS_CODES_TO_EXCEPTIONS.get(response.status_code):
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            # suppress exception context since we're raising exceptions which inherit from httpx.HTTPStatusError anyway
            raise companycam_exc(
                *e.args, request=e.request, response=e.response
            ) from None


class BasicTokenAuth(httpx.Auth):
    def __init__(self, token: str) -> None:
        self.token = token

    def auth_flow(
        self, request: httpx.Request
    ) -> typing.Generator[httpx.Request, httpx.Response, None]:
        request.headers["authorization"] = f"Bearer {self.token}"
        yield request


class API(object):
    """
    Usage:
    ```py
    >>> api = companycam.API(token="YOUR_ACCESS_TOKEN")
    >>> api.company.retrieve()
    ```

    **Parameters:**

    * **token** - An access token.
    * **version** - *(optional)* API version e.g. "v2".
    * **server_url** - *(optional)* Specify a server URL if you wish to use something
    other than the default e.g. for testing.
    """

    def __init__(
        self,
        token: str,
        version: typing.Literal["v2"] = "v2",
        server_url: str | None = None,
    ) -> None:
        if version not in SUPPORTED_VERSIONS:
            raise ValueError(
                "This package only supports the following API versions: '"
                + "', '".join(SUPPORTED_VERSIONS)
                + "'"
            )
        if version == "v2":
            default_server_url = v2.defaults.SERVER_URL
        self.client = LazyClient(
            auth=BasicTokenAuth(token),
            headers={"accept": "application/json"},
            event_hooks={"response": [raise_on_4xx_5xx]},
            base_url=(server_url or default_server_url),
        )
        if version == "v2":
            self.company = v2.managers.CompanyManager(self.client)
            self.users = v2.managers.UsersManager(self.client)
            self.projects = v2.managers.ProjectsManager(self.client)
            self.photos = v2.managers.PhotosManager(self.client)
            self.tags = v2.managers.TagsManager(self.client)
            self.groups = v2.managers.GroupsManager(self.client)
            self.webhooks = v2.managers.WebhooksManager(self.client)
