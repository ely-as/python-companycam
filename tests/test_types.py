import httpx
import pytest

from companycam import types


@pytest.mark.parametrize("type_name", ["PrimitiveData", "QueryParamTypes"])
def test_types_copied_from_HTTPX__types_have_not_changed(type_name: str) -> None:
    assert getattr(httpx._types, type_name) == getattr(types, type_name)
