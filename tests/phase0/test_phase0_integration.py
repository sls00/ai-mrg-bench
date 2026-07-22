"""Phase0 integration checks."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest
import yaml
from jsonschema import validate

from workbench.audit import verify_audit_chain

pytestmark = pytest.mark.phase0


def test_fixture_manifest_matches_files() -> None:
    manifest_path = Path("manifests/german_credit_fixture_manifest.yaml")
    assert manifest_path.exists(), "Fixture manifest must exist after bootstrap."
    payload = yaml.safe_load(manifest_path.read_text())
    files = payload.get("files", [])
    assert files, "Manifest should contain fixture entries."

    for entry in files:
        file_path = Path(entry["path"])
        assert file_path.exists(), f"Missing fixture file: {file_path}"
        actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
        assert actual == str(entry["sha256"])

    proc = subprocess.run(
        ["bash", "scripts/check_fixture_hashes.sh"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PASS" in proc.stdout
    assert "SKIP" not in proc.stdout


def test_phase0_run_validates_schema_and_chain(phase0_run: object) -> None:
    run = phase0_run
    assert hasattr(run, "result")
    assert hasattr(run, "db_path")
    result = run.result
    db_path = run.db_path

    appendix_b_path = result.artifact_dir / "bias_battery_summary.json"
    schema_path = Path("schemas/bias_battery_summary.schema.json")
    appendix_payload = json.loads(appendix_b_path.read_text())
    schema = json.loads(schema_path.read_text())
    validate(instance=appendix_payload, schema=schema)

    verification = verify_audit_chain(db_path)
    assert verification.status == "PASS"
    required = {
        "validation_run.start",
        "bias_battery.result",
        "validation_run.complete",
        "report.generated",
    }
    assert required.issubset(verification.event_type_counts.keys())
    assert verification.total_events >= 4
