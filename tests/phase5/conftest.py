"""Shared fixtures for phase5 (P5 synth-fin CRE) tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from workbench.config import ValidationRunConfig
from workbench.sdk import ValidationResult, ValidationRun


@dataclass(slots=True)
class Phase5Run:
    config: ValidationRunConfig
    result: ValidationResult
    db_path: Path


@pytest.fixture(scope="session")
def phase5_run(tmp_path_factory: pytest.TempPathFactory) -> Phase5Run:
    config_path = Path("configs/synth_fin_cre_baseline.yaml")
    if not config_path.exists():
        pytest.fail("Missing configs/synth_fin_cre_baseline.yaml")

    config = ValidationRunConfig.from_yaml(config_path)
    run_root = tmp_path_factory.mktemp("phase5-artifacts")
    config.run_id = "pytest-phase5"
    config.audit.db_path = run_root / "workbench-phase5.db"
    config.outputs.artifact_dir_template = str(run_root / "{run_id}")

    result = ValidationRun(config).run()
    return Phase5Run(config=config, result=result, db_path=config.audit.db_path)
