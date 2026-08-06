#!/usr/bin/env python3
"""Bootstrap P5 synth-fin CRE fixtures (panel copy, splits, trained model).

Source panel comes from an external `synth-fin generate` run (this repo does
not vendor or reimplement synth-fin's generator). Regeneration command
(documented in both READMEs):

    cd ../synth-fin
    uv sync
    uv run synth-fin generate \\
      --scenario base \\
      --bias-profile proxy_discrimination_mild \\
      --n 5000 \\
      --seed 42 \\
      --out /tmp/sf-p5-panel

Then, from this repo:

    uv run python scripts/bootstrap_synth_fin_cre_fixtures.py \\
      --source /tmp/sf-p5-panel

`data/synthetic_cre/deals.csv` and `manifest.json` are byte-identical copies
of the synth-fin output (config_hash/checksum provenance preserved).
`train.csv`/`validation.csv` are workbench-side derivatives with the two
additive columns from `workbench.fixtures.synth_fin_cre` attached.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from xgboost import XGBClassifier

from workbench.fixtures.synth_fin_cre import (
    LABEL_COLUMN,
    add_workbench_columns,
    model_feature_columns,
)

SEED = 42
TEST_SIZE = 0.30
MODEL_PATH = Path("models/synth-fin-cre-xgb-v1.0.joblib")
DATA_DIR = Path("data/synthetic_cre")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Directory containing synth-fin's deals.csv + manifest.json output.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path.cwd()
    source_deals = args.source / "deals.csv"
    source_manifest = args.source / "manifest.json"
    if not source_deals.exists() or not source_manifest.exists():
        raise FileNotFoundError(
            f"Expected deals.csv + manifest.json under {args.source}; "
            "run `synth-fin generate` first (see module docstring).",
        )

    data_dir = root / DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)
    deals_path = data_dir / "deals.csv"
    manifest_path = data_dir / "manifest.json"
    shutil.copyfile(source_deals, deals_path)
    shutil.copyfile(source_manifest, manifest_path)

    manifest = json.loads(manifest_path.read_text())
    config_hash = manifest["config_hash"]

    deals = pd.read_csv(deals_path)
    enriched = add_workbench_columns(deals)

    train_df, validation_df = train_test_split(
        enriched,
        test_size=TEST_SIZE,
        random_state=SEED,
        stratify=enriched[LABEL_COLUMN],
    )
    train_df = train_df.reset_index(drop=True)
    validation_df = validation_df.reset_index(drop=True)

    feature_columns = model_feature_columns(enriched)
    categorical_columns = [c for c in feature_columns if enriched[c].dtype == "object"]
    numeric_columns = [c for c in feature_columns if c not in categorical_columns]
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
                    random_state=SEED,
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
    model.fit(train_df[feature_columns], train_df[LABEL_COLUMN])

    train_path = data_dir / "train.csv"
    validation_path = data_dir / "validation.csv"
    train_df.to_csv(train_path, index=False)
    validation_df.to_csv(validation_path, index=False)

    model_path = root / MODEL_PATH
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    print(f"Wrote panel copy: {deals_path} ({len(deals)} rows, config_hash={config_hash[:12]}...)")
    print(f"Wrote manifest copy: {manifest_path}")
    print(f"Wrote train split: {train_path} ({len(train_df)} rows)")
    print(f"Wrote validation split: {validation_path} ({len(validation_df)} rows)")
    print(f"Wrote model artifact: {model_path}")
    print(f"Model features ({len(feature_columns)}): {feature_columns}")


if __name__ == "__main__":
    main()
