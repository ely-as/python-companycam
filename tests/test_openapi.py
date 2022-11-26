from .openapi import PATH_TO_OPENAPI_YAML, load_openapi_spec


def test_openapi_yaml_file_exists():
    assert PATH_TO_OPENAPI_YAML.exists()


def test_load_openapi_spec_returns():
    assert load_openapi_spec()
