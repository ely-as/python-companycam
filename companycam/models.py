import typing

import pydantic


class Model(pydantic.BaseModel):
    def dict(self, **kwargs) -> typing.Dict[str, typing.Any]:
        # Default exclude_none to True rather than False
        kwargs["exclude_none"] = kwargs.pop("exclude_none", True)
        return super().dict(**kwargs)


class ModelWithRequiredID(Model):
    # 'id' is a required field in most models where it is a field, but we want users to
    # be able to construct model objects without an 'id' since that is set by the API
    id: typing.Optional[str]
