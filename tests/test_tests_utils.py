import pytest

from . import utils


def test_openapi_yaml_file_exists() -> None:
    assert utils.PATH_TO_OPENAPI_YAML.exists()


def test_load_openapi_spec_returns() -> None:
    assert utils.load_openapi_spec()


@pytest.mark.parametrize(
    "input,expected_output",
    [
        ("#/components/schemas/Project", "Project"),
    ],
)
def test_get_name_from_ref_returns_expected_value(
    input: str, expected_output: str
) -> None:
    assert utils.get_name_from_ref(input) == expected_output


@pytest.mark.parametrize(
    "input,expected_output",
    [
        ("/users/{id}", "/users/{}"),
        ("/projects/{project}/assigned_users/{user}", "/projects/{}/assigned_users/{}"),
    ],
)
def test_normalize_url_returns_expected_value(input: str, expected_output: str) -> None:
    assert utils.normalize_url(input) == expected_output
