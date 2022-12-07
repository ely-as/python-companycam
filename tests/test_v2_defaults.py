from companycam.v2 import defaults

from .openapi import load_openapi_spec

OPENAPI_SPEC = load_openapi_spec()


def test_SERVER_URL_matches_spec() -> None:
    assert OPENAPI_SPEC["servers"][0]["url"] == defaults.SERVER_URL


def test_spec_contains_only_one_server() -> None:
    # the spec supports a list of servers, but we assume there's only one, so test this assumption
    assert len(OPENAPI_SPEC["servers"]) == 1
