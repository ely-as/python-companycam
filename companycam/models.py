from typing import Any

import pydantic

from companycam.utils import PYDANTIC_VERSION


class Model(pydantic.BaseModel):
    """Implements a custom Config option `assignment_aliases`. Allows fields to be
    assigned to via an alias (in both object construction and attribute assignment), but
    preserves the original field name in any outputs.

    Cannot simply use @property setters with pydantic, see
    https://github.com/pydantic/pydantic/issues/1577.
    """

    @property
    def _assignment_aliases(self) -> dict:
        if PYDANTIC_VERSION >= (2, 0, 0):
            config = super().__getattribute__("model_config")
            if aliases := config.get("assignment_aliases"):
                return aliases
            else:
                try:
                    configCls = super().__getattribute__("Config")
                    return getattr(configCls, "assignment_aliases", {})
                except AttributeError:
                    return {}
        else:
            config = super().__getattribute__("__config__")
            return getattr(config, "assignment_aliases", {})

    def __init__(self, *args, **kwargs) -> None:
        assignment_aliases = super().__getattribute__("_assignment_aliases")
        for alias, field_name in assignment_aliases.items():
            if alias in kwargs and field_name not in kwargs:
                kwargs[field_name] = kwargs.pop(alias)
        super().__init__(*args, **kwargs)

    def __getattribute__(self, name: str) -> Any:
        assignment_aliases = super().__getattribute__("_assignment_aliases")
        if name in assignment_aliases:
            name = assignment_aliases[name]
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        assignment_aliases = super().__getattribute__("_assignment_aliases")
        if name in assignment_aliases:
            name = assignment_aliases[name]
        return super().__setattr__(name, value)

    def model_dump(self, *, exclude_none: bool = True, **kwargs) -> dict[str, Any]:
        if PYDANTIC_VERSION >= (2, 0, 0):
            return super().model_dump(exclude_none=exclude_none, **kwargs)
        return super().dict(exclude_none=exclude_none, **kwargs)

    @classmethod
    def model_json_schema(cls, *args, **kwargs) -> dict[str, Any]:
        if PYDANTIC_VERSION >= (2, 0, 0):
            return super().model_json_schema(*args, **kwargs)
        return super().schema(*args, **kwargs)

    if PYDANTIC_VERSION >= (2, 0, 0):
        model_config = pydantic.ConfigDict(coerce_numbers_to_str=True)


class ModelWithRequiredID(Model):
    # 'id' is a required field in most models where it is a field, but we want users to
    # be able to construct model objects without an 'id' since that is set by the API
    id: str | None = None
