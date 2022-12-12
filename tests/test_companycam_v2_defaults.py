from companycam.v2 import defaults

from . import utils

OPENAPI = utils.OpenAPI()


def test_SERVER_URL_matches_spec() -> None:
    assert OPENAPI.spec["servers"][0]["url"] == defaults.SERVER_URL


def test_spec_contains_only_one_server() -> None:
    # the spec supports a list of servers, but we assume there's only one, so test this assumption
    assert len(OPENAPI.spec["servers"]) == 1
