#!/usr/bin/env python3
"""Bootstrap German Credit fixtures (raw CSV, splits, and trained XGB model)."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier


UCI_COLUMNS = [
    "checking_status",
    "duration",
    "credit_history",
    "purpose",
    "credit_amount",
    "savings_status",
    "employment",
    "installment_commitment",
    "personal_status",
    "other_parties",
    "residence_since",
    "property_magnitude",
    "age",
    "other_payment_plans",
    "housing",
    "existing_credits",
    "job",
    "num_dependents",
    "own_telephone",
    "foreign_worker",
    "class",
]
FEMALE_CODES = {"A92", "A95"}
MALE_CODES = {"A91", "A93", "A94"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-url",
        default="https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data",
        help="UCI source URL.",
    )
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def derive_sex(personal_status: str) -> str:
    if personal_status in FEMALE_CODES:
        return "female"
    if personal_status in MALE_CODES:
        return "male"
    raise ValueError(f"Unknown personal_status code: {personal_status}")


def main() -> None:
    args = parse_args()
    root = Path.cwd()

    raw = pd.read_csv(args.source_url, sep=r"\s+", header=None, names=UCI_COLUMNS)
    raw["sex"] = raw["personal_status"].map(derive_sex)
    raw["credit_risk"] = raw["class"].map({1: 1, 2: 0}).astype(int)
    raw_path = root / "data" / "raw" / "german_credit_uci.csv"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw.to_csv(raw_path, index=False)

    train_df, validation_df = train_test_split(
        raw,
        test_size=0.30,
        random_state=args.seed,
        stratify=raw["credit_risk"],
    )
    train_df = train_df.reset_index(drop=True)
    validation_df = validation_df.reset_index(drop=True)

    excluded_features = {"sex", "personal_status", "class", "credit_risk", "approval_binary"}
    feature_columns = [column for column in raw.columns if column not in excluded_features]
    categorical_columns = [column for column in feature_columns if raw[column].dtype == "object"]
    numeric_columns = [column for column in feature_columns if column not in categorical_columns]
    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_columns),
            ("numeric", "passthrough", numeric_columns),
        ],
    )
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                XGBClassifier(
                    random_state=args.seed,
                    n_estimators=220,
                    max_depth=4,
                    learning_rate=0.05,
                    subsample=0.9,
                    colsample_bytree=0.9,
                    objective="binary:logistic",
                    eval_metric="logloss",
                    n_jobs=1,
                ),
            ),
        ],
    )
    model.fit(train_df[feature_columns], train_df["credit_risk"])
    train_scores = model.predict_proba(train_df[feature_columns])[:, 1]
    validation_scores = model.predict_proba(validation_df[feature_columns])[:, 1]
    train_df["approval_binary"] = (train_scores >= 0.5).astype(int)
    validation_df["approval_binary"] = (validation_scores >= 0.5).astype(int)

    train_path = root / "data" / "german_credit_train.csv"
    validation_path = root / "data" / "german_credit_validation.csv"
    train_df.to_csv(train_path, index=False)
    validation_df.to_csv(validation_path, index=False)

    model_path = root / "models" / "german-credit-xgb-v1.2.joblib"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    print(f"Wrote raw dataset: {raw_path}")
    print(f"Wrote train split: {train_path} ({len(train_df)} rows)")
    print(f"Wrote validation split: {validation_path} ({len(validation_df)} rows)")
    print(f"Wrote model artifact: {model_path}")


if __name__ == "__main__":
    main()
