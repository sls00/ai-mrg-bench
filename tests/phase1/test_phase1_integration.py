"""Phase1 integration checks: adverse-action translator + methodology hash-binding."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import validate

from workbench.audit import verify_audit_chain

pytestmark = pytest.mark.phase1


def test_phase1_run_validates_schema_and_chain(phase1_run: object) -> None:
    run = phase1_run
    assert hasattr(run, "result")
    assert hasattr(run, "db_path")
    result = run.result
    db_path = run.db_path

    methodology_path = result.artifact_dir / "translation_methodology_v1.json"
    methodology_md_path = result.artifact_dir / "translation_methodology_v1.md"
    fidelity_path = result.artifact_dir / "fidelity_validation_report.json"
    assert methodology_path.exists()
    assert methodology_md_path.exists()
    assert fidelity_path.exists()

    methodology_schema = json.loads(
        Path("schemas/translation_methodology_v1.schema.json").read_text(),
    )
    fidelity_schema = json.loads(Path("schemas/fidelity_validation.schema.json").read_text())
    validate(instance=json.loads(methodology_path.read_text()), schema=methodology_schema)
    validate(instance=json.loads(fidelity_path.read_text()), schema=fidelity_schema)

    verification = verify_audit_chain(db_path)
    assert verification.status == "PASS"
    required = {
        "validation_run.start",
        "bias_battery.result",
        "adverse_action.methodology_published",
        "adverse_action.attribution",
        "validation_run.complete",
        "report.generated",
    }
    assert required.issubset(verification.event_type_counts.keys())
    assert verification.event_type_counts["adverse_action.methodology_published"] == 1
    assert verification.event_type_counts["adverse_action.attribution"] >= 1


def test_methodology_hash_bound_in_audit_event(phase1_run: object) -> None:
    run = phase1_run
    result = run.result
    methodology_path = result.artifact_dir / "translation_methodology_v1.json"
    methodology_md_path = result.artifact_dir / "translation_methodology_v1.md"

    import hashlib

    expected_json_sha256 = hashlib.sha256(methodology_path.read_bytes()).hexdigest()
    expected_md_sha256 = hashlib.sha256(methodology_md_path.read_bytes()).hexdigest()

    events = [
        event
        for event in _load_events(run.db_path)
        if event["event_type"] == "adverse_action.methodology_published"
    ]
    assert len(events) == 1
    artifact_refs = json.loads(events[0]["artifact_refs"])
    refs_by_name = {ref["name"]: ref["sha256"] for ref in artifact_refs}
    assert refs_by_name["translation_methodology_v1.json"] == expected_json_sha256
    assert refs_by_name["translation_methodology_v1.md"] == expected_md_sha256

    payload = json.loads(events[0]["payload_json"])
    assert "reasoning" in payload


def test_attribution_events_carry_reasoning_and_principal_reasons(phase1_run: object) -> None:
    run = phase1_run
    events = [
        event
        for event in _load_events(run.db_path)
        if event["event_type"] == "adverse_action.attribution"
    ]
    assert len(events) >= 1
    for event in events:
        payload = json.loads(event["payload_json"])
        assert "reasoning" in payload
        assert payload["decision"] == "adverse"
        assert 1 <= len(payload["principal_reasons"]) <= 4
        for reason in payload["principal_reasons"]:
            assert reason["description"]
            assert reason["feature"]


def test_appendix_a_and_d_hash_bound_in_report_generated_event(phase1_run: object) -> None:
    run = phase1_run
    result = run.result
    methodology_path = result.artifact_dir / "translation_methodology_v1.json"
    fidelity_path = result.artifact_dir / "fidelity_validation_report.json"

    import hashlib

    expected_methodology_sha256 = hashlib.sha256(methodology_path.read_bytes()).hexdigest()
    expected_fidelity_sha256 = hashlib.sha256(fidelity_path.read_bytes()).hexdigest()

    events = [
        event for event in _load_events(run.db_path) if event["event_type"] == "report.generated"
    ]
    assert len(events) == 1
    artifact_refs = json.loads(events[0]["artifact_refs"])
    refs_by_name = {ref["name"]: ref["sha256"] for ref in artifact_refs}
    assert refs_by_name["translation_methodology_v1.json"] == expected_methodology_sha256
    assert refs_by_name["fidelity_validation_report.json"] == expected_fidelity_sha256

    payload = json.loads(events[0]["payload_json"])
    assert payload["appendices"]["A"] == "present"
    assert payload["appendices"]["D"] == "present"


def _load_events(db_path: Path) -> list[dict]:
    from workbench.audit import AuditStore

    return AuditStore(db_path).events()
