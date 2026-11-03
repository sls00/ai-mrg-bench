"""Phase5 (P5 synth-fin CRE) integration checks."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest
import yaml
from jsonschema import validate

from workbench.audit import verify_audit_chain

pytestmark = pytest.mark.phase5


def test_fixture_manifest_matches_files() -> None:
    manifest_path = Path("manifests/synth_fin_cre_fixture_manifest.yaml")
    assert manifest_path.exists(), "P5 fixture manifest must exist after bootstrap."
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


def test_synth_fin_config_hash_pinned_and_matches_committed_manifest() -> None:
    """Panel drift gate: the fixture manifest's pinned config_hash must still
    equal the config_hash actually recorded in the committed synth-fin
    manifest.json. If synth-fin regenerates the panel with different
    parameters, this test (not just the byte-hash check) fails loudly.
    """
    fixture_manifest = yaml.safe_load(
        Path("manifests/synth_fin_cre_fixture_manifest.yaml").read_text(),
    )
    pinned_hash = fixture_manifest.get("synth_fin_config_hash")
    assert pinned_hash, "synth_fin_config_hash must be pinned in the fixture manifest."

    synth_fin_manifest = json.loads(Path("data/synthetic_cre/manifest.json").read_text())
    assert synth_fin_manifest["config_hash"] == pinned_hash


def test_phase5_run_validates_schema_and_chain(phase5_run: object) -> None:
    run = phase5_run
    assert hasattr(run, "result")
    assert hasattr(run, "db_path")
    result = run.result
    db_path = run.db_path

    appendix_b_path = result.artifact_dir / "bias_battery_summary.json"
    schema_path = Path("schemas/bias_battery_summary_synth_fin_cre.schema.json")
    appendix_payload = json.loads(appendix_b_path.read_text())
    schema = json.loads(schema_path.read_text())
    validate(instance=appendix_payload, schema=schema)

    assert appendix_payload["protected_attribute"] == "minority_tract_top_quintile"
    assert appendix_payload["reference_group"] == "below_top_quintile"

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


def test_phase5_run_shows_subgroup_adverse_shift(phase5_run: object) -> None:
    """The whole point of P5: prove the synth-fin bias.apply ground truth
    (proxy_discrimination_mild, top-quartile minority_tract_pct rows) is
    visible in the workbench's own bias battery output for the top-quintile
    geography-proxy subgroup -- not just re-asserted from synth-fin's side.
    """
    run = phase5_run
    result = run.result
    appendix_b_path = result.artifact_dir / "bias_battery_summary.json"
    payload = json.loads(appendix_b_path.read_text())
    layer_a = payload["layers"]["A"]

    by_group = layer_a["selection_rate_by_group"]
    reference_rate = by_group["below_top_quintile"]
    top_quintile_rate = by_group["top_quintile"]

    # decision_column is 1=favorable/approved (see workbench.fixtures.synth_fin_cre
    # .derive_decision_column); the biased top-quintile group must show a
    # materially *lower* favorable-decision rate than the reference group.
    assert top_quintile_rate < reference_rate
    assert reference_rate - top_quintile_rate >= 0.03
    assert layer_a["selection_rate_gap"] < 0
    assert layer_a["air"] < 1.0


def test_phase5_run_protected_attribute_excluded_from_model_features(
    phase5_run: object,
) -> None:
    import joblib

    run = phase5_run
    model = joblib.load(run.config.model_path)
    feature_names = set(model.feature_names_in_)
    assert "minority_tract_top_quintile" not in feature_names
    assert "minority_tract_pct" not in feature_names
    assert "credit_decision_favorable" not in feature_names
    assert "elevated_credit_risk" not in feature_names
    assert "creditworthy" not in feature_names


def test_phase5_label_is_creditworthy_with_favorable_polarity(phase5_run: object) -> None:
    """Layer B is only meaningful if label and decision share 1 = favorable.

    Regression guard for the original P5 wiring, which scored decisions
    (1 = approved) against `elevated_credit_risk` (1 = risky), so "FNR"
    counted risky loans that were denied.
    """
    import pandas as pd

    from workbench.fixtures.synth_fin_cre import LABEL_COLUMN, MODEL_TARGET_COLUMN

    run = phase5_run
    assert run.config.label_column == LABEL_COLUMN == "creditworthy"
    dataset = pd.read_csv(run.config.dataset_path)
    assert (dataset[LABEL_COLUMN] == 1 - dataset[MODEL_TARGET_COLUMN]).all()


def test_phase5_layer_b_surfaces_creditworthy_denial_gap(phase5_run: object) -> None:
    """The planted denial shift must show up as creditworthy loans in the
    top-quintile group being denied materially more often (FNR parity),
    even though Layer A's AIR clears the four-fifths screen.
    """
    run = phase5_run
    payload = json.loads((run.result.artifact_dir / "bias_battery_summary.json").read_text())
    layer_a = payload["layers"]["A"]
    layer_b = payload["layers"]["B"]

    fnr = layer_b["fnr_by_group"]
    assert fnr["top_quintile"] > fnr["below_top_quintile"]
    assert layer_b["fnr_parity_ratio"] >= 2.5
    assert layer_a["air"] >= 0.80
