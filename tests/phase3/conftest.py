"""Shared fixtures for phase3 CA/CO overlay tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from workbench.config import ValidationRunConfig
from workbench.sdk import ValidationResult, ValidationRun


@dataclass(slots=True)
class Phase3Run:
    config: ValidationRunConfig
    result: ValidationResult
    db_path: Path


def _run_overlay_config(
    *,
    config_path: Path,
    run_root: Path,
    run_id: str,
) -> Phase3Run:
    if not config_path.exists():
        pytest.fail(f"Missing {config_path}")

    config = ValidationRunConfig.from_yaml(config_path)
    config.run_id = run_id
    config.audit.db_path = run_root / f"workbench-{run_id}.db"
    config.outputs.artifact_dir_template = str(run_root / "{run_id}")

    result = ValidationRun(config).run()
    return Phase3Run(config=config, result=result, db_path=config.audit.db_path)


@pytest.fixture(scope="session")
def phase3_ca_run(tmp_path_factory: pytest.TempPathFactory) -> Phase3Run:
    run_root = tmp_path_factory.mktemp("phase3-ca")
    return _run_overlay_config(
        config_path=Path("configs/german_credit_ca_overlay.yaml"),
        run_root=run_root,
        run_id="pytest-phase3-ca",
    )


@pytest.fixture(scope="session")
def phase3_co_run(tmp_path_factory: pytest.TempPathFactory) -> Phase3Run:
    run_root = tmp_path_factory.mktemp("phase3-co")
    return _run_overlay_config(
        config_path=Path("configs/german_credit_co_overlay.yaml"),
        run_root=run_root,
        run_id="pytest-phase3-co",
    )


@pytest.fixture(scope="session")
def phase3_baseline_run(tmp_path_factory: pytest.TempPathFactory) -> Phase3Run:
    """Baseline full run (state_overlay: none) for §II byte-for-byte regression."""
    run_root = tmp_path_factory.mktemp("phase3-baseline")
    return _run_overlay_config(
        config_path=Path("configs/german_credit_full.yaml"),
        run_root=run_root,
        run_id="pytest-phase3-baseline",
    )
