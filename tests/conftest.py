from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def the_test_dir() -> Path:
    return Path(__file__).absolute().parent


@pytest.fixture(scope="session")
def simple_py_script(the_test_dir: Path) -> Path:
    return the_test_dir / "data" / "simple.py"
