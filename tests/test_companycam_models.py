import typing

from pytest_mock import MockerFixture

from companycam import models


class ExampleModel(models.Model):
    name: str
    address: str
    email: typing.Optional[str]


class ExampleModelWithAlias(ExampleModel):
    class Config:
        assignment_aliases = {"first_name": "name"}


def test_Model_handles_unset_assignment_aliases() -> None:
    # __init__
    obj = ExampleModel(name="Name", address="Address")
    # __getattribute__
    obj.name
    obj.address
    # __setattr__
    obj.name = "First name"


def test_Model_with_assignment_aliases_can_construct_with_original_field_names() -> None:
    assert ExampleModelWithAlias(name="Name", address="Address")


def test_Model_with_assignment_aliases_can_construct_with_aliased_field_names() -> None:
    assert ExampleModelWithAlias(first_name="Name", address="Address")


def test_Model_fields_with_assignment_aliases_can_be_accessed_by_original_name() -> None:
    assert ExampleModelWithAlias(name="Name", address="Address").name == "Name"
    assert ExampleModelWithAlias(first_name="Name", address="Address").name == "Name"


def test_Model_fields_with_assignment_aliases_can_be_accessed_by_alias() -> None:
    assert ExampleModelWithAlias(name="Name", address="Address").first_name == "Name"
    assert (
        ExampleModelWithAlias(first_name="Name", address="Address").first_name == "Name"
    )


def test_Model_fields_with_assignment_aliases_can_be_set_by_original_name() -> None:
    obj = ExampleModelWithAlias(name="Name", address="Address")
    obj.name = "New name"
    assert obj.name == "New name"


def test_Model_fields_with_assignment_aliases_can_be_set_by_alias() -> None:
    obj = ExampleModelWithAlias(name="Name", address="Address")
    obj.first_name = "New name"
    assert obj.name == "New name"


def test_Model_with_assignment_aliases_outputs_using_original_field_names() -> None:
    obj = ExampleModelWithAlias(first_name="Name", address="Address")
    dict_ = obj.dict()
    assert "name" in dict_
    assert "first_name" not in dict_


def test_Model_dict_defaults_exclude_none_to_True(mocker: MockerFixture) -> None:
    mock = mocker.patch("pydantic.BaseModel.dict")
    obj = ExampleModel(name="Name", address="Address")
    obj.dict()
    assert "exclude_none" in mock.call_args.kwargs
    assert mock.call_args.kwargs["exclude_none"] is True


def test_Model_dict_can_set_exclude_none_to_False(mocker: MockerFixture) -> None:
    mock = mocker.patch("pydantic.BaseModel.dict")
    obj = ExampleModel(name="Name", address="Address")
    obj.dict(exclude_none=False)
    assert "exclude_none" in mock.call_args.kwargs
    assert mock.call_args.kwargs["exclude_none"] is False


def test_Model_dict_exclude_none_ensures_None_values_are_excluded() -> None:
    obj = ExampleModel(name="Name", address="Address")
    dict_ = obj.dict()
    assert "email" not in dict_


def test_Model_dict_exclude_none_can_be_overridden() -> None:
    obj = ExampleModel(name="Name", address="Address")
    dict_ = obj.dict(exclude_none=False)
    assert "email" in dict_
