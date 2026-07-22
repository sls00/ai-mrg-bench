"""Shared pytest configuration and phase markers."""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    for marker in (
        "phase0",
        "phase1",
        "phase2",
        "phase3",
        "phase4",
        "api",
    ):
        config.addinivalue_line("markers", f"{marker}: see pyproject.toml markers table")
