"""Materiality tier assignment."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MaterialityResult:
    tier: str
    rationale: str


def assign_materiality_tier(exposure: float, purpose: str) -> MaterialityResult:
    """Assign T1/T2/T3 using the R-06 §5.5 thresholds."""
    if exposure >= 0.10 or purpose == "credit_decisioning":
        return MaterialityResult(
            tier="T3",
            rationale="T3 because exposure >= 0.10 or purpose is credit_decisioning.",
        )
    if exposure >= 0.01:
        return MaterialityResult(
            tier="T2",
            rationale="T2 because exposure >= 0.01 and below T3 threshold.",
        )
    return MaterialityResult(
        tier="T1",
        rationale="T1 because exposure below 0.01 and non-credit_decisioning purpose.",
    )
