# AI Model Risk & Governance Workbench

Open, model-agnostic validation workbench for traditional ML credit models: tiering, bias/proxy testing, adverse-action translation, drift monitoring, hash-chained audit log, and OCC seven-section reporting.

**Status:** P0–P3 German Credit demo path implemented; P4 Home Credit/BISG architecture notebook shipped (no CI gate); P5 synth-fin CRE fair-lending demo implemented (CI-gated).

## See the output first

[**`docs/examples/`**](docs/examples/) holds a committed run you can read without installing anything — an OCC seven-section validation report, the bias metrics behind it, and its audit-chain verification. In that run the adverse impact ratio (0.9036) clears the conventional four-fifths screen while error-rate parity shows creditworthy loans in the affected group denied 2.96× as often, which is the case a single-metric screen misses.

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

## Notebooks

| Notebook | Role |
| -------- | ---- |
| [`notebooks/01_german_credit_validation.ipynb`](notebooks/01_german_credit_validation.ipynb) | Thin companion: CLI wrappers for the P2 full run + P3 CA overlay, ending in a side-by-side §II diff. Restores the dropped P2 AC notebook surface without rewriting the full R-10 §5.1 tutorial — **CLI remains canonical** for CI/reproducibility. |
| [`notebooks/02_home_credit_bias_proxy.ipynb`](notebooks/02_home_credit_bias_proxy.ipynb) | P4 scale story: Home Credit + `surgeo` BISG **architecture** (illustrative US surname/ZCTA sample; no production module; no CI gate). |

```bash
uv sync --all-extras --dev
uv run jupyter notebook notebooks/01_german_credit_validation.ipynb
uv run jupyter notebook notebooks/02_home_credit_bias_proxy.ipynb
```

### P4 demo limitation (BISG architecture only)

German Credit has no US surname/geography fields, so race/ethnicity BISG cannot run on the canonical demo. P4 documents how a Home Credit–scale proxy path would attach to Layer C via `surgeo`, using a **synthetic US panel** (`data/illustrative/home_credit_bisg_proxy_sample.csv`) — not a vendored Kaggle dump. `surgeo` 1.1.2 uses 2010 Census tables (2020 DHC gap: deep-research V4/V5). This is review-support architecture evidence, not an ECOA determination.

## Demo path (P5 — synth-fin CRE fair-lending demo)

P5 is an **additive, CI-gated** demo phase built on a synthetic commercial real-estate (CRE) panel from the sibling [`synth-fin`](https://github.com/sls00/synth-fin) project. It **complements P4's BISG architecture — it does not replace it**: P4 shows how race/ethnicity BISG attaches at Home Credit scale; P5 exercises the same three-layer bias battery end-to-end (Layers A/B/C, adverse-impact ratio, error parity, proxy risk) on a **geography proxy** (`minority_tract_pct`, binned at its top quintile) — not surname/BISG race inference.

```bash
uv run workbench validate run \
  --config configs/synth_fin_cre_baseline.yaml \
  --output-dir artifacts/synth_fin_cre_p5/
```

The committed panel (`data/synthetic_cre/deals.csv` + `manifest.json`) is a byte-identical copy of synth-fin's own generator output, reproducible via:

```bash
cd ../synth-fin
uv run synth-fin generate \
  --scenario base \
  --bias-profile proxy_discrimination_mild \
  --n 5000 \
  --seed 42 \
  --out /tmp/sf-p5-panel
```

See [`docs/dev.md`](docs/dev.md#p5-fixture-bootstrap-synth-fin-cre-panel) for the full bootstrap sequence (train/validation split, model training, fixture-manifest freeze). `scripts/check_fixture_hashes.sh` gates this panel the same way it already gates German Credit's fixtures — no new CI job, one generalized script.

### P5 demo limitations

- **Geography proxy, not BISG.** `minority_tract_top_quintile` bins `minority_tract_pct` at its 80th percentile; it is a census-tract-level geography proxy, not a surname/BISG race or ethnicity inference. It complements, and does not replace, P4's BISG architecture demo.
- **Synthetic ground truth, not observed disparity.** The subgroup adverse-decision shift is a `synth-fin`-injected bias profile (`proxy_discrimination_mild`), independently reproducible from the panel's `manifest.json` — not an observed real-world lending disparity.
- **Adverse-action translation out of scope.** `modules.adverse_action_translator` is disabled for this config: `workbench.adverse_action`'s Reg B specific-reasons mapping-rules catalog is German-Credit-specific and does not yet cover CRE features. Extending it is future work, not part of this demo phase.

## Documentation

- Research baseline: [`deep-research-v1.md`](deep-research-v1.md)
- Developer guide: [`docs/dev.md`](docs/dev.md)
- Build spec: [`.gstack/SPEC-P0-P2-v2.md`](.gstack/SPEC-P0-P2-v2.md) (local agent context; not committed)
- P3 authority: [`research/findings/R-10-mvp-phasing-demo-scenario.md`](research/findings/R-10-mvp-phasing-demo-scenario.md) §2/§3/§8; [`research/findings/R-08-state-ai-lending-laws.md`](research/findings/R-08-state-ai-lending-laws.md)
- P4 BISG authority: R-03, R-07, R-10 §2 P4 row; caveats V4/V5 in [`deep-research-v1.md`](deep-research-v1.md) §10.2

## Do-not-claim (messaging hygiene)

Per R-14 close-out — do **not** assert in shipping copy:

- CFPB **Circular 2026-03** as current operative authority (no primary source found; see `research/findings/R-12-circular-2026-03-primary-verification.md`)
- That withdrawn Circular 2022-03/2023-03 positions remain current CFPB guidance without noting May 12, 2025 withdrawal

Historical citations of withdrawn circulars are allowed when clearly marked historical.

## License

[Blue Oak Model License 1.0.0](LICENSE) — Copyright © 2026 Steven L. Sorenson.
