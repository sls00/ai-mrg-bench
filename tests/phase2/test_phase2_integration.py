"""Phase2 integration checks: drift monitor, Appendix C, and the full 7-event sequence."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import validate

from workbench.audit import AuditStore, verify_audit_chain

pytestmark = pytest.mark.phase2


def test_phase2_run_validates_schema_and_full_event_sequence(phase2_run: object) -> None:
    run = phase2_run
    assert hasattr(run, "result")
    assert hasattr(run, "db_path")
    result = run.result
    db_path = run.db_path

    drift_report_path = result.artifact_dir / "drift_report.json"
    assert drift_report_path.exists()

    schema = json.loads(Path("schemas/drift_report.schema.json").read_text())
    validate(instance=json.loads(drift_report_path.read_text()), schema=schema)

    verification = verify_audit_chain(db_path)
    assert verification.status == "PASS"
    required = {
        "validation_run.start",
        "bias_battery.result",
        "adverse_action.methodology_published",
        "adverse_action.attribution",
        "drift.event",
        "validation_run.complete",
        "report.generated",
    }
    assert required.issubset(verification.event_type_counts.keys())
    assert verification.event_type_counts["drift.event"] == 1


def test_drift_report_has_at_least_three_feature_metrics_and_amber_or_red(
    phase2_run: object,
) -> None:
    run = phase2_run
    drift_report = json.loads((run.result.artifact_dir / "drift_report.json").read_text())
    assert len(drift_report["feature_drift"]) >= 3

    alerts = {feature["alert_level"] for feature in drift_report["feature_drift"]}
    alerts.add(drift_report["score_drift"]["alert_level"])
    assert alerts & {"amber", "red"}


def test_segment_drift_present_for_sex(phase2_run: object) -> None:
    run = phase2_run
    drift_report = json.loads((run.result.artifact_dir / "drift_report.json").read_text())
    segment = drift_report["segment_drift"]
    assert segment["protected_attribute"] == "sex"
    assert set(segment["by_group"].keys()) == {"male", "female"}
    for metrics in segment["by_group"].values():
        assert metrics["alert_level"] in {"green", "amber", "red"}


def test_drift_event_hash_bound_and_carries_reasoning(phase2_run: object) -> None:
    run = phase2_run
    drift_report_path = run.result.artifact_dir / "drift_report.json"
    expected_sha256 = hashlib.sha256(drift_report_path.read_bytes()).hexdigest()

    events = [e for e in _load_events(run.db_path) if e["event_type"] == "drift.event"]
    assert len(events) == 1
    artifact_refs = json.loads(events[0]["artifact_refs"])
    refs_by_name = {ref["name"]: ref["sha256"] for ref in artifact_refs}
    assert refs_by_name["drift_report.json"] == expected_sha256

    payload = json.loads(events[0]["payload_json"])
    assert "reasoning" in payload
    assert payload["materiality_tier"] == "T3"
    assert payload["alert_level"] in {"green", "amber", "red"}
    assert payload["recommended_action"]


def test_appendix_c_hash_bound_in_report_generated_event(phase2_run: object) -> None:
    run = phase2_run
    drift_report_path = run.result.artifact_dir / "drift_report.json"
    expected_sha256 = hashlib.sha256(drift_report_path.read_bytes()).hexdigest()

    events = [e for e in _load_events(run.db_path) if e["event_type"] == "report.generated"]
    assert len(events) == 1
    artifact_refs = json.loads(events[0]["artifact_refs"])
    refs_by_name = {ref["name"]: ref["sha256"] for ref in artifact_refs}
    assert refs_by_name["drift_report.json"] == expected_sha256

    payload = json.loads(events[0]["payload_json"])
    assert payload["appendices"]["C"] == "present"


def _load_events(db_path: Path) -> list[dict]:
    return AuditStore(db_path).events()
