"""Shared fixtures for phase1 tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from workbench.config import ValidationRunConfig
from workbench.sdk import ValidationResult, ValidationRun


@dataclass(slots=True)
class Phase1Run:
    config: ValidationRunConfig
    result: ValidationResult
    db_path: Path


@pytest.fixture(scope="session")
def phase1_run(tmp_path_factory: pytest.TempPathFactory) -> Phase1Run:
    config_path = Path("configs/german_credit_baseline.yaml")
    if not config_path.exists():
        pytest.fail("Missing configs/german_credit_baseline.yaml")

    config = ValidationRunConfig.from_yaml(config_path)
    run_root = tmp_path_factory.mktemp("phase1-artifacts")
    config.run_id = "pytest-phase1"
    config.audit.db_path = run_root / "workbench-phase1.db"
    config.outputs.artifact_dir_template = str(run_root / "{run_id}")

    result = ValidationRun(config).run()
    return Phase1Run(config=config, result=result, db_path=config.audit.db_path)
