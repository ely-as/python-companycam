from inspect import getmembers, isclass
from typing import Dict, List, Type

from companycam import models
from pydantic import BaseModel
import pytest

from .openapi import load_openapi_spec

ALL_MODELS = dict(
    getmembers(models, lambda m: isclass(m) and m.__module__ == models.__name__)
)
OPENAPI_SPEC = load_openapi_spec()


def get_model_from_component_name(component_name: str) -> Type[BaseModel]:
    """Get pydantic model from the name of an OpenAPI Component or skip test if not found."""
    try:
        return ALL_MODELS[component_name]
    except KeyError:
        return pytest.skip(
            f"Pydantic model with name '{component_name}' not found, skipping because error is covered by a different test"
        )


def get_model_property_fields_from_property_name(
    model: Type[BaseModel], property_name: str
) -> Dict:
    """Get property fields from pydantic model schema or skip test if not found."""
    try:
        return model.schema()["properties"][property_name]
    except KeyError:
        return pytest.skip(
            f"Pydantic model '{model}' missing field with name '{property_name}', skipping because error is covered by a different test"
        )


def get_name_from_ref(uri: str) -> str:
    """Get component name from a Reference Object $ref field."""
    return uri.split("/")[:-1][0]


@pytest.mark.parametrize("name,model", ALL_MODELS.items())
def test_pydantic_model_name_matches_an_OpenAPI_component(
    name: str, model: Type[BaseModel]
):
    assert model.schema()["title"] in OPENAPI_SPEC["components"]["schemas"]


@pytest.mark.parametrize("component_name", OPENAPI_SPEC["components"]["schemas"].keys())
def test_OpenAPI_component_matches_a_pydantic_model(component_name: str):
    assert component_name in ALL_MODELS


@pytest.mark.parametrize(
    "component_name,required",
    [
        (name, fields.get("required", []))
        for name, fields in OPENAPI_SPEC["components"]["schemas"].items()
    ],
)
def test_required_OpenAPI_properties_are_required_in_pydantic_model(
    component_name: str, required: List[str]
):
    model = get_model_from_component_name(component_name)
    assert required == model.schema().get("required", [])


@pytest.mark.parametrize(
    "component_name,property_names",
    [
        (name, [p for p in fields["properties"]])
        for name, fields in OPENAPI_SPEC["components"]["schemas"].items()
    ],
)
def test_pydantic_models_have_the_same_properties_as_OpenAPI_components(
    component_name: str, property_names: List[str]
):
    model = get_model_from_component_name(component_name)
    assert property_names == [p for p in model.schema()["properties"]]


@pytest.mark.parametrize(
    "component_name,property_name,property_fields",
    [
        (name, property_name, property_fields)
        for name, fields in OPENAPI_SPEC["components"]["schemas"].items()
        for property_name, property_fields in fields["properties"].items()
    ],
)
def test_pydantic_model_fields_have_same_type_as_OpenAPI_component_properties(
    component_name: str, property_name: str, property_fields: Dict
):
    model = get_model_from_component_name(component_name)
    model_property_fields = get_model_property_fields_from_property_name(
        model, property_name
    )
    if "$ref" in model_property_fields:
        assert get_name_from_ref(property_fields["$ref"]) or get_name_from_ref(
            model_property_fields["$ref"]
        )
    elif "type" in model_property_fields:
        assert property_fields["type"] == model_property_fields["type"]
    else:
        pytest.fail(
            f"Field '{property_name}' in pydantic model '{model}' has no schema attribute to type check "
            "with i.e. '$ref' or 'type'"
        )


@pytest.mark.parametrize(
    "component_name,property_name,enum",
    [
        (name, property_name, property_fields["enum"])
        for name, fields in OPENAPI_SPEC["components"]["schemas"].items()
        for property_name, property_fields in fields["properties"].items()
        if "enum" in property_fields
    ],
)
def test_pydantic_model_Literal_fields_have_same_enum_options_as_OpenAPI_component_properties(
    component_name: str, property_name: str, enum: List[str]
):
    model = get_model_from_component_name(component_name)
    model_property_fields = get_model_property_fields_from_property_name(
        model, property_name
    )
    if "enum" in model_property_fields:
        assert model_property_fields["enum"] == enum
    else:
        pytest.fail(
            f"Expected field '{property_name}' in pydantic model '{model}' to be a fixed field with enum={enum}"
        )
