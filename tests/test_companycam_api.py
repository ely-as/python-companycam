from companycam import api


def test_API_version_arg_type_matches_SUPPORTED_VERSIONS() -> None:
    # We cannot cast the type e.g. Literal[*SUPPORTED_VERSIONS], so check that
    # it's defined consistently in both places
    type_ = api.API.__init__.__annotations__["version"]
    assert list(type_.__args__) == list(api.SUPPORTED_VERSIONS)
