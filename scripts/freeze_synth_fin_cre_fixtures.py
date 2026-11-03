#!/usr/bin/env python3
"""Freeze P5 synth-fin CRE fixture hashes into a deterministic manifest.

Mirrors `scripts/freeze_german_credit_fixtures.py`'s shape exactly
(`fixture_version`/`seed`/`derivation_rules_version`/`files[]`), plus one
additive field -- `synth_fin_config_hash` -- pinning the upstream synth-fin
`config_hash` so drift in the *source* panel (not just these committed
bytes) is independently checkable against `data/synthetic_cre/manifest.json`.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd
import yaml


@dataclass(frozen=True)
class FixtureEntry:
    path: str
    role: str
    rows: int | None


FILES: list[FixtureEntry] = [
    FixtureEntry("data/synthetic_cre/deals.csv", "source_of_truth", 5000),
    FixtureEntry("data/synthetic_cre/manifest.json", "source_of_truth_manifest", None),
    FixtureEntry("data/synthetic_cre/train.csv", "model_training_population", 3500),
    FixtureEntry("data/synthetic_cre/validation.csv", "validation_run_primary", 1500),
    FixtureEntry("models/synth-fin-cre-xgb-v1.0.joblib", "pre_trained_model", None),
    FixtureEntry(
        "configs/feature_mapping_synth_fin_cre.yaml",
        "adverse_action_feature_dictionary",
        None,
    ),
]

MANIFEST_PATH = Path("manifests/synth_fin_cre_fixture_manifest.yaml")


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
            raise FileNotFoundError(
                f"Missing fixture artifact: {entry.path} "
                "(run scripts/bootstrap_synth_fin_cre_fixtures.py first)",
            )
        rows = entry.rows if entry.rows is not None else row_count(abs_path)
        manifest_rows.append(
            {
                "path": entry.path,
                "role": entry.role,
                "rows": rows,
                "sha256": sha256_file(abs_path),
            },
        )

    synth_fin_manifest = json.loads((root / "data/synthetic_cre/manifest.json").read_text())
    synth_fin_config_hash = synth_fin_manifest["config_hash"]

    payload = {
        "fixture_version": str(date.today()),
        "seed": 42,
        "derivation_rules_version": "1.1",
        "synth_fin_config_hash": synth_fin_config_hash,
        "files": manifest_rows,
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    (root / MANIFEST_PATH).write_text(yaml.safe_dump(payload, sort_keys=False))
    print(f"Wrote fixture manifest: {MANIFEST_PATH}")
    print(f"Pinned synth_fin_config_hash={synth_fin_config_hash}")


if __name__ == "__main__":
    main()
