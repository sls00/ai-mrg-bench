"""Golden-string assertions for P0 report output."""

from __future__ import annotations

import pytest

from workbench.report import DISCLAIMER_TEXT, LIMITATIONS_TEXT

pytestmark = pytest.mark.phase0


def test_report_contains_required_sections_and_strings(phase0_run: object) -> None:
    run = phase0_run
    assert hasattr(run, "result")
    result = run.result
    report = result.report_path.read_text()
    assert "## I. Introduction" in report
    assert "## II. Purpose and Scope" in report
    assert "## III. Overview of Model Risk and MRM" in report
    assert "## IV. Model Development and Model Use" in report
    assert "## V. Model Validation and Monitoring" in report
    assert "## VI. Governance and Controls" in report

    assert DISCLAIMER_TEXT in report
    assert LIMITATIONS_TEXT in report
    assert "Not run — drift module disabled" in report
