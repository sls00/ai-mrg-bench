"""P2 drift monitor: PSI/KS population + score drift, segment PSI, tier escalation.

Implements the R-05 Sec3-4 tier-gated drift engine: Lewis-bin Population Stability
Index as the primary population/score-drift test, Kolmogorov-Smirnov as the
secondary distributional corroborator, and a materiality-tier x alert-level lookup
that mirrors the R-05 Sec4.2 traffic-light escalation matrix. Drift on the German
Credit monitor split is injected covariate shift (scripts/inject_monitor_shift.py),
not observed production drift -- see R-10 Sec4.5.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

PSI_AMBER_THRESHOLD = 0.10
PSI_RED_THRESHOLD = 0.25
KS_PVALUE_AMBER_THRESHOLD = 0.05
KS_PVALUE_RED_THRESHOLD = 0.01
DEFAULT_N_BINS = 10
PSI_PROPORTION_FLOOR = 1e-4

# R-10 Sec4.5: the three features specifically shifted on the monitor split.
DRIFT_FEATURES = ["duration", "credit_amount", "installment_commitment"]

_ALERT_RANK = {"green": 0, "amber": 1, "red": 2}

MONITORING_CADENCE_BY_TIER = {"T1": "quarterly", "T2": "monthly", "T3": "weekly"}

# R-05 Sec4.2 escalation matrix (traffic-light policy), keyed by (materiality_tier, alert_level).
ESCALATION_ACTIONS = {
    ("T1", "green"): "Log only; continue quarterly monitoring.",
    ("T1", "amber"): "Log and flag for annual review.",
    ("T1", "red"): "Escalate to T2 review within 60 days.",
    ("T2", "green"): "Log only; continue monthly monitoring.",
    ("T2", "amber"): "Analyst review within 30 days; root-cause memo required.",
    ("T2", "red"): "Validator re-validation scoping within 30 days.",
    ("T3", "green"): "Log and dashboard; continue weekly monitoring.",
    ("T3", "amber"): (
        "Validator notification within 10 days; increased monitoring frequency."
    ),
    ("T3", "red"): (
        "Full re-validation trigger; model use restriction pending review; "
        "MRM committee convened within 15 days."
    ),
}

VALIDATOR_NOTIFICATION_DAYS = {
    ("T3", "amber"): 10,
    ("T3", "red"): 15,
}


@dataclass(slots=True)
class DriftResult:
    payload: dict[str, Any]
    appendix_payload: dict[str, Any]
    section_context: dict[str, Any]


def population_stability_index(
    reference: np.ndarray,
    current: np.ndarray,
    n_bins: int = DEFAULT_N_BINS,
) -> float:
    """Lewis (1994) decile-bin PSI: sum((actual% - expected%) * ln(actual%/expected%)).

    Bin edges are the reference (development) population's quantiles -- the
    industry-standard "expected" population for PSI. Proportions are floored to
    avoid log(0)/division-by-zero on empty bins (R-05 Sec3.1 caveat: thresholds
    do not adjust for sample size).
    """
    reference_arr = np.asarray(reference, dtype=float)
    current_arr = np.asarray(current, dtype=float)
    edges = _bin_edges(reference_arr, n_bins)
    expected = _bin_proportions(reference_arr, edges)
    actual = _bin_proportions(current_arr, edges)
    return float(np.sum((actual - expected) * np.log(actual / expected)))


def psi_alert_level(psi: float) -> str:
    """R-05 Sec3.1 Lewis bands: <0.10 stable, 0.10-0.25 amber, >=0.25 red."""
    if psi >= PSI_RED_THRESHOLD:
        return "red"
    if psi >= PSI_AMBER_THRESHOLD:
        return "amber"
    return "green"


def ks_alert_level(pvalue: float) -> str:
    """R-05 Sec3.2 default thresholds: amber p<0.05, red p<0.01."""
    if pvalue < KS_PVALUE_RED_THRESHOLD:
        return "red"
    if pvalue < KS_PVALUE_AMBER_THRESHOLD:
        return "amber"
    return "green"


def combine_alert_levels(*levels: str) -> str:
    """Overall alert is the most severe of the contributing PSI/KS signals."""
    return max(levels, key=_ALERT_RANK.__getitem__)


def monitoring_cadence(materiality_tier: str) -> str:
    return MONITORING_CADENCE_BY_TIER[materiality_tier]


def escalation_action(materiality_tier: str, alert_level: str) -> str:
    return ESCALATION_ACTIONS[(materiality_tier, alert_level)]


def run_drift_monitor(
    *,
    reference_dataset: pd.DataFrame,
    monitor_dataset: pd.DataFrame,
    model: Any,
    model_features: list[str],
    protected_attribute: str,
    reference_group: str,
    run_id: str,
    materiality_tier: str,
    reference_path: str,
    monitor_path: str,
) -> DriftResult:
    reference_scores = _predict_scores(model, reference_dataset[model_features])
    monitor_scores = _predict_scores(model, monitor_dataset[model_features])

    score_psi = population_stability_index(reference_scores, monitor_scores)
    score_ks = ks_2samp(reference_scores, monitor_scores)
    score_alert = combine_alert_levels(
        psi_alert_level(score_psi),
        ks_alert_level(float(score_ks.pvalue)),
    )
    score_drift = {
        "psi": score_psi,
        "ks_statistic": float(score_ks.statistic),
        "ks_pvalue": float(score_ks.pvalue),
        "alert_level": score_alert,
    }

    feature_drift = [
        _feature_drift_metrics(reference_dataset, monitor_dataset, feature)
        for feature in DRIFT_FEATURES
        if feature in reference_dataset.columns and feature in monitor_dataset.columns
    ]
    if len(feature_drift) < 3:
        raise ValueError(
            "drift_monitor requires >=3 feature CSIs; DRIFT_FEATURES "
            f"{DRIFT_FEATURES} not fully present in reference/monitor datasets.",
        )

    segment_drift = _segment_score_psi(
        reference_dataset=reference_dataset,
        monitor_dataset=monitor_dataset,
        reference_scores=reference_scores,
        monitor_scores=monitor_scores,
        protected_attribute=protected_attribute,
        reference_group=reference_group,
    )

    overall_alert = combine_alert_levels(
        score_alert,
        *(feature["alert_level"] for feature in feature_drift),
    )
    recommended_action = escalation_action(materiality_tier, overall_alert)
    cadence = monitoring_cadence(materiality_tier)
    validator_notification_days = VALIDATOR_NOTIFICATION_DAYS.get(
        (materiality_tier, overall_alert),
    )

    reasoning = {
        "summary": (
            f"Score PSI={score_psi:.4f} ({score_alert}); overall alert level "
            f"{overall_alert} at materiality tier {materiality_tier} escalates per "
            f"the R-05 Sec4 tier matrix: {recommended_action}"
        ),
        "methodology_note": (
            "PSI uses Lewis (1994) decile bins on the reference (development) "
            "population; the 0.10/0.25 thresholds are documented industry "
            "heuristics, not statistically derived, and do not adjust for sample "
            "size (R-05 Sec3.1)."
        ),
        "drift_basis": (
            "Population drift on the monitor split is injected covariate shift "
            "(scripts/inject_monitor_shift.py: duration x1.35 + N(0,2) noise, "
            "credit_amount +2000 EUR on 40% of rows, installment_commitment "
            "resampled from the reference population with a +15% mean shift), "
            "not observed production drift -- German Credit has no application "
            "dates for a temporal split (R-10 Sec4.5)."
        ),
    }

    payload = {
        "run_id": run_id,
        "alert_level": overall_alert,
        "materiality_tier": materiality_tier,
        "recommended_action": recommended_action,
        "score_drift": score_drift,
        "feature_drift": feature_drift,
        "segment_drift": segment_drift,
        "reasoning": reasoning,
    }

    appendix_payload = {
        "run_id": run_id,
        "reference_dataset": {"path": reference_path, "rows": int(len(reference_dataset))},
        "monitor_dataset": {"path": monitor_path, "rows": int(len(monitor_dataset))},
        "score_drift": score_drift,
        "feature_drift": feature_drift,
        "segment_drift": segment_drift,
        "materiality_tier": materiality_tier,
        "overall_alert_level": overall_alert,
        "recommended_action": recommended_action,
        "escalation": {
            "cadence": cadence,
            "validator_notification_days": validator_notification_days,
            "tier_policy_note": (
                "R-05 Sec4.2 escalation matrix: T3 Amber requires validator "
                "notification within 10 days and increased monitoring frequency; "
                "T3 Red triggers a full re-validation and MRM committee review "
                "within 15 days."
            ),
        },
        "injected_shift_note": reasoning["drift_basis"],
        "reasoning": reasoning,
    }

    section_context = {
        "score_psi": score_psi,
        "score_alert_level": score_alert,
        "score_ks_statistic": score_drift["ks_statistic"],
        "score_ks_pvalue": score_drift["ks_pvalue"],
        "feature_drift": feature_drift,
        "segment_drift": segment_drift,
        "overall_alert_level": overall_alert,
        "materiality_tier": materiality_tier,
        "recommended_action": recommended_action,
        "cadence": cadence,
        "validator_notification_days": validator_notification_days,
        "reasoning": reasoning,
    }

    return DriftResult(
        payload=payload,
        appendix_payload=appendix_payload,
        section_context=section_context,
    )


def _feature_drift_metrics(
    reference_dataset: pd.DataFrame,
    monitor_dataset: pd.DataFrame,
    feature: str,
) -> dict[str, Any]:
    reference_values = (
        pd.to_numeric(reference_dataset[feature], errors="coerce").dropna().to_numpy()
    )
    monitor_values = pd.to_numeric(monitor_dataset[feature], errors="coerce").dropna().to_numpy()
    psi = population_stability_index(reference_values, monitor_values)
    ks_result = ks_2samp(reference_values, monitor_values)
    alert = combine_alert_levels(
        psi_alert_level(psi),
        ks_alert_level(float(ks_result.pvalue)),
    )
    return {
        "feature": feature,
        "psi": psi,
        "ks_statistic": float(ks_result.statistic),
        "ks_pvalue": float(ks_result.pvalue),
        "alert_level": alert,
    }


def _segment_score_psi(
    *,
    reference_dataset: pd.DataFrame,
    monitor_dataset: pd.DataFrame,
    reference_scores: np.ndarray,
    monitor_scores: np.ndarray,
    protected_attribute: str,
    reference_group: str,
) -> dict[str, Any]:
    reference_groups = reference_dataset[protected_attribute].astype(str).to_numpy()
    monitor_groups = monitor_dataset[protected_attribute].astype(str).to_numpy()
    groups = sorted(set(reference_groups) | set(monitor_groups))

    by_group: dict[str, Any] = {}
    for group in groups:
        reference_segment = reference_scores[reference_groups == group]
        monitor_segment = monitor_scores[monitor_groups == group]
        if reference_segment.size == 0 or monitor_segment.size == 0:
            continue
        psi = population_stability_index(reference_segment, monitor_segment)
        by_group[group] = {
            "psi": psi,
            "alert_level": psi_alert_level(psi),
            "n_reference": int(reference_segment.size),
            "n_monitor": int(monitor_segment.size),
        }

    return {
        "protected_attribute": protected_attribute,
        "reference_group": reference_group,
        "by_group": by_group,
    }


def _bin_edges(reference: np.ndarray, n_bins: int) -> np.ndarray:
    quantiles = np.linspace(0.0, 1.0, n_bins + 1)
    edges = np.unique(np.quantile(reference, quantiles)).astype(float)
    if edges.size < 2:
        edges = np.array([reference.min(), reference.max()], dtype=float)
    edges[0] = -np.inf
    edges[-1] = np.inf
    return edges


def _bin_proportions(values: np.ndarray, edges: np.ndarray) -> np.ndarray:
    counts, _ = np.histogram(values, bins=edges)
    total = max(int(counts.sum()), 1)
    proportions = counts / total
    return np.clip(proportions, PSI_PROPORTION_FLOOR, None)


def _predict_scores(model: Any, features: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return np.asarray(model.predict_proba(features))[:, 1]
    return np.asarray(model.predict(features), dtype=float)
