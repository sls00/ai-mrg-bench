"""Golden-string assertions for P3 report §II regulatory-frames table."""

from __future__ import annotations

import re

import pytest

pytestmark = pytest.mark.phase3

_SECTION_II_RE = re.compile(
    r"## II\. Purpose and Scope\n(?P<body>.*?)(?=\n## III\. Overview of Model Risk)",
    re.DOTALL,
)


def _section_ii(report: str) -> str:
    match = _SECTION_II_RE.search(report)
    assert match is not None, "Section II not found in report"
    return match.group("body")


def test_ca_report_section_ii_has_regulatory_frames_table(phase3_ca_run: object) -> None:
    report = phase3_ca_run.result.report_path.read_text()
    section_ii = _section_ii(report)

    assert "### Regulatory frames active for this validation run" in section_ii
    assert "| Frame | Authority | Role |" in section_ii
    assert "California CCPA/CPRA ADMT" in section_ii
    assert "admt_risk_assessment_summary.json" in section_ii
    assert "Does not constitute CPPA certification" in section_ii
    assert "risk-assessment evidence" in section_ii
    # Never claim a compliance determination in §II overlay framing.
    assert "compliance determination" in section_ii  # appears inside the non-claims line
    assert "is a compliance determination" not in section_ii.lower()
    assert "constitutes CPPA certification" not in section_ii


def test_co_report_section_ii_has_checklist_framing(phase3_co_run: object) -> None:
    report = phase3_co_run.result.report_path.read_text()
    section_ii = _section_ii(report)

    assert "### Regulatory frames active for this validation run" in section_ii
    assert "Colorado SB 26-189" in section_ii
    assert "co_disclosure_checklist.json" in section_ii
    assert "3 years" in section_ii or "Record retention flag: 3 years" in section_ii
    assert "Does not satisfy Colorado Attorney General rules" in section_ii
    assert "admt_risk_assessment_summary.json" not in section_ii


def test_baseline_section_ii_unchanged_byte_for_byte(
    phase3_baseline_run: object,
) -> None:
    """Baseline (state_overlay: none) §II must match the pre-P3 template shape exactly."""
    report = phase3_baseline_run.result.report_path.read_text()
    section_ii = _section_ii(report)

    assert "### Regulatory frames active for this validation run" not in section_ii
    assert "CPPA certification" not in section_ii
    assert "SB 26-189" not in section_ii

    # Canonical baseline bullets — any drift here is a P3 template regression.
    expected_prefix = (
        "\n- Intended use: Credit decisioning support for validation demonstration.\n"
        "- Materiality: **T3** (exposure=0.15, purpose=credit_decisioning)\n"
        "- Regulatory frame:\n"
        "  - federal_ecoa: `proxy_discrimination`\n"
        "  - fha_overlay: `False`\n"
        "  - state_overlay: `none`\n"
        "\n"
    )
    assert section_ii.startswith(expected_prefix)
    assert "Demo limitations:" in section_ii
