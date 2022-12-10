import typing

import pytest

import companycam

from . import utils

CLIENT_V2 = utils.ClientTestHelper(
    managers=companycam.v2.managers, models=companycam.v2.models
)
OPENAPI = utils.OpenAPI()


@pytest.mark.parametrize("path_info", CLIENT_V2.manager_paths)
def test_all_manager_paths_exist_in_OpenAPI_spec(path_info: typing.Dict) -> None:
    assert OPENAPI.find_path(method=path_info["method"], url=path_info["url"])


def test_managers_have_same_number_of_paths_as_OpenAPI_spec() -> None:
    number_of_manager_paths = len(CLIENT_V2.manager_paths)
    number_of_spec_paths = len(OPENAPI.paths)
    assert number_of_manager_paths == number_of_spec_paths


@pytest.mark.parametrize("path_info", CLIENT_V2.manager_paths)
def test_all_manager_paths_return_same_type_as_in_OpenAPI_spec(  # noqa: C901 (complexity: 7)
    path_info: typing.Dict,
) -> None:
    try:
        method = path_info["method"]
        url = path_info["url"]
        path = OPENAPI.find_path(method=method, url=url)
    except ValueError:
        pytest.skip(
            "Path appears to be missing, but this is covered by a different unit test."
        )
    # For HTTP 204 (No Content) responses, expect bool
    if path.status_code_2xx == "204":
        assert path_info["return_type"] == bool
        return
    # For HTTP 200/201 responses
    elif path.response_json_schema:
        component = path.response_json_component
        if not component:
            pytest.fail(
                f"Cannot find $ref in {path.status_code_2xx} response for "
                f"'{method.upper()} {url}' in OpenAPI spec."
            )
        else:
            assert component in str(path_info["return_type"])
        if path.response_json_is_list:
            assert "List" in str(path_info["return_type"])
