"""Phase3 integration: CA ADMT + CO checklist artifacts and audit payload enrichment."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import validate

from workbench.audit import AuditStore, verify_audit_chain

pytestmark = pytest.mark.phase3


def test_ca_emits_schema_valid_admt_summary(phase3_ca_run: object) -> None:
    run = phase3_ca_run
    admt_path = run.result.artifact_dir / "admt_risk_assessment_summary.json"
    assert admt_path.exists()
    assert not (run.result.artifact_dir / "co_disclosure_checklist.json").exists()

    schema = json.loads(Path("schemas/admt_risk_assessment.schema.json").read_text())
    payload = json.loads(admt_path.read_text())
    validate(instance=payload, schema=schema)
    assert payload["discrimination_harms_evidence"]["layer_a_label"] == (
        "outcomes_analysis_risk_assessment_evidence"
    )


def test_co_emits_schema_valid_checklist_only(phase3_co_run: object) -> None:
    run = phase3_co_run
    checklist_path = run.result.artifact_dir / "co_disclosure_checklist.json"
    assert checklist_path.exists()
    assert not (run.result.artifact_dir / "admt_risk_assessment_summary.json").exists()

    schema = json.loads(Path("schemas/co_disclosure_checklist.schema.json").read_text())
    payload = json.loads(checklist_path.read_text())
    validate(instance=payload, schema=schema)
    assert payload["disparate_impact_battery"] is False


def test_ca_bias_battery_result_enriched_and_hash_bound(phase3_ca_run: object) -> None:
    run = phase3_ca_run
    admt_path = run.result.artifact_dir / "admt_risk_assessment_summary.json"
    expected_sha = hashlib.sha256(admt_path.read_bytes()).hexdigest()

    events = [
        e for e in _load_events(run.db_path) if e["event_type"] == "bias_battery.result"
    ]
    assert len(events) == 1
    payload = json.loads(events[0]["payload_json"])

    assert payload["layer_a_label"] == "outcomes_analysis_risk_assessment_evidence"
    frame = payload["jurisdiction_frame"]
    assert frame["state_overlay"] == "CA"
    assert "state_authority" in frame
    assert "CCPA" in frame["state_authority"] or "ADMT" in frame["state_authority"]
    assert "DFPI" not in frame["state_authority"]

    artifacts = payload["overlay_artifacts"]
    assert len(artifacts) == 1
    assert artifacts[0]["name"] == "admt_risk_assessment_summary.json"
    assert artifacts[0]["sha256"] == expected_sha


def test_co_bias_battery_result_enriched_and_hash_bound(phase3_co_run: object) -> None:
    run = phase3_co_run
    checklist_path = run.result.artifact_dir / "co_disclosure_checklist.json"
    expected_sha = hashlib.sha256(checklist_path.read_bytes()).hexdigest()

    events = [
        e for e in _load_events(run.db_path) if e["event_type"] == "bias_battery.result"
    ]
    assert len(events) == 1
    payload = json.loads(events[0]["payload_json"])

    assert payload["layer_a_label"] == "outcomes_analysis_risk_assessment_evidence"
    assert payload["jurisdiction_frame"]["state_overlay"] == "CO"
    assert "SB 26-189" in payload["jurisdiction_frame"]["state_authority"]
    artifacts = payload["overlay_artifacts"]
    assert artifacts[0]["name"] == "co_disclosure_checklist.json"
    assert artifacts[0]["sha256"] == expected_sha


def test_ca_audit_chain_still_passes(phase3_ca_run: object) -> None:
    verification = verify_audit_chain(phase3_ca_run.db_path)
    assert verification.status == "PASS"
    assert "bias_battery.result" in verification.event_type_counts


def test_baseline_bias_battery_payload_has_no_overlay_fields(
    phase3_baseline_run: object,
) -> None:
    run = phase3_baseline_run
    events = [
        e for e in _load_events(run.db_path) if e["event_type"] == "bias_battery.result"
    ]
    payload = json.loads(events[0]["payload_json"])
    assert payload["jurisdiction_frame"]["state_overlay"] == "none"
    assert "state_authority" not in payload["jurisdiction_frame"]
    assert "overlay_artifacts" not in payload
    assert payload["layer_a_label"] == "outcomes_analysis_risk_assessment_evidence"


def _load_events(db_path: Path) -> list[dict]:
    return AuditStore(db_path).events()
