# pylint: disable=missing-module-docstring

import sys
from pathlib import Path

import pytest
import tomli_w


@pytest.fixture(scope="session")
def toml_file_init(tmp_path_factory: pytest.TempPathFactory) -> Path:
    file_path = tmp_path_factory.mktemp(".example_init") / "config.toml"
    with file_path.open(mode="wb") as fptr:
        tomli_w.dump(
            {
                "field0": 33.33,
            },
            fptr,
        )
    return file_path


def test_global_initialization(
    monkeypatch: pytest.MonkeyPatch, toml_file_init: Path
) -> None:
    monkeypatch.setattr(
        sys, "argv", ["test_global_initialization", "-a", str(toml_file_init)]
    )
    from .config_example_module_global import test_global

    assert test_global == 33.33
