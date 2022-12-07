import re
import typing
from inspect import getmembers, isclass, isfunction

import pytest
from pytest_mock import MockerFixture

import companycam
from companycam.v2 import managers

from .openapi import get_name_from_ref, load_openapi_spec

ALL_MANAGERS = dict(
    getmembers(managers, lambda m: isclass(m) and m.__module__ == managers.__name__)
)
OPENAPI_SPEC = load_openapi_spec()


def normalize_url(url: str) -> str:
    """Remove the field names from placeholders in a format string e.g. `/users/{id}`
    would become `/users/{}`.
    """
    return re.sub(r"{\w*}", "{}", url)


def yield_paths_from_managers(
    *managers: typing.Type[managers.BaseManager],
) -> typing.Iterator[typing.Dict]:
    for manager in managers:
        for func_name, func in getmembers(
            manager, lambda m: isfunction(m) and hasattr(m, "_decorated_by")
        ):
            yield {
                "func": func,
                "func_name": func_name,
                "manager": manager,
                "method": func._decorated_by.method,
                "return_type": func._decorated_by.return_type,
                "url": func._decorated_by.url,
            }


OPENAPI_SPEC_PATHS = {normalize_url(k): v for k, v in OPENAPI_SPEC["paths"].items()}


@pytest.mark.parametrize("path_info", yield_paths_from_managers(*ALL_MANAGERS.values()))
def test_all_manager_paths_exist_in_OpenAPI_spec(path_info: typing.Dict) -> None:
    # path being a combination of URL and HTTP method, so assert both
    url = normalize_url(path_info["url"])
    assert url in OPENAPI_SPEC_PATHS
    assert path_info["method"] in OPENAPI_SPEC_PATHS[url]


@pytest.mark.parametrize("path_info", yield_paths_from_managers(*ALL_MANAGERS.values()))
def test_all_manager_paths_return_same_type_as_in_OpenAPI_spec(  # noqa: C901 (will refactor)
    path_info: typing.Dict,
) -> None:
    try:
        url = normalize_url(path_info["url"])
        method = path_info["method"]
        path_spec = OPENAPI_SPEC_PATHS[url][method]
    except AttributeError:
        pytest.skip(
            "Path appears to be missing, but this is covered by a different unit test."
        )
    try:
        resp_2xx = [k for k in path_spec["responses"] if k.startswith("2")][0]
    except IndexError:
        return
    if resp_2xx == "204":
        assert path_info["return_type"] == bool
    if "application_json" in path_spec["responses"][resp_2xx].get("content", {}):
        schema = path_spec["content"]["schema"]
        if "items" in schema and schema["type"] == "array":
            ref = schema["items"]["$ref"]
            assert "List" in str(path_info["return_type"])
        elif "$ref" in schema:
            ref = schema["$ref"]
        else:
            pytest.fail(
                f"Cannot find $ref in {resp_2xx} response for {method.upper()} {url} in OpenAPI spec."
            )
        model_name = get_name_from_ref(ref)
        assert model_name in str(path_info["return_type"])
