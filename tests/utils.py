from __future__ import annotations

import re
import types
import typing
from functools import cached_property
from inspect import getmembers, isclass, isfunction
from pathlib import Path

import pytest
import yaml

if typing.TYPE_CHECKING:
    from companycam.managers import BaseManager

PATH_TO_OPENAPI_YAML: Path = Path(__file__).parent.parent / "openapi-spec/openapi.yaml"


def get_name_from_ref(uri: str) -> str:
    """Get component name from an OpenAPI Reference Object $ref field e.g.
    passing `#/components/schemas/Company` would return `Company`.
    """
    return uri.split("/")[-1]


def load_openapi_spec() -> typing.Dict:
    data = {}
    with open(PATH_TO_OPENAPI_YAML, "r") as f:
        data = yaml.safe_load(f)
    return data


def normalize_url(url: str) -> str:
    """Remove the field names from placeholders in a format string e.g. `/users/{id}`
    would become `/users/{}`.
    """
    return re.sub(r"{\w*}", "{}", url)


class OpenAPIPath(object):
    def __init__(self, method: str, url: str, path_dict: typing.Dict) -> None:
        self.method = method
        self.url = url
        self.dict = path_dict

    @cached_property
    def normalized_url(self) -> str:
        return normalize_url(self.url)

    @cached_property
    def parameters(self) -> typing.List[typing.Dict]:
        return self.dict.get("parameters", [])

    @cached_property
    def query_parameters(self) -> typing.List[typing.Dict]:
        return [p for p in self.parameters if p.get("in") == "query"]

    @cached_property
    def responses(self) -> typing.Dict[str, typing.Dict]:
        return self.dict["responses"]

    @cached_property
    def response_2xx(self) -> typing.Dict:
        return self.responses[self.status_code_2xx]

    @cached_property
    def response_json_schema(self) -> typing.Dict:
        try:
            return self.response_2xx["content"]["application/json"]["schema"]
        except KeyError:
            return {}

    @cached_property
    def response_json_component(self) -> typing.Optional[str]:
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
        responses_2xx = [r for r in self.responses if str(r).startswith("2")]
        if len(responses_2xx) > 1:
            raise ValueError(
                f"({self.method} {self.url}) Found multiple valid (2xx) status codes: "
                + ", ".join(responses_2xx)
            )
        elif len(responses_2xx) == 0:
            raise ValueError(
                f"({self.method} {self.url}) Could not find valid (2xx) status code"
            )
        return responses_2xx[0]


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
    def component_schemas(self) -> typing.Dict:
        return self.spec["components"]["schemas"]

    @cached_property
    def paths(self) -> typing.List[OpenAPIPath]:
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


class ClientTestHelper(object):
    def __init__(self, managers: types.ModuleType, models: types.ModuleType) -> None:
        self.managers = self.get_managers_from_module(managers)
        self.models = self.get_managers_from_module(models)

    @staticmethod
    def get_managers_from_module(managers: types.ModuleType) -> typing.Dict:
        return dict(
            getmembers(
                managers, lambda m: isclass(m) and m.__module__ == managers.__name__
            )
        )

    @staticmethod
    def get_models_from_module(models: types.ModuleType) -> typing.Dict:
        return dict(
            getmembers(models, lambda m: isclass(m) and m.__module__ == models.__name__)
        )

    @staticmethod
    def get_paths_from_manager_cls(manager: BaseManager) -> typing.Dict:
        return dict(
            getmembers(manager, lambda m: isfunction(m) and hasattr(m, "_decorated_by"))
        )

    @cached_property
    def manager_paths(self) -> typing.List[typing.Dict]:
        return [
            {
                "func": func,
                "func_name": func_name,
                "manager": manager,
                "method": func._decorated_by.method,
                "return_type": func._decorated_by.return_type,
                "url": func._decorated_by.url,
            }
            for manager in self.managers.values()
            for func_name, func in self.get_paths_from_manager_cls(manager).items()
        ]
