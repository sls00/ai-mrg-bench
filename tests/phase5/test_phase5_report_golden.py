"""Golden-string assertions for P5 (synth-fin CRE) report output.

Covers the two dataset-agnostic report fixes P5 required: the protected
attribute name is no longer hardcoded to `sex` (Sec IV), and the demo
limitations paragraph (Sec II) describes the actual synth-fin CRE panel
instead of the German Credit dataset. German Credit's own goldens
(`tests/phase0/test_phase0_report_golden.py`) assert the *default* text is
unchanged; this file asserts the *override* path.
"""

from __future__ import annotations

import pytest

from workbench.report import DISCLAIMER_TEXT, LIMITATIONS_TEXT

pytestmark = pytest.mark.phase5


def test_report_uses_cre_specific_limitations_not_german_credit_default(
    phase5_run: object,
) -> None:
    run = phase5_run
    report = run.result.report_path.read_text()

    assert DISCLAIMER_TEXT in report
    assert "**Demo limitations:**" in report
    assert "synth-fin synthetic commercial" in report
    assert "not real borrower or property data" in report
    # The shared German-Credit-specific default must NOT leak into this run.
    assert LIMITATIONS_TEXT not in report
    assert "UCI German Credit dataset" not in report


def test_report_names_actual_protected_attribute_not_sex(phase5_run: object) -> None:
    run = phase5_run
    report = run.result.report_path.read_text()

    assert (
        "Protected attribute `minority_tract_top_quintile` is reserved for "
        "validation and excluded from model features."
    ) in report
    assert "Protected attribute `sex` is reserved for validation" not in report


def test_report_adverse_action_translator_disabled_is_documented(
    phase5_run: object,
) -> None:
    run = phase5_run
    report = run.result.report_path.read_text()

    assert (
        "Adverse-action translation methodology: Not run — "
        "adverse_action_translator module disabled."
    ) in report
    assert "Not applicable — adverse_action_translator module disabled." in report
    assert "Not run — drift module disabled" in report
