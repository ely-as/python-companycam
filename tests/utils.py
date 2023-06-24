from __future__ import annotations

import json
import re
import types
import typing
from collections.abc import Callable, Iterable
from functools import cached_property
from inspect import getmembers, isclass, isfunction, signature

import httpx
import pytest
import yaml
from pytest_mock import MockerFixture

import companycam

from . import paths

if typing.TYPE_CHECKING:
    from companycam.manager import BaseManager


# Functions which automatically discover objects which need to be tested to ensure
# reliable coverage


def get_managers_from_module(managers: types.ModuleType) -> dict:
    return dict(
        getmembers(managers, lambda m: isclass(m) and m.__module__ == managers.__name__)
    )


def get_models_from_module(models: types.ModuleType) -> dict:
    return dict(
        getmembers(models, lambda m: isclass(m) and m.__module__ == models.__name__)
    )


def get_paths_from_manager_cls(manager: BaseManager) -> dict:
    return dict(
        getmembers(manager, lambda m: isfunction(m) and hasattr(m, "_decorated_by"))
    )


# Utils for connecting the dots between our client, the OpenAPI spec, HTTPX objects etc.


def clean_url(url: str) -> str:
    """Remove any query strings or anchors from the URL."""
    return url.split("?")[0].split("#")[0]


def get_2xx_status_code(status_codes: Iterable[int | str]) -> str:
    """Get the 2xx status code from an iterable of status codes (expects one, only)."""
    codes_2xx = [str(c) for c in status_codes if str(c).startswith("2")]
    if len(codes_2xx) > 1:
        raise ValueError(
            "Found multiple success (2xx) status codes: " + ", ".join(codes_2xx)
        )
    elif len(codes_2xx) == 0:
        raise ValueError("Could not find success (2xx) status code")
    return codes_2xx[0]


def get_matching_url(format_strings: typing.Iterable[str], target_url: str) -> str:
    """Given an iterable of format strings e.g. `/users/{id}` find a match against a
    real URL e.g. `/users/1234`. Prefer exact matches e.g. `target_url="/users/current"
    would match `/users/current` rather than `/users/{}` if both format strings are
    present.
    """
    target_url = clean_url(target_url)
    matching_urls = [u for u in format_strings if match_url(u, target_url)]
    if len(matching_urls) == 1:
        return matching_urls[0]
    elif len(matching_urls) > 1:
        # Return an exact match if it exists
        for url in matching_urls:
            if target_url.endswith(url):
                return url
        raise ValueError(
            f"Matched more than one URL for '{target_url}': " + ", ".join(matching_urls)
        )
    raise ValueError(f"Could not find matching URL for '{target_url}'")


def get_name_from_ref(uri: str) -> str:
    """Get component name from an OpenAPI Reference Object $ref field e.g.
    passing `#/components/schemas/Company` would return `Company`.
    """
    return uri.split("/")[-1]


def load_openapi_spec() -> dict:
    with open(paths.OPENAPI_YAML, "r") as f:
        return yaml.safe_load(f)


def match_url(format_string: str, url: str) -> bool:
    """Match a format string e.g. `/users/{id}` against a real URL e.g. `/users/1234`."""
    format_string_re = (
        r"^(?:https?://)?"
        + r"(?:[^/]*)"
        + normalize_url(format_string).replace("{}", r"(?:[\w%]+)")
        + r"(?:/?)$"
    )
    return bool(re.search(format_string_re, url))


def normalize_url(url: str) -> str:
    """Remove the field names from placeholders in a format string e.g. `/users/{id}`
    would become `/users/{}`.
    """
    return re.sub(r"{\w*}", "{}", url)


# Classes to load an OpenAPI specification into and provide helpers


