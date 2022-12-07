from pathlib import Path
from typing import Dict

import yaml

PATH_TO_OPENAPI_YAML: Path = Path(__file__).parent.parent / "openapi-spec/openapi.yaml"


def get_name_from_ref(uri: str) -> str:
    """Get component name from a Reference Object $ref field."""
    return uri.split("/")[:-1][0]


def load_openapi_spec() -> Dict:
    data = {}
    with open(PATH_TO_OPENAPI_YAML, "r") as f:
        data = yaml.safe_load(f)
    return data
