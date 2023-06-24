import json

import jsonschema
import pytest
from pytest_mock import MockerFixture

import companycam

from . import utils
from .fixtures import v2_model_objects

CLIENT_V2 = utils.ClientTestHelper(
    managers=companycam.v2.managers, models=companycam.v2.models
)
OPENAPI = utils.OpenAPI()


def OPENAPI_find_path_with_skip(method: str, url: str) -> utils.OpenAPIPath:  # type: ignore[return]
    """This function assumes that `test_all_manager_paths_exist_in_OpenAPI_spec()`
    exists and will fail if `OpenAPI.find_path()` raises a `ValueError`.
    """
    try:
        return OPENAPI.find_path(method=method, url=url)
    except ValueError:
        pytest.skip(
            "Path appears to be missing in OpenAPI spec, but this is covered by a "
            "different unit test."
        )


@pytest.mark.parametrize("path", CLIENT_V2.manager_paths)
def test_all_manager_paths_exist_in_OpenAPI_spec(path: utils.ManagerPath) -> None:
    assert OPENAPI.find_path(method=path.method, url=path.url)


def test_managers_have_same_number_of_paths_as_OpenAPI_spec() -> None:
    number_of_manager_paths = len(CLIENT_V2.manager_paths)
    number_of_spec_paths = len(OPENAPI.paths)
    assert number_of_manager_paths == number_of_spec_paths


@pytest.mark.parametrize("manager_path", CLIENT_V2.manager_paths)
def test_all_manager_paths_return_same_type_as_in_OpenAPI_spec(  # noqa: C901 (complexity: 7)
    manager_path: utils.ManagerPath,
) -> None:
    method = manager_path.method
    url = manager_path.url
    openapi_path = OPENAPI_find_path_with_skip(method=method, url=url)
    # For HTTP 204 (No Content) responses, expect bool
    if openapi_path.status_code_2xx == "204":
        assert manager_path.return_type == bool
    # For HTTP 200/201 responses
    elif openapi_path.response_json_schema:
        component = openapi_path.response_json_component
        if not component:
            pytest.fail(
                f"Cannot find $ref in {openapi_path.status_code_2xx} response for "
                f"'{method.upper()} {url}' in OpenAPI spec."
            )
        else:
            assert component in str(manager_path.return_type)
        if openapi_path.response_json_is_list:
            assert "list[" in str(manager_path.return_type).lower()


@pytest.mark.parametrize("path", CLIENT_V2.manager_paths)
def test_all_manager_paths_return_successfully(
    mocker: MockerFixture, path: utils.ManagerPath
) -> None:
    utils.ClientSendPatcher(mocker)
    path.call(**path.filter_kwargs(**v2_model_objects.KWARGS))


@pytest.mark.parametrize("path", CLIENT_V2.manager_paths)
def test_all_manager_paths_accept_query_parameters_if_specified_in_OpenAPI_spec(
    mocker: MockerFixture, path: utils.ManagerPath
) -> None:
    openapi_path = OPENAPI_find_path_with_skip(method=path.method, url=path.url)
    if openapi_path.query_parameters:
        patch = utils.ClientSendPatcher(mocker)
        kwargs = path.filter_kwargs(**v2_model_objects.KWARGS)
        kwargs["query"] = {"page": 2}
        path.call(**kwargs)
        assert "page=2" in str(patch.request.url)


@pytest.mark.parametrize("path", CLIENT_V2.manager_paths)
def test_all_manager_paths_generate_correct_JSON_in_requests_as_per_OpenAPI_spec(
    mocker: MockerFixture, path: utils.ManagerPath
) -> None:
    openapi_path = OPENAPI_find_path_with_skip(method=path.method, url=path.url)
    if schema := openapi_path.request_json_schema:
        patch = utils.ClientSendPatcher(mocker)
        path.call(**path.filter_kwargs(**v2_model_objects.KWARGS))
        data = json.loads(patch.request.content)
        schema["components"] = OPENAPI.spec["components"]
        jsonschema.validate(instance=data, schema=schema)
