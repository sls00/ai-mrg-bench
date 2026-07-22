#!/usr/bin/env bash
# Fixture integrity gate — compares on-disk bytes to manifests/german_credit_fixture_manifest.yaml.
# Skips with exit 0 until the manifest exists (pre-P0 fixture bootstrap).
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

MANIFEST="manifests/german_credit_fixture_manifest.yaml"

if [ ! -f "$MANIFEST" ]; then
  echo "SKIP: $MANIFEST not found (fixture bootstrap not run yet)."
  exit 0
fi

uv run python - <<'PY'
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import yaml

root = Path(".")
manifest_path = root / "manifests/german_credit_fixture_manifest.yaml"
data = yaml.safe_load(manifest_path.read_text())
entries = data.get("artifacts") or data.get("files") or []

if not entries:
    print(f"FAIL: no artifacts listed in {manifest_path}")
    sys.exit(1)

failures = 0
for entry in entries:
    if isinstance(entry, str):
        rel = entry
        expected = None
    else:
        rel = entry["path"]
        expected = entry.get("sha256")

    path = root / rel
    if not path.is_file():
        print(f"MISSING: {rel}")
        failures += 1
        continue

    if expected:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != expected.lower():
            print(f"HASH MISMATCH: {rel}")
            print(f"  expected: {expected}")
            print(f"  actual:   {digest}")
            failures += 1
        else:
            print(f"OK: {rel}")

if failures:
    print(f"\nFAIL: {failures} fixture issue(s).")
    sys.exit(1)

print(f"PASS: {len(entries)} fixture artifact(s) match manifest.")
PY
