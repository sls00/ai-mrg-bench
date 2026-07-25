#!/usr/bin/env bash
# Fixture integrity gate — compares on-disk bytes to every
# manifests/*_fixture_manifest.yaml (german_credit, synth_fin_cre, ...).
# Skips with exit 0 until at least one manifest exists (pre-P0 fixture bootstrap).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

MANIFEST_DIR="manifests"
shopt -s nullglob
manifests=("$MANIFEST_DIR"/*_fixture_manifest.yaml)
shopt -u nullglob

if [ ${#manifests[@]} -eq 0 ]; then
  echo "SKIP: no $MANIFEST_DIR/*_fixture_manifest.yaml found (fixture bootstrap not run yet)."
  exit 0
fi

uv run python - <<'PY'
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml

root = Path(".")
manifest_paths = sorted(root.glob("manifests/*_fixture_manifest.yaml"))

if not manifest_paths:
    print("FAIL: no manifests/*_fixture_manifest.yaml found.")
    sys.exit(1)

failures = 0
total_entries = 0
for manifest_path in manifest_paths:
    data = yaml.safe_load(manifest_path.read_text())
    entries = data.get("artifacts") or data.get("files") or []

    if not entries:
        print(f"FAIL: no artifacts listed in {manifest_path}")
        failures += 1
        continue

    for entry in entries:
        if isinstance(entry, str):
            rel = entry
            expected = None
        else:
            rel = entry["path"]
            expected = entry.get("sha256")

        path = root / rel
        if not path.is_file():
            print(f"MISSING: {rel} (from {manifest_path})")
            failures += 1
            continue

        if expected:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if digest != expected.lower():
                print(f"HASH MISMATCH: {rel} (from {manifest_path})")
                print(f"  expected: {expected}")
                print(f"  actual:   {digest}")
                failures += 1
            else:
                print(f"OK: {rel}")
        total_entries += 1

if failures:
    print(f"\nFAIL: {failures} fixture issue(s) across {len(manifest_paths)} manifest(s).")
    sys.exit(1)

print(f"PASS: {total_entries} fixture artifact(s) match across {len(manifest_paths)} manifest(s).")
PY
