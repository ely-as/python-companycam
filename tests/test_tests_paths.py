import inspect
import pathlib

import pytest

from . import paths


@pytest.mark.parametrize(
    "name,path", inspect.getmembers(paths, lambda m: isinstance(m, pathlib.Path))
)
def test_path_exists(name: str, path: pathlib.Path) -> None:
    assert path.exists()
