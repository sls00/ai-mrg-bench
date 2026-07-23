# AI Model Risk & Governance Workbench

Open, model-agnostic validation workbench for traditional ML credit models: tiering, bias/proxy testing, adverse-action translation, drift monitoring, hash-chained audit log, and OCC seven-section reporting.

**Status:** P0–P3 German Credit demo path implemented (P4 Home Credit/BISG deferred).

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

## Demo path (German Credit)

```bash
# Full federal run (P2)
uv run workbench validate run --config configs/german_credit_full.yaml

# P3 CA overlay (primary) — emits admt_risk_assessment_summary.json
uv run workbench validate run \
  --config configs/german_credit_ca_overlay.yaml \
  --output-dir artifacts/run_ca_overlay/

# P3 CO overlay (alternative) — emits co_disclosure_checklist.json only
uv run workbench validate run --config configs/german_credit_co_overlay.yaml

uv run workbench audit verify-chain
```

### P3 demo limitation (jurisdictional frame only)

The CA/CO `state_overlay` toggle is a **jurisdictional-frame demonstration** on UCI German Credit (non-US data, no race/BISG). It changes report §II framing and emits overlay evidence artifacts for portfolio review. It is **not** a compliance determination, CPPA certification, California AG determination, or Colorado AG determination. Layer A metrics are labeled **outcomes analysis / risk-assessment evidence**, never ECOA or state disparate-impact compliance.

## Documentation

- Research baseline: [`deep-research-v1.md`](deep-research-v1.md)
- Developer guide: [`docs/dev.md`](docs/dev.md)
- Build spec: [`.gstack/SPEC-P0-P2-v2.md`](.gstack/SPEC-P0-P2-v2.md) (local agent context; not committed)
- P3 authority: [`research/findings/R-10-mvp-phasing-demo-scenario.md`](research/findings/R-10-mvp-phasing-demo-scenario.md) §2/§3/§8; [`research/findings/R-08-state-ai-lending-laws.md`](research/findings/R-08-state-ai-lending-laws.md)

## Do-not-claim (messaging hygiene)

Per R-14 close-out — do **not** assert in shipping copy:

- CFPB **Circular 2026-03** as current operative authority (no primary source found; see `research/findings/R-12-circular-2026-03-primary-verification.md`)
- That withdrawn Circular 2022-03/2023-03 positions remain current CFPB guidance without noting May 12, 2025 withdrawal

Historical citations of withdrawn circulars are allowed when clearly marked historical.

## License

MIT
