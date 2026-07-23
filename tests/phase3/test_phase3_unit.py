"""P3 unit tests for state-overlay lookup and config deltas."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from workbench.config import ValidationRunConfig
from workbench.overlay import OVERLAY_PROFILES, resolve_state_overlay

pytestmark = pytest.mark.phase3

_FAKE_LAYERS = {
    "A": {"air": 0.9, "selection_rate_gap": -0.05, "smd_score": -0.1},
    "B": {"fpr_parity_ratio": 1.0, "fnr_parity_ratio": 1.0},
    "C": {
        "auxiliary_classifier_auc": 0.55,
        "top_proxy_correlations": [{"feature": "duration", "abs_correlation": 0.1}],
    },
}


def test_ca_overlay_config_delta_only_state_and_run_id() -> None:
    full = yaml.safe_load(Path("configs/german_credit_full.yaml").read_text())
    ca = yaml.safe_load(Path("configs/german_credit_ca_overlay.yaml").read_text())
    full_run = full["validation_run"]
    ca_run = ca["validation_run"]

    assert ca_run["run_id"] == "german-credit-demo-ca-overlay"
    assert ca_run["regulatory_frame"]["state_overlay"] == "CA"
    assert (
        ca_run["regulatory_frame"]["federal_ecoa"]
        == full_run["regulatory_frame"]["federal_ecoa"]
    )
    assert ca_run["regulatory_frame"]["fha_overlay"] == full_run["regulatory_frame"]["fha_overlay"]

    # Everything except run_id + state_overlay matches the full demo config.
    full_compare = {**full_run, "run_id": ca_run["run_id"]}
    full_compare["regulatory_frame"] = {
        **full_run["regulatory_frame"],
        "state_overlay": "CA",
    }
    assert ca_run == full_compare


def test_co_overlay_config_delta_only_state_and_run_id() -> None:
    full = yaml.safe_load(Path("configs/german_credit_full.yaml").read_text())
    co = yaml.safe_load(Path("configs/german_credit_co_overlay.yaml").read_text())
    full_run = full["validation_run"]
    co_run = co["validation_run"]

    assert co_run["run_id"] == "german-credit-demo-co-overlay"
    assert co_run["regulatory_frame"]["state_overlay"] == "CO"

    full_compare = {**full_run, "run_id": co_run["run_id"]}
    full_compare["regulatory_frame"] = {
        **full_run["regulatory_frame"],
        "state_overlay": "CO",
    }
    assert co_run == full_compare


def test_overlay_configs_load_via_validation_run_config() -> None:
    ca = ValidationRunConfig.from_yaml(Path("configs/german_credit_ca_overlay.yaml"))
    co = ValidationRunConfig.from_yaml(Path("configs/german_credit_co_overlay.yaml"))
    assert ca.regulatory_frame.state_overlay == "CA"
    assert co.regulatory_frame.state_overlay == "CO"
    assert ca.modules.drift_monitor is True
    assert co.modules.adverse_action_translator is True


def test_resolve_none_returns_none() -> None:
    assert (
        resolve_state_overlay(
            state_overlay="none",
            run_id="r",
            bias_layers=_FAKE_LAYERS,
            layer_a_label="outcomes_analysis_risk_assessment_evidence",
            protected_attribute="sex",
        )
        is None
    )


def test_resolve_ca_builds_admt_artifact() -> None:
    result = resolve_state_overlay(
        state_overlay="CA",
        run_id="demo-ca",
        bias_layers=_FAKE_LAYERS,
        layer_a_label="outcomes_analysis_risk_assessment_evidence",
        protected_attribute="sex",
    )
    assert result is not None
    assert result.artifact_name == "admt_risk_assessment_summary.json"
    assert result.state_authority == OVERLAY_PROFILES["CA"]["state_authority"]
    assert result.artifact_payload["artifact_kind"] == "admt_risk_assessment_summary"
    assert "CPPA certification" in result.overlay_non_claims
    assert "disparate-impact compliance" in (
        result.artifact_payload["discrimination_harms_evidence"]["messaging"]
    )


def test_resolve_co_builds_checklist_only() -> None:
    result = resolve_state_overlay(
        state_overlay="CO",
        run_id="demo-co",
        bias_layers=_FAKE_LAYERS,
        layer_a_label="outcomes_analysis_risk_assessment_evidence",
        protected_attribute="sex",
    )
    assert result is not None
    assert result.artifact_name == "co_disclosure_checklist.json"
    assert result.artifact_payload["artifact_kind"] == "co_disclosure_checklist"
    assert result.artifact_payload["disparate_impact_battery"] is False
    assert "admt_risk_assessment" not in result.artifact_payload
    retention = next(
        item for item in result.artifact_payload["checklist"] if item["item"] == "record_retention"
    )
    assert retention["retention_years"] == 3


def test_resolve_unknown_overlay_raises() -> None:
    with pytest.raises(ValueError, match="Unsupported state_overlay"):
        resolve_state_overlay(
            state_overlay="NY",
            run_id="r",
            bias_layers=_FAKE_LAYERS,
            layer_a_label="outcomes_analysis_risk_assessment_evidence",
            protected_attribute="sex",
        )


def test_overlay_profiles_cover_ca_and_co_only() -> None:
    assert set(OVERLAY_PROFILES) == {"CA", "CO"}
