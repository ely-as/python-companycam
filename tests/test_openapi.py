from .openapi import PATH_TO_OPENAPI_YAML, load_openapi_spec


def test_openapi_yaml_file_exists() -> None:
    assert PATH_TO_OPENAPI_YAML.exists()


def test_load_openapi_spec_returns() -> None:
    assert load_openapi_spec()
