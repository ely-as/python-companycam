from typing import TYPE_CHECKING, List, Mapping, Optional, Sequence, Tuple, Union

if TYPE_CHECKING:
    from httpx import QueryParams

# Copied from httpx._types. They are copied and not used directly since they are not part of HTTPX's API
# (i.e. module begins with an underscore) and could change unexpectedly.

PrimitiveData = Optional[Union[str, int, float, bool]]

QueryParamTypes = Union[
    "QueryParams",
    Mapping[str, Union[PrimitiveData, Sequence[PrimitiveData]]],
    List[Tuple[str, PrimitiveData]],
    Tuple[Tuple[str, PrimitiveData], ...],
    str,
    bytes,
]