class OpenAPIPath(object):
    def __init__(self, method: str, url: str, path_dict: dict) -> None:
        self.method = method
        self.url = url
        self.dict = path_dict

    @cached_property
    def normalized_url(self) -> str:
        return normalize_url(self.url)

    @cached_property
    def parameters(self) -> list[dict]:
        return self.dict.get("parameters", [])

    @cached_property
    def query_parameters(self) -> list[dict]:
        return [p for p in self.parameters if p.get("in") == "query"]

    @cached_property
    def request_json_schema(self) -> dict:
        try:
            return self.dict["requestBody"]["content"]["application/json"]["schema"]
        except KeyError:
            return {}

    @cached_property
    def responses(self) -> dict[str, dict]:
        return self.dict["responses"]

    @cached_property
    def response_2xx(self) -> dict:
        return self.responses[self.status_code_2xx]

    @cached_property
    def response_json_schema(self) -> dict:
        try:
            return self.response_2xx["content"]["application/json"]["schema"]
        except KeyError:
            return {}

    @cached_property
    def response_json_component(self) -> str | None:
        """Find $ref in schema and convert to component name. Can implement a recursive
        key search if we need to handle responses more complicated than objects and
        lists of objects.
        """
        # Lists of objects
        try:
            return get_name_from_ref(self.response_json_schema["items"]["$ref"])
        except (KeyError, TypeError):
            pass
        # Objects
        try:
            return get_name_from_ref(self.response_json_schema["$ref"])
        except (KeyError, TypeError):
            return None

    @cached_property
    def response_json_is_list(self) -> bool:
        try:
            return self.response_json_schema["type"] == "array"
        except (KeyError, TypeError):
            return False

    @cached_property
    def status_code_2xx(self) -> str:
        return get_2xx_status_code(self.responses)


class OpenAPI(object):
    def __init__(self) -> None:
        try:
            self.spec = load_openapi_spec()
        except FileNotFoundError:
            pytest.skip(
                "Failed to load OpenAPI spec (has own unit test) - skipping module",
                allow_module_level=True,
            )

    @property
    def component_schemas(self) -> dict:
        return self.spec["components"]["schemas"]

    @cached_property
    def paths(self) -> list[OpenAPIPath]:
        return [
            OpenAPIPath(method, url, path_dict)
            for url, methods in self.spec["paths"].items()
            for method, path_dict in methods.items()
        ]

    def find_path(self, method: str, url: str) -> OpenAPIPath:
        method = method.lower()
        url_found = False
        for openapi_url, openapi_methods in self.spec["paths"].items():
            if normalize_url(openapi_url) == normalize_url(url):
                url_found = True
                if method in openapi_methods:
                    return OpenAPIPath(method, url, openapi_methods[method])
        if url_found:
            raise ValueError(
                f"URL '{url}' found in OpenAPI specification, but no matching method '{method}'"
            )
        else:
            raise ValueError(f"URL '{url}' not found in OpenAPI specification.")


# Classes for aggregating and testing our models and manager paths


class ClientSendPatcher(object):
    def __init__(self, mocker: MockerFixture) -> None:
        self.mock = mocker.patch("httpx.Client.send")
        self.mock.side_effect = self.get_response
        with open(paths.FIXTURE_V2_RESPONSES, "r") as f:
            self.fixture = json.load(f)

    @property
    def request(self) -> httpx.Request:
        return self.mock.call_args[0][0]

    def get_response(self, request: httpx.Request) -> httpx.Response:
        try:
            url = str(request.url)
            method = request.method.lower()
            fixture_url = get_matching_url(self.fixture, url)  # can raise ValueError
            response = self.fixture[fixture_url][method]  # can raise KeyError
        except (KeyError, ValueError) as exc:
            raise type(exc)(
                f"{exc} (Is an API path missing a fixture? i.e. '{request.method} "
                f"{url}')"
            ) from None
        return httpx.Response(**response)


class ManagerPath(object):
    def __init__(
        self, func: Callable[..., typing.Any], manager: type[BaseManager]
    ) -> None:
        self.func = func
        self.func_name = func.__name__
        self.func_parameters = dict(signature(func).parameters)
        self.manager = manager
        self.method = func._decorated_by.method  # type: ignore[attr-defined]
        self.return_type = func._decorated_by.return_type  # type: ignore[attr-defined]
        self.url = func._decorated_by.url  # type: ignore[attr-defined]

    def call(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        api = companycam.API(token="TEST_TOKEN", server_url="http://testserver")
        manager_obj = self.manager(api.client)
        result = getattr(manager_obj, self.func_name)(*args, **kwargs)
        return result

    def filter_kwargs(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        """Filter out any kwargs which are not valid func parameters"""
        return {k: v for k, v in kwargs.items() if k in self.func_parameters}


class ClientTestHelper(object):
    def __init__(self, managers: types.ModuleType, models: types.ModuleType) -> None:
        self.managers = get_managers_from_module(managers)
        self.models = get_managers_from_module(models)

    @cached_property
    def manager_paths(self) -> list[ManagerPath]:
        return [
            ManagerPath(func, manager)
            for manager in self.managers.values()
            for func_name, func in get_paths_from_manager_cls(manager).items()
        ]
