"""Golden-string assertions for P1 report output (Sec V.1 + Appendices A/D)."""

from __future__ import annotations

import json

import pytest

pytestmark = pytest.mark.phase1


def test_report_section_v1_and_appendices_a_d_populated(phase1_run: object) -> None:
    run = phase1_run
    result = run.result
    report = result.report_path.read_text()

    assert "## V. Model Validation and Monitoring" in report
    assert "### V.1 Conceptual Soundness" in report
    assert "Adverse-action translation methodology overview:" in report
    assert "Fidelity validation (`fidelity_report_v1`) overall status: **PASS**" in report

    assert "### Appendix A" in report
    assert (
        "`translation_methodology_v1.json` / `.md` generated and hash-bound "
        "in the `adverse_action.methodology_published` audit event."
    ) in report

    assert "### Appendix D" in report
    assert "`fidelity_validation_report.json` generated; overall status **PASS**" in report

    # P0 drift text untouched — P1 does not enable drift_monitor.
    assert "Not run — drift module disabled" in report


def test_report_json_appendices_present(phase1_run: object) -> None:
    run = phase1_run
    result = run.result
    report_json = json.loads((result.artifact_dir / "report.json").read_text())
    assert report_json["appendices"]["A"].endswith("translation_methodology_v1.json")
    assert report_json["appendices"]["D"].endswith("fidelity_validation_report.json")
    assert report_json["appendices"]["B"].endswith("bias_battery_summary.json")
    assert report_json["appendices"]["C"] == "Not run — drift module disabled"
