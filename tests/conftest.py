import importlib.resources
from contextlib import AbstractContextManager, ExitStack, contextmanager
from importlib.abc import Traversable
from pathlib import Path
from typing import Callable, Iterator

import pytest

TEST_DATA_PKG = "ppm2._test_data"
TEST_DATA_RESOURCES = importlib.resources.files(TEST_DATA_PKG)

def gen_resource_paths(
    resources: Traversable,
) -> Callable[
    *tuple[Path, ...],
    AbstractContextManager[Path | list[Path]],
]:
    """Generate a context manager funtion that takes a set of file paths and
    yielding a list of real pathlib.Path objects for the given filenames."""

    @contextmanager
    def resource_paths(
        *filenames: str | Path,
    ) -> Iterator[Path | list[Path]]:

        with ExitStack() as stack:
            paths = []
            for name in filenames:
                resource = resources.joinpath(str(name))
                path = stack.enter_context(importlib.resources.as_file(resource))
                paths.append(path)

            if len(paths) == 0:
                raise ValueError("No paths in resources found.")
            elif len(paths) > 1:
                yield paths
            else:
                yield paths[0]

    return resource_paths


TEST_DATA = gen_resource_paths(TEST_DATA_RESOURCES)


@pytest.fixture(scope="session")
def test_data():
    return TEST_DATA
