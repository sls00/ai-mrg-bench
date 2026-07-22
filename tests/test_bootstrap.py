"""Bootstrap smoke tests — expanded in P0+."""

from __future__ import annotations

from workbench import __version__


def test_package_version() -> None:
    assert __version__ == "0.0.0"
