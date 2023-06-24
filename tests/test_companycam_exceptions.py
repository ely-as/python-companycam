import pytest

from companycam import exceptions


def test_subclasses_of_BaseCompanyCamException_have_unique_status_codes() -> None:
    no_subclasses = 0
    status_codes = set()
    for exc in exceptions.BaseCompanyCamException.__subclasses__():
        no_subclasses += 1
        status_codes.add(exc.status_code)
    assert no_subclasses == len(status_codes)


@pytest.mark.parametrize("cls", exceptions.BaseCompanyCamException.__subclasses__())
def test_subclasses_of_BaseCompanyCamException_have_no_subclasses(
    cls: type[exceptions.BaseCompanyCamException],
) -> None:
    assert len(cls.__subclasses__()) == 0
