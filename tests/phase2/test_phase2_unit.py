"""P2 unit tests for the drift monitor building blocks."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from workbench.config import ValidationRunConfig
from workbench.drift import (
    ESCALATION_ACTIONS,
    combine_alert_levels,
    escalation_action,
    ks_alert_level,
    monitoring_cadence,
    population_stability_index,
    psi_alert_level,
)

pytestmark = pytest.mark.phase2


def test_full_config_enables_all_three_modules() -> None:
    config = ValidationRunConfig.from_yaml(Path("configs/german_credit_full.yaml"))
    assert config.modules.bias_battery is True
    assert config.modules.adverse_action_translator is True
    assert config.modules.drift_monitor is True
    assert config.run_id == "german-credit-demo-v1"
    assert config.reference_dataset_path is not None
    assert config.monitor_dataset_path is not None
    assert config.reference_dataset_path.name == "german_credit_train.csv"
    assert config.monitor_dataset_path.name == "german_credit_monitor.csv"


def test_drift_monitor_requires_reference_and_monitor_datasets(tmp_path: Path) -> None:
    payload = Path("configs/german_credit_p0.yaml").read_text()
    bad_config_path = tmp_path / "bad.yaml"
    bad_config_path.write_text(payload.replace("drift_monitor: false", "drift_monitor: true"))
    with pytest.raises(ValueError, match="drift_monitor"):
        ValidationRunConfig.from_yaml(bad_config_path)


def test_psi_thresholds_classify_green_amber_red() -> None:
    assert psi_alert_level(0.05) == "green"
    assert psi_alert_level(0.10) == "amber"
    assert psi_alert_level(0.24) == "amber"
    assert psi_alert_level(0.25) == "red"


def test_ks_pvalue_thresholds_classify_alerts() -> None:
    assert ks_alert_level(0.5) == "green"
    assert ks_alert_level(0.03) == "amber"
    assert ks_alert_level(0.005) == "red"


def test_combine_alert_levels_takes_max_severity() -> None:
    assert combine_alert_levels("green", "amber") == "amber"
    assert combine_alert_levels("red", "green", "amber") == "red"
    assert combine_alert_levels("green", "green") == "green"


def test_population_stability_index_zero_for_identical_distributions() -> None:
    reference = np.linspace(0, 1, 500)
    psi = population_stability_index(reference, reference)
    assert psi == pytest.approx(0.0, abs=1e-9)


def test_population_stability_index_rises_with_shift() -> None:
    rng = np.random.default_rng(42)
    reference = rng.normal(loc=0.0, scale=1.0, size=1000)
    shifted = rng.normal(loc=2.0, scale=1.0, size=1000)
    psi = population_stability_index(reference, shifted)
    assert psi > 0.25


def test_escalation_actions_cover_all_tiers_and_alert_levels() -> None:
    for tier in ("T1", "T2", "T3"):
        for alert in ("green", "amber", "red"):
            assert (tier, alert) in ESCALATION_ACTIONS


def test_t3_amber_and_red_escalation_language() -> None:
    assert "validator notification" in escalation_action("T3", "amber").lower()
    assert "re-validation" in escalation_action("T3", "red").lower()


def test_monitoring_cadence_by_tier() -> None:
    assert monitoring_cadence("T3") == "weekly"
    assert monitoring_cadence("T2") == "monthly"
    assert monitoring_cadence("T1") == "quarterly"
