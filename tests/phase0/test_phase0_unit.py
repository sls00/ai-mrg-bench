"""P0 unit tests for intake and tiering behavior."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from workbench.config import ValidationRunConfig
from workbench.ingest import enforce_protected_class_gate, run_intake_gate
from workbench.materiality import assign_materiality_tier

pytestmark = pytest.mark.phase0


def test_intake_gate_passes_for_statistical_credit_model() -> None:
    config = ValidationRunConfig.from_yaml(Path("configs/german_credit_p0.yaml"))
    result = run_intake_gate(config)
    assert result.status == "PASS"


def test_materiality_assigns_t3_for_credit_decisioning() -> None:
    materiality = assign_materiality_tier(exposure=0.15, purpose="credit_decisioning")
    assert materiality.tier == "T3"


def test_protected_class_gate_rejects_model_input() -> None:
    with pytest.raises(ValueError, match="Protected-class ingest gate failed"):
        enforce_protected_class_gate(
            model_features=["duration", "sex", "credit_amount"],
            protected_names={"sex"},
        )


def test_banlist_script_passes() -> None:
    proc = subprocess.run(
        ["bash", "scripts/check_circular_banlist.sh"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
