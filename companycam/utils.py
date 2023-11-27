from typing import Any, TypeVar

import pydantic

T = TypeVar("T")


def pydantic_version() -> tuple[int, ...]:
    version = [int(n) for n in pydantic.VERSION.split(".")][:3]
    return tuple(n for n in version)


PYDANTIC_VERSION: tuple[int, ...] = pydantic_version()


def parse_obj_as(type_: type[T], obj: Any) -> T:
    if PYDANTIC_VERSION >= (2, 0, 0):
        # TypeAdapter introduced in V2
        return pydantic.TypeAdapter(type_).validate_python(obj)
    else:
        # parse_obj_as deprecated in V2, removed in V3
        return pydantic.parse_obj_as(type_, obj)
