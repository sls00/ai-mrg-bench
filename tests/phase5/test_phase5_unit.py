"""Unit tests for the P5 synth-fin CRE fixture-derivation helpers."""

from __future__ import annotations

import pandas as pd
import pytest

from workbench.fixtures.synth_fin_cre import (
    DECISION_COLUMN,
    EXCLUDED_FROM_MODEL_FEATURES,
    PROTECTED_ATTRIBUTE_COLUMN,
    REFERENCE_LABEL,
    TOP_QUINTILE_LABEL,
    add_workbench_columns,
    derive_decision_column,
    derive_protected_attribute,
    model_feature_columns,
)

pytestmark = pytest.mark.phase5


def _toy_deals() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "property_id": [f"p{i}" for i in range(10)],
            "minority_tract_pct": [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.60, 0.80, 0.95],
            "adverse_action_flag": [0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
            "elevated_credit_risk": [0, 0, 0, 1, 0, 0, 1, 0, 1, 1],
            "market_msa": ["m"] * 10,
            "loan_amount": list(range(10)),
        },
    )


def test_derive_protected_attribute_splits_top_quintile() -> None:
    deals = _toy_deals()
    protected = derive_protected_attribute(deals)
    assert protected.name == PROTECTED_ATTRIBUTE_COLUMN
    # 10 rows -> top quintile = top 2 rows by minority_tract_pct (0.80, 0.95).
    assert (protected == TOP_QUINTILE_LABEL).sum() == 2
    assert protected.iloc[-1] == TOP_QUINTILE_LABEL
    assert protected.iloc[-2] == TOP_QUINTILE_LABEL
    assert protected.iloc[0] == REFERENCE_LABEL


def test_derive_protected_attribute_missing_column_raises() -> None:
    with pytest.raises(KeyError):
        derive_protected_attribute(pd.DataFrame({"other": [1, 2, 3]}))


def test_derive_decision_column_inverts_adverse_flag() -> None:
    deals = _toy_deals()
    decision = derive_decision_column(deals)
    assert decision.name == DECISION_COLUMN
    assert list(decision) == [1, 1, 1, 1, 1, 1, 1, 1, 0, 0]


def test_derive_decision_column_rejects_non_binary() -> None:
    deals = _toy_deals()
    deals["adverse_action_flag"] = [2] * len(deals)
    with pytest.raises(ValueError, match="must be 0/1"):
        derive_decision_column(deals)


def test_add_workbench_columns_does_not_mutate_input() -> None:
    deals = _toy_deals()
    original_columns = set(deals.columns)
    enriched = add_workbench_columns(deals)
    assert set(deals.columns) == original_columns, "input frame must not be mutated"
    assert PROTECTED_ATTRIBUTE_COLUMN in enriched.columns
    assert DECISION_COLUMN in enriched.columns
    assert len(enriched) == len(deals)


def test_model_feature_columns_excludes_protected_and_outcome_fields() -> None:
    deals = _toy_deals()
    enriched = add_workbench_columns(deals)
    features = model_feature_columns(enriched)
    for excluded in EXCLUDED_FROM_MODEL_FEATURES:
        assert excluded not in features
    assert "loan_amount" in features
