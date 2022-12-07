import typing

import pytest

from .openapi import load_openapi_spec

OPENAPI_SPEC = load_openapi_spec()


@pytest.mark.parametrize(
    "path,method,response",
    [
        (path, method, response)
        for path, methods in OPENAPI_SPEC["paths"].items()
        for method, method_dict in methods.items()
        for status_code, response in method_dict["responses"].items()
        if status_code in ["200", "201"]
    ],
)
def test_all_paths_in_OpenAPI_spec_which_return_200_or_201_also_return_JSON_content(
    path: str, method: str, response: typing.Dict
) -> None:
    """BaseManager assumes that response data will be JSON, so test this
    assumption against the spec.
    """
    content = response["content"]
    if "application/json" not in content:
        pytest.fail(
            f"{method.upper()} {path} does not return JSON data i.e. 'application/json' not in {content}"
        )
