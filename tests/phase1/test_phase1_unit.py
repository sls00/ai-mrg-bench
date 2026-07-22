"""P1 unit tests for the adverse-action translator building blocks."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from workbench.adverse_action.feature_dictionary import (
    describe_factor,
    is_mapped_specifically,
)
from workbench.config import ValidationRunConfig

pytestmark = pytest.mark.phase1


def test_baseline_config_enables_adverse_action_without_drift() -> None:
    config = ValidationRunConfig.from_yaml(Path("configs/german_credit_baseline.yaml"))
    assert config.modules.bias_battery is True
    assert config.modules.adverse_action_translator is True
    assert config.modules.drift_monitor is False


def test_describe_factor_uses_specific_categorical_level() -> None:
    row = pd.Series({"checking_status": "A14"})
    description = describe_factor("checking_status", row)
    assert description == "no checking account on file"
    assert is_mapped_specifically("checking_status", row) is True


def test_describe_factor_falls_back_for_unknown_categorical_code() -> None:
    row = pd.Series({"checking_status": "A99"})
    description = describe_factor("checking_status", row)
    assert "A99" in description
    assert is_mapped_specifically("checking_status", row) is False


def test_describe_factor_renders_numeric_template() -> None:
    row = pd.Series({"duration": 24.0})
    description = describe_factor("duration", row)
    assert description == "requested loan duration of 24 months"
    assert is_mapped_specifically("duration", row) is True
