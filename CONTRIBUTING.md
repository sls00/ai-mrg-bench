# Contributing — ai-mrg-bench

## Scope
Open, model-agnostic validation workbench for traditional ML credit models: tiering, bias and proxy testing, drift, hash-chained audit, and OCC reporting. It supports **review**; it does not certify compliance. Keep that boundary intact in code, docs, and report copy.

## Dev setup
```bash
uv sync --all-extras --dev
```

## Verification gate
```bash
uv run pytest -q                    # THE gate
uv run ruff check src tests         # lint
uv run mypy src                     # strict on src/workbench
```

## Run a validation
```bash
uv run workbench validate run --config configs/synth_fin_cre_baseline.yaml \
  --output-dir artifacts/synth_fin_cre_p5/
uv run workbench audit verify-chain
```

## Phase markers
Tag tests `@pytest.mark.phase0` … `phase5`. PR labels (`phase:p0` … `phase:p5`) set the CI floor. See `docs/dev.md`.

## Citation discipline
CI enforces a banlist of fabricated or withdrawn regulatory citations:

```bash
bash scripts/check_circular_banlist.sh
```

This exists because CFPB Circular 2026-03 could not be traced to any primary source, and because withdrawn circulars are routinely cited as current. Historical citations are fine **when clearly marked historical**. Never introduce a regulatory citation you have not verified against a primary source, and record the verification in `research/findings/`.

## Fixture integrity
```bash
bash scripts/check_fixture_hashes.sh
```

Frozen fixtures are hash-verified in CI. If you regenerate them, update the hashes in the same PR and explain why in the description.

## Branching
- `main` — integration branch
- `feat/…`, `fix/…` — short-lived branches; open **draft** PRs early

## Contributor License Agreement
Before your first pull request is merged, read [`CLA.md`](CLA.md) and include this line in the PR description:

> I have read and agree to the Contributor License Agreement in `CLA.md`.

Sign off your commits too (`git commit -s`). You keep the copyright to your work; the CLA grants the Maintainer the right to distribute it, including under different license terms in the future.

## License
[Blue Oak Model License 1.0.0](https://blueoakcouncil.org/license/1.0.0) — Copyright © 2026 Steven L. Sorenson. See `LICENSE`.
