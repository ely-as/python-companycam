import pytest

from . import utils

OPENAPI = utils.OpenAPI()


@pytest.mark.parametrize("path", OPENAPI.paths)
def test_all_paths_in_OpenAPI_spec_which_return_200_or_201_also_return_JSON_content(
    path: utils.OpenAPIPath,
) -> None:
    """BaseManager assumes that response data will be JSON, so test this
    assumption against the spec.
    """
    if path.status_code_2xx in ["200", "201"]:
        assert path.response_json_schema
