from collections.abc import Iterable

import pytest

from . import utils


@pytest.mark.parametrize(
    "url,expected_output",
    [
        ("/users/1234", "/users/1234"),
        ("/users/1234#my-anchor", "/users/1234"),
        ("/users/1234?page=2&per_page=10", "/users/1234"),
    ],
)
def test_clean_url_returns_expected_value(url: str, expected_output: str) -> None:
    assert utils.clean_url(url) == expected_output


@pytest.mark.parametrize(
    "status_codes,expected_output",
    [
        ({"200": {}, "404": {}, "500": {}}, "200"),  # takes dict, str, finds 200
        ({"200": {}}.keys(), "200"),  # takes dict.keys()
        ([200, 404, 500], "200"),  # takes list, int
        ((201, 404, 500), "201"),  # takes tuple, finds 201
        ([204, 404, 500], "204"),  # finds 204
    ],
)
def test_get_2xx_status_code_returns_expected_value(
    status_codes: Iterable[int | str], expected_output: str
) -> None:
    assert utils.get_2xx_status_code(status_codes) == expected_output


def test_get_2xx_status_code_raises_ValueError_if_multiple_codes_found() -> None:
    with pytest.raises(ValueError):
        utils.get_2xx_status_code(["200", "201", "204"])


def test_get_2xx_status_code_raises_ValueError_if_no_codes_found() -> None:
    with pytest.raises(ValueError):
        utils.get_2xx_status_code(["403", "404", "500"])


def test_load_openapi_spec_succeeds() -> None:
    assert utils.load_openapi_spec()


@pytest.mark.parametrize(
    "uri,expected_output",
    [
        ("#/components/schemas/Project", "Project"),
    ],
)
def test_get_name_from_ref_returns_expected_value(
    uri: str, expected_output: str
) -> None:
    assert utils.get_name_from_ref(uri) == expected_output


@pytest.mark.parametrize(
    "format_string,url,expected_output",
    [
        ("/users/{user}", "/users/1234", True),  # named param
        ("/users/{}", "/users/1234", True),  # unnamed param
        ("/users/{}", "/users/1234/", True),  # trailing slash ok
        ("/users/{}", "/users/1234/extra", False),  # additional url sections not ok
        ("/users/{}", "https://server/users/1234", True),  # with base URL
        ("/users/{}", "/projects/1234/users/5678", False),  # partial match
        ("/projects/{}/users/{}", "/users/1234", False),  # partial match
        (
            "/projects/{project}/assigned_users/{user}",  # multiple params
            "/projects/1234/assigned_users/5678",
            True,
        ),
    ],
)
def test_match_url_returns_expected_value(
    format_string: str, url: str, expected_output: bool
) -> None:
    assert utils.match_url(format_string, url) == expected_output


@pytest.mark.parametrize(
    "url,expected_output",
    [
        ("/users/{id}", "/users/{}"),
        ("/projects/{project}/assigned_users/{user}", "/projects/{}/assigned_users/{}"),
    ],
)
def test_normalize_url_returns_expected_value(url: str, expected_output: str) -> None:
    assert utils.normalize_url(url) == expected_output
