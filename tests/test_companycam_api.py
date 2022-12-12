import typing  # noqa: F401 (used by eval)

import pytest

from companycam import api


def test_API_version_arg_type_matches_SUPPORTED_VERSIONS() -> None:
    # We cannot cast the type e.g. Literal[*SUPPORTED_VERSIONS], so check that
    # it's defined consistently in both places
    try:
        type_ = eval(api.API.__init__.__annotations__["version"])
    except NameError as exc:
        pytest.fail(
            "Could not evaluate type annotation for arg 'version' in companycam.api.API.__init__. "
            f"Ensure the correct names are imported in {__name__}. "
            f"{exc.__class__.__name__}: {exc}"
        )
    assert list(type_.__args__) == list(api.SUPPORTED_VERSIONS)
