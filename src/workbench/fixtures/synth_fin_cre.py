"""P5 fixture-derivation helpers for the synth-fin CRE fair-lending demo.

These transforms are applied on top of an *unmodified* synth-fin
`deals.csv` export to produce the three workbench-facing columns the
validation-run configs need. They never mutate the pristine synth-fin
panel: `data/synthetic_cre/deals.csv` + `manifest.json` stay byte-identical
to the `synth-fin generate` output (so the fixture manifest's pinned
`config_hash` remains verifiable) -- the derived columns below are added
only when building the `train.csv` / `validation.csv` splits that
`workbench validate run` actually consumes.

No new bias math: the underlying subgroup shift is entirely synth-fin's
`proxy_discrimination_mild` profile (see `manifest.json` -> `stages` ->
`bias.apply`). This module is glue only.
"""

from __future__ import annotations

import pandas as pd

PROTECTED_ATTRIBUTE_COLUMN = "minority_tract_top_quintile"
TOP_QUINTILE_LABEL = "top_quintile"
REFERENCE_LABEL = "below_top_quintile"
TOP_QUINTILE_QUANTILE = 0.80  # top 20% by minority_tract_pct

DECISION_COLUMN = "credit_decision_favorable"
SOURCE_ADVERSE_COLUMN = "adverse_action_flag"
SOURCE_PROXY_COLUMN = "minority_tract_pct"

# What the demo classifier is trained to predict (1 = elevated credit risk).
# Kept as the training target and split stratifier so the trained model and
# the train/validation row assignment are unchanged by the label fix below.
MODEL_TARGET_COLUMN = "elevated_credit_risk"

# Ground-truth label the bias battery evaluates decisions against
# (1 = creditworthy, i.e. *not* elevated risk). It must share the decision
# column's polarity (1 = favorable): fairlearn's FNR is
# P(decision == 0 | label == 1), so with a 1 = risky label "FNR" would count
# risky loans that were denied -- not an error. Mirrors German Credit's
# `credit_risk` (1 = good).
LABEL_COLUMN = "creditworthy"

# Everything excluded from the demo classifier's feature set: identifiers,
# the label/decision columns themselves, other outcome-adjacent flags
# (`default_flag`, `risk_grade` -- rule-derived from ltv/dscr, which are
# already features), and every geography/income proxy field (`market_msa`,
# `zip_income_quintile`, `minority_tract_pct`) so no protected-class signal
# leaks into the model through a side door. `vintage_year` is dropped too
# for parity with the minimal German Credit feature set.
EXCLUDED_FROM_MODEL_FEATURES: tuple[str, ...] = (
    "property_id",
    "market_msa",
    "vintage_year",
    "risk_grade",
    "default_flag",
    SOURCE_ADVERSE_COLUMN,
    MODEL_TARGET_COLUMN,
    LABEL_COLUMN,
    "zip_income_quintile",
    SOURCE_PROXY_COLUMN,
    PROTECTED_ATTRIBUTE_COLUMN,
    DECISION_COLUMN,
)


def derive_protected_attribute(deals: pd.DataFrame) -> pd.Series:
    """Bin `minority_tract_pct` into a top-quintile geography proxy.

    Geography proxy per factory plan D4 (`minority_tract_pct` / quintile --
    not surname/BISG). Binary framing (top quintile vs. everyone else) is a
    deliberate choice: `workbench.bias_battery._layer_a_outcomes` collapses
    every *non-reference* group to its minimum selection rate before
    computing AIR/selection_rate_gap, so a >2-group categorical would hide
    (not surface) the subgroup shift this demo exists to show. With exactly
    one non-reference group, that collapse is a no-op.
    """
    if SOURCE_PROXY_COLUMN not in deals.columns:
        raise KeyError(f"deals frame is missing '{SOURCE_PROXY_COLUMN}'")
    threshold = deals[SOURCE_PROXY_COLUMN].quantile(TOP_QUINTILE_QUANTILE)
    is_top = deals[SOURCE_PROXY_COLUMN] >= threshold
    return is_top.map({True: TOP_QUINTILE_LABEL, False: REFERENCE_LABEL}).rename(
        PROTECTED_ATTRIBUTE_COLUMN,
    )


def derive_decision_column(deals: pd.DataFrame) -> pd.Series:
    """Invert `adverse_action_flag` into a favorable/approved decision flag.

    `workbench.bias_battery` (selection_rate/AIR "favorable outcome"
    convention) and `workbench.adverse_action`
    (`denied_positions = np.flatnonzero(decisions == 0)`) both expect
    `decision_column` encoded as 1=favorable/approved, 0=denied/adverse --
    mirroring German Credit's `approval_binary`. synth-fin's own
    `adverse_action_flag` is polarity-inverted (1=adverse action taken), so
    this derived column flips it for workbench compatibility. The
    underlying synth-fin field/ground truth is untouched.
    """
    if SOURCE_ADVERSE_COLUMN not in deals.columns:
        raise KeyError(f"deals frame is missing '{SOURCE_ADVERSE_COLUMN}'")
    adverse = deals[SOURCE_ADVERSE_COLUMN].astype(int)
    if not set(adverse.unique()).issubset({0, 1}):
        raise ValueError(f"'{SOURCE_ADVERSE_COLUMN}' must be 0/1")
    return (1 - adverse).rename(DECISION_COLUMN)


def derive_label_column(deals: pd.DataFrame) -> pd.Series:
    """Invert `elevated_credit_risk` into a creditworthy (1 = favorable) label.

    `workbench.bias_battery` Layer B computes FPR/FNR from (label, decision)
    and assumes both use 1 = favorable, as German Credit's `credit_risk` /
    `approval_binary` do. synth-fin's `elevated_credit_risk` is 1 = risky,
    so this flips it the same way `derive_decision_column` flips
    `adverse_action_flag`. FNR then reads as "creditworthy loans denied".
    """
    if MODEL_TARGET_COLUMN not in deals.columns:
        raise KeyError(f"deals frame is missing '{MODEL_TARGET_COLUMN}'")
    risky = deals[MODEL_TARGET_COLUMN].astype(int)
    if not set(risky.unique()).issubset({0, 1}):
        raise ValueError(f"'{MODEL_TARGET_COLUMN}' must be 0/1")
    return (1 - risky).rename(LABEL_COLUMN)


def add_workbench_columns(deals: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of `deals` with the three additive workbench columns attached."""
    out = deals.copy()
    out[PROTECTED_ATTRIBUTE_COLUMN] = derive_protected_attribute(deals)
    out[DECISION_COLUMN] = derive_decision_column(deals)
    out[LABEL_COLUMN] = derive_label_column(deals)
    return out


def model_feature_columns(deals: pd.DataFrame) -> list[str]:
    """Feature columns for the demo classifier.

    Everything in `deals` except identifiers, labels, the decision column,
    and any protected-attribute / geography-proxy field.
    """
    return [column for column in deals.columns if column not in EXCLUDED_FROM_MODEL_FEATURES]
