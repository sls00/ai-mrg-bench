#!/usr/bin/env python3
"""Freeze German Credit fixture hashes into a deterministic manifest."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
from pathlib import Path

import pandas as pd
import yaml


@dataclass(frozen=True)
class FixtureEntry:
    path: str
    role: str
    rows: int | None


FILES: list[FixtureEntry] = [
    FixtureEntry("data/raw/german_credit_uci.csv", "source_of_truth", 1000),
    FixtureEntry("data/german_credit_train.csv", "drift_reference_population", 700),
    FixtureEntry("data/german_credit_validation.csv", "validation_run_primary", 300),
    FixtureEntry("data/german_credit_monitor.csv", "drift_monitor_injected_shift", 300),
    FixtureEntry("models/german-credit-xgb-v1.2.joblib", "pre_trained_model", None),
    FixtureEntry("configs/feature_mapping_german_credit.yaml", "adverse_action_feature_dictionary", None),
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def row_count(path: Path) -> int | None:
    if path.suffix.lower() != ".csv":
        return None
    return int(len(pd.read_csv(path)))


def main() -> None:
    root = Path.cwd()
    manifest_rows: list[dict[str, object]] = []
    for entry in FILES:
        abs_path = root / entry.path
        if not abs_path.exists():
            raise FileNotFoundError(f"Missing fixture artifact: {entry.path}")
        rows = entry.rows if entry.rows is not None else row_count(abs_path)
        manifest_rows.append(
            {
                "path": entry.path,
                "role": entry.role,
                "rows": rows,
                "sha256": sha256_file(abs_path),
            },
        )

    payload = {
        "fixture_version": str(date.today()),
        "seed": 42,
        "derivation_rules_version": "1.0",
        "files": manifest_rows,
    }
    manifest_path = root / "manifests" / "german_credit_fixture_manifest.yaml"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(yaml.safe_dump(payload, sort_keys=False))
    print(f"Wrote fixture manifest: {manifest_path}")


if __name__ == "__main__":
    main()
