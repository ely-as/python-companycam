import typing

import pydantic


class Model(pydantic.BaseModel):
    """Implements a custom Config option `assignment_aliases`. Allows fields to be
    assigned to via an alias (in both object construction and attribute assignment), but
    preserves the original field name in any outputs.

    Cannot simply use @property setters with pydantic, see
    https://github.com/pydantic/pydantic/issues/1577.
    """

    class Config:
        assignment_aliases: typing.Dict[str, str]

    def __init__(self, *args, **kwargs) -> None:
        config = super().__getattribute__("__config__")
        assignment_aliases = getattr(config, "assignment_aliases", {})
        for alias, field_name in assignment_aliases.items():
            if alias in kwargs and field_name not in kwargs:
                kwargs[field_name] = kwargs.pop(alias)
        super().__init__(*args, **kwargs)

    def __getattribute__(self, name: str) -> typing.Any:
        config = super().__getattribute__("__config__")
        assignment_aliases = getattr(config, "assignment_aliases", {})
        if name in assignment_aliases:
            name = assignment_aliases[name]
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: typing.Any) -> None:
        config = super().__getattribute__("__config__")
        assignment_aliases = getattr(config, "assignment_aliases", {})
        if name in assignment_aliases:
            name = assignment_aliases[name]
        return super().__setattr__(name, value)

    def dict(self, exclude_none: bool = True, **kwargs) -> typing.Dict[str, typing.Any]:
        return super().dict(exclude_none=exclude_none, **kwargs)


class ModelWithRequiredID(Model):
    # 'id' is a required field in most models where it is a field, but we want users to
    # be able to construct model objects without an 'id' since that is set by the API
    id: typing.Optional[str]
