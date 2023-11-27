import pytest
from pydantic import BaseModel

import companycam
from companycam.utils import model_json_schema

from . import utils

CLIENT_V2 = utils.ClientTestHelper(
    managers=companycam.v2.managers, models=companycam.v2.models
)
OPENAPI = utils.OpenAPI()


def get_model_from_component_name(component_name: str) -> type[BaseModel]:
    """Get pydantic model from the name of an OpenAPI Component or skip test if not found."""
    try:
        return CLIENT_V2.models[component_name]
    except KeyError:
        return pytest.skip(
            f"Pydantic model with name '{component_name}' not found, skipping because error is covered by a different test"
        )


def get_model_property_fields_from_property_name(
    model: type[BaseModel], property_name: str
) -> dict:
    """Get property fields from pydantic model schema or skip test if not found."""
    try:
        fields = model_json_schema(model)["properties"][property_name]
        # The following update pulls the 'type' or '$ref' key-value back into the
        # top-level dict, so output from V1 and V2 are compatible i.e.:
        # V1 : {'title': 'Id', 'type': 'string'}
        # V2 : {'anyOf': [{'type': 'string'}, {'type': 'null'}], 'default': None, 'title': 'Id'}
        #
        # V1 : {'$ref': '#/definitions/Address'}
        # V2 : {'anyOf': [{'$ref': '#/$defs/Address'}, {'type': 'null'}], 'default': None}
        fields.update(
            {k: v for t in fields.get("anyOf", []) for k, v in t.items() if v != "null"}
        )
        return fields
    except KeyError:
        return pytest.skip(
            f"Pydantic model '{model}' missing field with name '{property_name}', skipping because error is covered by a different test"
        )


@pytest.mark.parametrize("name,model", CLIENT_V2.models.items())
def test_pydantic_model_name_matches_an_OpenAPI_component(
    name: str, model: type[BaseModel]
) -> None:
    assert model_json_schema(model)["title"] in OPENAPI.component_schemas


@pytest.mark.parametrize("component_name", OPENAPI.component_schemas)
def test_OpenAPI_component_matches_a_pydantic_model(component_name: str) -> None:
    assert component_name in CLIENT_V2.models


@pytest.mark.parametrize(
    "component_name,required",
    [
        (name, fields.get("required", []))
        for name, fields in OPENAPI.component_schemas.items()
    ],
)
def test_required_OpenAPI_properties_are_required_in_pydantic_model_except_for_id(
    component_name: str, required: list[str]
) -> None:
    model = get_model_from_component_name(component_name)
    model_required = model_json_schema(model).get("required", [])
    if "id" in required:
        required.remove("id")
    assert required == model_required


@pytest.mark.parametrize(
    "component_name,property_names",
    [
        (name, list(fields["properties"]))
        for name, fields in OPENAPI.component_schemas.items()
    ],
)
def test_pydantic_models_have_the_same_properties_as_OpenAPI_components(
    component_name: str, property_names: list[str]
) -> None:
    model = get_model_from_component_name(component_name)
    assert property_names == list(model_json_schema(model)["properties"])


@pytest.mark.parametrize(
    "component_name,property_name,property_fields",
    [
        (name, property_name, property_fields)
        for name, fields in OPENAPI.component_schemas.items()
        for property_name, property_fields in fields["properties"].items()
    ],
)
def test_pydantic_model_fields_have_same_type_as_OpenAPI_component_properties(
    component_name: str, property_name: str, property_fields: dict
) -> None:
    model = get_model_from_component_name(component_name)
    model_property_fields = get_model_property_fields_from_property_name(
        model, property_name
    )
    if "$ref" in model_property_fields:
        assert utils.get_name_from_ref(
            property_fields["$ref"]
        ) or utils.get_name_from_ref(model_property_fields["$ref"])
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
        for name, fields in OPENAPI.component_schemas.items()
        for property_name, property_fields in fields["properties"].items()
        if "enum" in property_fields
    ],
)
def test_pydantic_model_Literal_fields_have_same_enum_options_as_OpenAPI_component_properties(
    component_name: str, property_name: str, enum: list[str]
) -> None:
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


def test_Photo_model_can_coerce_coordinates_input_to_list() -> None:
    Photo = CLIENT_V2.models["Photo"]
    photo = Photo(coordinates={"lat": 0.0, "lon": 0.0})
    assert isinstance(photo.coordinates, list)
