"""P0 three-layer bias battery for German Credit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from fairlearn.metrics import (
    MetricFrame,
    false_negative_rate,
    false_positive_rate,
    selection_rate,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

from workbench.config import RegulatoryFrameConfig


@dataclass(slots=True)
class BiasBatteryResult:
    payload: dict[str, Any]
    appendix_payload: dict[str, Any]


def run_bias_battery(
    *,
    dataset: pd.DataFrame,
    model: Any,
    model_features: list[str],
    protected_attribute: str,
    reference_group: str,
    decision_column: str,
    label_column: str,
    run_id: str,
    regulatory_frame: RegulatoryFrameConfig,
) -> BiasBatteryResult:
    labels = dataset[label_column].astype(int)
    decisions = dataset[decision_column].astype(int)
    protected = dataset[protected_attribute].astype(str)

    features = dataset[model_features]
    scores = _predict_scores(model, features)

    layer_a = _layer_a_outcomes(
        labels=labels,
        decisions=decisions,
        scores=scores,
        protected=protected,
        reference_group=reference_group,
    )
    layer_b = _layer_b_error_parity(
        labels=labels,
        decisions=decisions,
        protected=protected,
        reference_group=reference_group,
    )
    layer_c = _layer_c_proxy_risk(
        features=features,
        protected=protected,
    )

    jurisdiction_frame = {
        "federal_ecoa": regulatory_frame.federal_ecoa,
        "fha_overlay": regulatory_frame.fha_overlay,
        "state_overlay": regulatory_frame.state_overlay,
    }
    reasoning = {
        "why_layer_a": (
            "Layer A captures AIR, selection-rate gap, and score-distribution imbalance."
        ),
        "why_layer_b": (
            "Layer B checks whether model errors disproportionately burden protected groups."
        ),
        "why_layer_c": (
            "Layer C estimates proxy discrimination risk via feature association "
            "and predictability."
        ),
        "regulatory_note": (
            "Federal ECOA frame is proxy_discrimination; outcomes metrics support risk review."
        ),
    }

    summary = {
        "run_id": run_id,
        "protected_attribute": protected_attribute,
        "reference_group": reference_group,
        "jurisdiction_frame": jurisdiction_frame,
        "layers": {"A": layer_a, "B": layer_b, "C": layer_c},
        "reasoning": reasoning,
        "aequitas_pin": _aequitas_version(),
    }

    payload = {
        "protected_attribute": protected_attribute,
        "jurisdiction_frame": jurisdiction_frame,
        "layer_a_label": "outcomes_analysis_risk_assessment_evidence",
        "layers": {"A": layer_a, "B": layer_b, "C": layer_c},
        "reasoning": reasoning,
    }

    return BiasBatteryResult(payload=payload, appendix_payload=summary)


def _layer_a_outcomes(
    *,
    labels: pd.Series,
    decisions: pd.Series,
    scores: np.ndarray,
    protected: pd.Series,
    reference_group: str,
) -> dict[str, Any]:
    metric_frame = MetricFrame(
        metrics={"selection_rate": selection_rate},
        y_true=labels,
        y_pred=decisions,
        sensitive_features=protected,
    )
    by_group = metric_frame.by_group["selection_rate"].to_dict()
    reference_rate = float(by_group[reference_group])
    comparison_rates = [
        float(rate) for group, rate in by_group.items() if group != reference_group
    ]
    min_group_rate = min(comparison_rates) if comparison_rates else reference_rate
    air = _safe_div(min_group_rate, reference_rate)

    non_reference_scores = scores[protected != reference_group]
    reference_scores = scores[protected == reference_group]
    non_reference_mean = float(np.mean(non_reference_scores))
    reference_mean = float(np.mean(reference_scores))
    pooled_std = float(
        np.sqrt(
            (np.var(non_reference_scores, ddof=1) + np.var(reference_scores, ddof=1)) / 2,
        ),
    )
    smd = _safe_div(non_reference_mean - reference_mean, pooled_std)

    non_reference_rate = min_group_rate if comparison_rates else reference_rate
    return {
        "air": air,
        "selection_rate_gap": non_reference_rate - reference_rate,
        "selection_rate_by_group": {key: float(value) for key, value in by_group.items()},
        "smd_score": smd,
    }


def _layer_b_error_parity(
    *,
    labels: pd.Series,
    decisions: pd.Series,
    protected: pd.Series,
    reference_group: str,
) -> dict[str, Any]:
    metric_frame = MetricFrame(
        metrics={"fpr": false_positive_rate, "fnr": false_negative_rate},
        y_true=labels,
        y_pred=decisions,
        sensitive_features=protected,
    )
    fpr_by_group = metric_frame.by_group["fpr"].to_dict()
    fnr_by_group = metric_frame.by_group["fnr"].to_dict()
    reference_fpr = float(fpr_by_group[reference_group])
    reference_fnr = float(fnr_by_group[reference_group])
    comparison_fprs = [
        float(value) for group, value in fpr_by_group.items() if group != reference_group
    ]
    comparison_fnrs = [
        float(value) for group, value in fnr_by_group.items() if group != reference_group
    ]
    compared_fpr = comparison_fprs[0] if comparison_fprs else reference_fpr
    compared_fnr = comparison_fnrs[0] if comparison_fnrs else reference_fnr
    return {
        "fpr_parity_ratio": _safe_div(compared_fpr, reference_fpr),
        "fnr_parity_ratio": _safe_div(compared_fnr, reference_fnr),
        "fpr_gap": compared_fpr - reference_fpr,
        "fnr_gap": compared_fnr - reference_fnr,
        "fpr_by_group": {key: float(value) for key, value in fpr_by_group.items()},
        "fnr_by_group": {key: float(value) for key, value in fnr_by_group.items()},
    }


def _layer_c_proxy_risk(*, features: pd.DataFrame, protected: pd.Series) -> dict[str, Any]:
    protected_binary = (protected == sorted(protected.unique())[0]).astype(int)
    correlations: list[tuple[str, float]] = []

    for column in features.columns:
        series = features[column]
        if series.dtype == object or str(series.dtype).startswith("category"):
            numeric = pd.factorize(series)[0].astype(float)
        else:
            numeric = pd.to_numeric(series, errors="coerce").fillna(0.0).to_numpy()
        if np.std(numeric) == 0:
            correlation = 0.0
        else:
            correlation = float(np.corrcoef(numeric, protected_binary)[0, 1])
            if np.isnan(correlation):
                correlation = 0.0
        correlations.append((column, abs(correlation)))

    top_correlations = sorted(correlations, key=lambda item: item[1], reverse=True)[:5]
    proxy_df = pd.get_dummies(features, drop_first=False)
    x_train, x_test, y_train, y_test = train_test_split(
        proxy_df,
        protected_binary,
        test_size=0.30,
        random_state=42,
        stratify=protected_binary,
    )
    classifier = LogisticRegression(max_iter=2000, solver="liblinear", random_state=42)
    classifier.fit(x_train, y_train)
    auc = float(roc_auc_score(y_test, classifier.predict_proba(x_test)[:, 1]))
    return {
        "top_proxy_correlations": [
            {"feature": feature, "abs_correlation": value} for feature, value in top_correlations
        ],
        "auxiliary_classifier_auc": auc,
    }


def _predict_scores(model: Any, features: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        predicted = model.predict_proba(features)
        return np.asarray(predicted)[:, 1]
    return np.asarray(model.predict(features), dtype=float)


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def _aequitas_version() -> str:
    try:
        import aequitas
    except Exception as exc:  # pragma: no cover - defensive only
        return f"unavailable:{exc.__class__.__name__}"
    return str(getattr(aequitas, "__version__", "unknown"))
