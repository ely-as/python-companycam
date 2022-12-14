from pathlib import Path

# directories
TEST_DIR = Path(__file__).parent
FIXTURES_DIR = TEST_DIR / "fixtures"
ROOT_DIR = TEST_DIR.parent

# fixture files
FIXTURE_V2_RESPONSES = FIXTURES_DIR / "v2_2xx_responses.json"

# companycam/openapi-spec files
OPENAPI_YAML = ROOT_DIR / "openapi-spec/openapi.yaml"
POSTMAN_COLLECTION = ROOT_DIR / "openapi-spec/CompanyCam v2.postman_collection.json"
