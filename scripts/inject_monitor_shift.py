#!/usr/bin/env python3
"""Inject deterministic covariate shift into the German Credit monitor split."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--validation",
        default="data/german_credit_validation.csv",
        help="Path to the validation split CSV.",
    )
    parser.add_argument(
        "--train",
        default="data/german_credit_train.csv",
        help="Path to the training split CSV.",
    )
    parser.add_argument(
        "--model",
        default="models/german-credit-xgb-v1.2.joblib",
        help="Path to trained model artifact.",
    )
    parser.add_argument(
        "--output",
        default="data/german_credit_monitor.csv",
        help="Path to write monitor split with injected shift.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)

    validation = pd.read_csv(args.validation)
    train = pd.read_csv(args.train)
    monitor = validation.copy()

    # R-10 §4.5: duration * 1.35 + Gaussian noise sigma=2
    duration_noise = rng.normal(loc=0.0, scale=2.0, size=len(monitor))
    shifted_duration = np.round(monitor["duration"] * 1.35 + duration_noise).astype(int)
    monitor["duration"] = np.clip(shifted_duration, a_min=1, a_max=None)

    # R-10 §4.5: +2000 offset to 40% rows for credit_amount
    shift_mask = rng.random(len(monitor)) < 0.40
    monitor.loc[shift_mask, "credit_amount"] = monitor.loc[shift_mask, "credit_amount"] + 2000

    # R-10 §4.5: resample installment_commitment with +15% mean shift
    resampled = train["installment_commitment"].sample(
        n=len(monitor),
        replace=True,
        random_state=args.seed,
    )
    shifted_installment = np.round(resampled.to_numpy(dtype=float) * 1.15).astype(int)
    monitor["installment_commitment"] = np.clip(shifted_installment, a_min=1, a_max=4)

    model = joblib.load(args.model)
    feature_names = [str(name) for name in model.feature_names_in_]
    scores = model.predict_proba(monitor[feature_names])[:, 1]
    monitor["approval_binary"] = (scores >= 0.5).astype(int)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    monitor.to_csv(output_path, index=False)
    print(f"Wrote shifted monitor split: {output_path} ({len(monitor)} rows)")


if __name__ == "__main__":
    main()
