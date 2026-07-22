"""Golden-string assertions for P2 report output (Sec V.3, Sec VII, Appendix C)."""

from __future__ import annotations

import json

import pytest

pytestmark = pytest.mark.phase2


def test_report_section_v3_and_appendix_c_populated(phase2_run: object) -> None:
    run = phase2_run
    result = run.result
    report = result.report_path.read_text()

    assert "### V.3 Ongoing Model Monitoring" in report
    assert "Score population stability" in report
    assert "Segment-level score PSI by `sex`" in report
    assert "Overall alert level:" in report
    assert "Escalation narrative (R-05 Sec4 tier matrix):" in report
    assert "validator notification within" in report or "Root-cause analysis" in report

    assert "## VII. Vendor and Other Third-Party Products" in report
    assert "Not applicable — in-house model." in report

    assert "### Appendix C" in report
    assert "drift_report.json` generated with score PSI=" in report
    assert "hash-bound in the `drift.event` and `report.generated`" in report

    # P1 appendices still populated alongside the new drift section.
    assert "### Appendix A" in report
    assert "### Appendix B" in report
    assert "### Appendix D" in report
    assert "### Appendix E" in report


def test_report_json_appendix_c_present(phase2_run: object) -> None:
    run = phase2_run
    result = run.result
    report_json = json.loads((result.artifact_dir / "report.json").read_text())
    assert report_json["appendices"]["C"].endswith("drift_report.json")
    assert report_json["appendices"]["A"].endswith("translation_methodology_v1.json")
    assert report_json["appendices"]["B"].endswith("bias_battery_summary.json")
    assert report_json["appendices"]["D"].endswith("fidelity_validation_report.json")
