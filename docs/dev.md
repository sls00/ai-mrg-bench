# Developer guide — AI MRG Workbench

Mechanical conventions for phase-gated delivery (`SPEC-P0-P2-v2.md`).

## Prerequisites

- Python **3.11** or **3.12** (CI matrix)
- [uv](https://docs.astral.sh/uv/) for lockfile-driven installs
- [Git LFS](https://git-lfs.com/) for frozen demo models (`models/*.joblib`)

```bash
git lfs install
git lfs pull
uv sync --all-extras --dev
```

## Worktree + phase-PR discipline

Branch protection is **not** enabled on this private repo (free-tier limitation). Use dedicated worktrees per phase PR:

| Phase | Branch (example) | PR label |
| ----- | ---------------- | -------- |
| AC0 | `worktree-docs+r14-messaging-amendment` | `phase:ac0` |
| Bootstrap | `chore/repo-bootstrap` | `phase:ac0` (docs + scaffold only) |
| P0 | `feat/p0-core-loop` | `phase:p0` |
| P1 | `feat/p1-adverse-action` | `phase:p1` |
| P2 | `feat/p2-drift-ci-api` | `phase:p2` |
| P3 | `feat/p3-ca-overlay` | `phase:p3` |

```bash
git worktree add ../ai-mrg-bench-p0 -b feat/p0-core-loop main
```

Squash WIP checkpoints before merge. Each phase PR should be reviewable in isolation.

## CI phase-floor protocol

GitHub Actions reads the PR label (`pull_request.labels` / `gh pr view`) and gates jobs:

| PR label | Required pytest | Other gates |
| -------- | --------------- | ----------- |
| `phase:ac0` | none (docs + scaffold) | `scripts/check_circular_banlist.sh` |
| `phase:p0` | `-m phase0` | ruff, mypy, fixture-hash |
| `phase:p1` | `-m "phase0 or phase1"` | same |
| `phase:p2` | `-m "phase0 or phase1 or phase2"` | + API smoke (`-m "phase2 and api"`) |
| `phase:p3` | `-m "phase0 or phase1 or phase2 or phase3"` | same |

Unlabeled PRs run lint/type-check + banlist only (no phase pytest floor).

## Local checks

```bash
# Messaging hygiene (Circular 2026-03 banlist)
bash scripts/check_circular_banlist.sh

# Lint + types
uv run ruff check src tests
uv run mypy src

# Fixture integrity (after P0 fixture bootstrap)
bash scripts/check_fixture_hashes.sh

# Phase tests (once implemented)
uv run pytest -m phase0
```

## Dependency pin note

- `aequitas` is pinned to `1.1.0` in `pyproject.toml` after a local German Credit compatibility smoke (`import aequitas` + `Group().get_crosstabs(...)`).

## Fixture bootstrap (run once before P0 evals)

See `SPEC-P0-P2-v2.md` §Fixture bootstrap sequence:

1. Add UCI German Credit CSV → `data/raw/german_credit_uci.csv`
2. Train XGBClassifier (seed 42) → `models/german-credit-xgb-v1.2.joblib`
3. Emit train/validation splits → `data/german_credit_{train,validation}.csv`
4. `scripts/inject_monitor_shift.py` → `data/german_credit_monitor.csv`
5. `scripts/freeze_german_credit_fixtures.py` → `manifests/german_credit_fixture_manifest.yaml`
6. Commit manifest + data + model (model via Git LFS)

CI `fixture-hash-verify` fails if on-disk bytes ≠ manifest.

## Package layout (target)

```
src/workbench/     # CLI, SDK, modules (P0+)
configs/           # german_credit_{p0,baseline,full}.yaml
schemas/           # JSON Schema for appendices
templates/         # OCC 2026-13 Jinja2
data/ models/ manifests/
tests/             # unit, property, integration, golden
```

## Messaging authority

Shipping copy authority: `deep-research-v1.md` + `research/findings/R-01`–`R-14`. Do **not** assert CFPB Circular 2026-03 as operative authority — see R-12/R-14.
