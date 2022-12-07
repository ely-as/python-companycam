import typing

import pydantic


class ModelWithRequiredID(pydantic.BaseModel):
    # 'id' is a required field in most models where it is a field, but we want users to
    # be able to construct model objects without an 'id' since that is set by the API
    id: typing.Optional[str]
