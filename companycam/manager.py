import functools
import inspect
import logging
from collections.abc import Callable
from string import Formatter
from typing import Any, Literal

import httpx
from pydantic import BaseModel, ValidationError

from companycam.client import LazyClient
from companycam.utils import parse_obj_as

formatter = Formatter()
logger = logging.getLogger(__name__)


class BaseManager(object):
    client: LazyClient

    def __init__(self, client: LazyClient) -> None:
        self.client = client


def field_names_in_format_string(format_string: str) -> list[str]:
    """For a given format string return the field_name's

    More on format strings: https://docs.python.org/3/library/string.html#formatstrings
    """
    return [x[1] for x in formatter.parse(format_string) if x[1]]


def get_string_from_object(obj: BaseModel | str) -> str:
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, BaseModel) and hasattr(obj, "id"):
        return obj.id
    elif isinstance(obj, BaseModel):
        raise ValueError(f"Failed to extract 'id' from {obj}: Model has no 'id' field")
    else:
        raise TypeError()


def format_url(url: str, kwargs: dict) -> str:
    expected_fields = field_names_in_format_string(url)
    url_kwargs = {}
    for field in expected_fields:
        url_kwargs[field] = get_string_from_object(kwargs[field])
    return url.format(**url_kwargs)


def request(**request_dict):
    """All keyword arguments get passed to `httpx.Client.build_request()`.

    Note that setting a return type on this function causes type checking issues,
    since the methods which use it have their return data converted by the `BaseRequest`
    decorator.
    """
    return request_dict


class BaseRequest(object):
    method: Literal["get", "post", "put", "delete"]
    return_type: type
    url: str

    def __init__(self, url: str) -> None:
        super().__init__()
        self.url = url

    def __call__(self, decorated_method: Callable[..., Any]) -> Callable[..., Any]:
        # store decorator object for introspection of decorated_method (e.g. unit tests)
        decorated_method._decorated_by = self  # type: ignore[attr-defined]
        # store return_type
        self.return_type = decorated_method.__annotations__.get("return")  # type: ignore[assignment]

        @functools.wraps(decorated_method)
        def wrapper(obj, *args, **kwargs):
            # Call method
            request_dict = decorated_method(obj, *args, **kwargs)
            if "url" not in request_dict:
                # Convert any args to kwargs for format_url
                url_kwargs = inspect.getcallargs(decorated_method, obj, *args, **kwargs)
                request_dict["url"] = format_url(self.url, url_kwargs)
            # Send request
            with obj.client.make_client() as client:
                request = client.build_request(self.method, **request_dict)
                response = client.send(request)
            # Convert response to return data
            return self.response_to_return_data(response)

        return wrapper

    def response_to_return_data(self, response: httpx.Response) -> Any:
        if response.status_code in [200, 201]:
            try:
                return parse_obj_as(self.return_type, response.json())
            except ValidationError:
                return response.json()
        elif response.status_code == 204:
            return True


class get(BaseRequest):
    method = "get"


class post(BaseRequest):
    method = "post"


class put(BaseRequest):
    method = "put"


class delete(BaseRequest):
    method = "delete"
