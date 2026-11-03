# Example output

Real output from a real run, committed so you can read the deliverable without installing anything.

## `synth_fin_cre_p5/` — CRE credit model, fair-lending validation

A Tier-3 commercial real-estate credit model put through the full validation path: intake gate, three-layer bias battery, hash-chained audit, and an OCC 2026-13 seven-section report.

| File | What it is |
| --- | --- |
| [`validation_report.md`](synth_fin_cre_p5/validation_report.md) | The seven-section report an independent validator would hand to a model risk committee |
| [`bias_battery_summary.json`](synth_fin_cre_p5/bias_battery_summary.json) | Per-layer metrics behind §V.2, including per-group rates |
| [`audit_chain_verification.json`](synth_fin_cre_p5/audit_chain_verification.json) | Hash-chain verification result: 3 events, 0 breaks |
| [`report.json`](synth_fin_cre_p5/report.json) | Machine-readable form of the same report |

### What this run demonstrates

The bias profile in this dataset is **injected on purpose**, so the correct answer is known in advance. That makes the run a positive control: the question is not whether the model is biased, it is whether the battery detects a disparity that was deliberately planted.

It does, and the interesting part is *where*:

- **Layer A** reports an adverse impact ratio of **0.9036**. The conventional four-fifths screen flags at 0.80, so this run **passes** that test.
- **Layer B** reports a false-negative-rate parity ratio of **2.9571**: creditworthy loans in the affected group were denied nearly three times as often as in the reference group (14.4% vs 4.9%).

A single-metric adverse-impact screen would have cleared this model. Error-rate parity does not. That gap is the reason the battery has three layers rather than one.

> **Correction (2 Nov 2026):** an earlier version of this run reported an FNR parity of 2.2283. That figure scored decisions against `elevated_credit_risk` (1 = risky) while the decision column uses 1 = approved, so it counted risky loans that were denied, which is not an error. The battery now uses a derived `creditworthy` label (1 = good, matching German Credit's `credit_risk`). The model, data split and Layer A results are unchanged.

### Reproducing it

```bash
uv sync --all-extras --dev
uv run workbench validate run \
  --config configs/synth_fin_cre_baseline.yaml \
  --output-dir artifacts/synth_fin_cre_p5/
uv run workbench audit verify-chain
```

The input panel comes from [`synth-fin`](https://github.com/sls00/synth-fin):

```bash
synth-fin generate --scenario base --bias-profile proxy_discrimination_mild \
  --n 5000 --seed 42
```

Both are seeded, so the metrics above reproduce exactly.

### Limitations

This is synthetic data, not real borrower or property records, and the subgroup shift is a ground-truth injection rather than an observed real-world disparity. `minority_tract_top_quintile` is a geography proxy, **not** surname or BISG race inference. The report supports review; it is not a compliance determination. Section II of the report states the full scope limits.
