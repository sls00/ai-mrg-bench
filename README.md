# AI Model Risk & Governance Workbench

Open, model-agnostic validation workbench for traditional ML credit models: tiering, bias/proxy testing, adverse-action translation, drift monitoring, hash-chained audit log, and OCC seven-section reporting.

**Status:** Research complete; application scaffold bootstrapped. P0 core loop not yet implemented.

## Quick start

```bash
git lfs install
git clone git@github.com:sls00/ai-mrg-bench.git
cd ai-mrg-bench
git lfs pull
uv sync --all-extras --dev
uv run workbench version
```

Frozen demo model artifacts (`models/*.joblib`) are tracked via **Git LFS**. Run `git lfs install` once per machine and `git lfs pull` after clone.

## Documentation

- Research baseline: [`deep-research-v1.md`](deep-research-v1.md)
- Developer guide: [`docs/dev.md`](docs/dev.md)
- Build spec: [`.gstack/SPEC-P0-P2-v2.md`](.gstack/SPEC-P0-P2-v2.md) (local agent context; not committed)

## Do-not-claim (messaging hygiene)

Per R-14 close-out — do **not** assert in shipping copy:

- CFPB **Circular 2026-03** as current operative authority (no primary source found; see `research/findings/R-12-circular-2026-03-primary-verification.md`)
- That withdrawn Circular 2022-03/2023-03 positions remain current CFPB guidance without noting May 12, 2025 withdrawal

Historical citations of withdrawn circulars are allowed when clearly marked historical.

## License

MIT
