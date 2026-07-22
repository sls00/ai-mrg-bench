# R-05 — Drift Detection & Materiality-Tier Escalation

**Ticket:** R-05  
**Session:** 2  
**Status:** Complete  
**Research date:** 2026-07-20  
**Depends on:** R-01 (monitoring patterns), OCC 2026-13 materiality framework (foundation §3.1)

---

## 1. Executive summary

**Recommendation:** Implement a **tier-gated drift monitoring engine** tracking three drift classes — **population (data) drift**, **performance (concept) drift**, and **score stability** — using PSI and KS as primary distributional tests, AUC/Gini/KS-statistic and calibration metrics for performance, with **materiality-tier-dependent escalation** mapped to OCC 2026-13 §V ongoing monitoring language.

OCC 2026-13 does **not** prescribe numeric thresholds. The Workbench should ship **documented default heuristics** (industry Lewis PSI bands + practitioner AUC-decay bands) as configurable starting points, with explicit acknowledgment that institutions must calibrate to their model risk appetite.

**Key OCC principle (primary ✅):**

> "When performance deviates meaningfully from expectations, banking organizations generally consider whether model adjustments, recalibration, or redevelopment are warranted."

> "The frequency and scope of monitoring reports will depend on the nature of the model, the availability of new data or modeling approaches, and **model materiality**."

---

## 2. Drift taxonomy

| Class | What shifts | Detection methods | Typical lag |
| ----- | ----------- | ----------------- | ----------- |
| **Population drift** | Input feature distributions P(X) | PSI, CSI, KS, Jensen-Shannon | Immediate (scoring-time) |
| **Score drift** | Output score distribution P(score) | PSI on score bins, KS on scores | Immediate |
| **Performance drift** | Relationship P(Y\|X) — discrimination/calibration | AUC, Gini, KS-statistic, Brier, ECE | Delayed (requires outcome seasoning) |
| **Concept drift** | Target definition or economic regime change | Back-testing, vintage analysis, residual trends | Months |

---

## 3. Recommended metrics and default thresholds

### 3.1 Population Stability Index (PSI) — primary

**Definition:** Sum over bins of `(actual% - expected%) × ln(actual% / expected%)`  
**Origin:** Lewis (1994); industry "Lewis constants" ⚠

| PSI value | Industry interpretation | Default Workbench action |
| --------- | ----------------------- | ------------------------ |
| < 0.10 | Stable | Log; continue monitoring |
| 0.10 – 0.25 | Moderate shift — investigate | **Amber alert**; root-cause analysis |
| ≥ 0.25 | Significant shift | **Red alert**; escalation per materiality tier |

**Caveats (document in methodology artifact):**
- Lewis thresholds are **heuristics**, not statistically derived ✅ (Western Michigan PSI paper; Annals of OR 2025 PRS paper)
- Thresholds do not account for sample size — small samples over-trigger, large samples under-trigger
- **Recommendation:** Offer optional sample-size-adjusted PSI benchmarks (α = 0.05) as advanced mode; default to Lewis for practitioner familiarity

**Application scope:**
- **Score PSI** — primary portfolio-level stability indicator
- **Feature PSI (CSI)** — per-input diagnostic to localize drift source
- Binning: deciles on development sample; minimum 5% expected per bin (merge tails)

### 3.2 Kolmogorov-Smirnov (KS) — secondary distributional

| Application | Use |
| ----------- | --- |
| Continuous feature drift | KS statistic + p-value between development and current distributions |
| Score distribution | KS between development and current score CDFs |
| Discrimination power | KS-statistic = max separation between good/bad score CDFs (performance metric, not drift per se) |

**Default thresholds (configurable):**

| Test | Amber | Red |
| ---- | ----- | --- |
| Feature KS p-value | < 0.05 | < 0.01 |
| Score KS p-value | < 0.05 | < 0.01 |
| Performance KS-statistic drop from baseline | > 5% relative | > 10% relative |

### 3.3 Performance metrics

| Metric | Formula / meaning | Amber trigger | Red trigger |
| ------ | ----------------- | ------------- | ----------- |
| **AUC** | Area under ROC | Drop ≥ 0.02 from baseline | Drop ≥ 0.05 from baseline |
| **Gini** | 2×AUC − 1 | Equivalent relative drop | Equivalent relative drop |
| **Brier score** | Mean squared error of probabilities | Increase ≥ 10% relative | Increase ≥ 20% relative |
| **ECE** | Expected calibration error | > 1.5× baseline | > 2× baseline |
| **Approval rate shift** | Portfolio-level selection rate change | > 5 pp vs. development | > 10 pp vs. development |

**Note:** AUC drop ≥ 0.05 as "material" is practitioner convention ⚠ (DC-Guard TechRxiv paper; SR 11-7 monitoring literature); not OCC-prescribed.

### 3.4 Supplementary indicators

| Indicator | Purpose |
| --------- | ------- |
| Missingness rate drift | Data pipeline failure detection |
| Outlier z-score drift | Silent unit/encoding errors |
| Segment-level PSI | Fair-lending-relevant subgroup stability (ties to R-03) |
| Champion-challenger divergence | Model comparison trigger |

---

## 4. Materiality-tier escalation matrix

OCC 2026-13 organizes oversight by **model materiality** = f(exposure, purpose). The Workbench tiering engine (foundation §3.1) should bind drift responses to tier.

### 4.1 Tier definitions (Workbench default)

| Tier | Exposure heuristic | Purpose heuristic | Monitoring cadence |
| ---- | ------------------ | ----------------- | ------------------ |
| **T1 — Immaterial** | < 1% portfolio or internal low-impact | Non-regulatory, experimental | Quarterly |
| **T2 — Moderate** | 1–10% portfolio | Business decision support | Monthly |
| **T3 — Material** | > 10% portfolio or regulatory/reporting | Credit decisioning, CECL, capital | Weekly + event-driven |

*Institutions customize; Workbench provides configurable schema.*

### 4.2 Escalation policy (default — traffic-light)

| Alert level | Trigger (any of) | T1 response | T2 response | T3 response |
| ----------- | ---------------- | ----------- | ----------- | ----------- |
| **Green** | All PSI < 0.10; AUC within 0.02 of baseline | Log only | Log only | Log + dashboard |
| **Amber** | Any PSI 0.10–0.25; OR AUC drop 0.02–0.05; OR feature KS p < 0.05 | Log + flag for annual review | Analyst review within 30 days; root-cause memo | Validator notification within 10 days; increased monitoring frequency |
| **Red** | Any PSI ≥ 0.25; OR AUC drop ≥ 0.05; OR ECE > 2× baseline; OR approval rate shift > 10 pp | Escalate to T2 review within 60 days | Validator re-validation scoping within 30 days | **Full re-validation trigger**; model use restriction pending review; MRM committee within 15 days |
| **Critical** | Red + fair-lending metric breach (R-03 AIR < 0.80 on FHA overlay) | — | Compliance + MRM joint review | **Immediate suspension** of automated decisions; regulatory notification assessment |

### 4.3 OCC 2026-13 mapping

| OCC 2026-13 concept | Workbench implementation |
| ------------------- | ------------------------ |
| §V Ongoing Model Monitoring | Scheduled drift runs + dashboard |
| "Performance deviates meaningfully from expectations" | Amber/Red threshold breach |
| "Model adjustments, recalibration, or redevelopment" | Escalation action menu |
| Materiality determines "frequency and scope" | Tier → cadence + escalation depth |
| Immaterial models: "monitoring... conditions under which use may become material" | T1 → auto re-tier check when exposure crosses threshold |
| §V Outcomes Analysis | Performance drift metrics on seasoned vintages |
| §VI Governance | Escalation audit trail with approver identity |
| FINOS mi-4 (observability) | Drift indicators in audit log per Art. 12(2)(b) |
| EU AI Act Art. 72 | Post-market monitoring feed (secondary) |

### 4.4 Escalation workflow (actionable)

```
drift_event detected
  → classify alert_level (green/amber/red/critical)
  → lookup model.tier → escalation_policy
  → create audit_log_entry (metric values, threshold, tier, recommended_action)
  → IF tier >= T2 AND alert >= amber: notify model_owner
  → IF tier == T3 AND alert >= red: create revalidation_ticket
  → IF critical: block_auto_decisioning flag (configurable kill-switch)
  → append to OCC §V monitoring section of validation report
```

---

## 5. Monitoring architecture

### 5.1 Reference population

- **Development sample** — primary reference for PSI/KS (frozen at model approval)
- **Rolling window** — last 3 months production for trend detection
- **Out-of-time holdout** — validation-time OOT set for initial baseline comparison

### 5.2 Monitoring cadence by tier

| Tier | Score PSI | Feature CSI | Performance (AUC) | Report |
| ---- | --------- | ----------- | ----------------- | ------ |
| T1 | Quarterly | Annual | Semi-annual | Summary log |
| T2 | Monthly | Quarterly | Quarterly | Analyst dashboard |
| T3 | Weekly | Monthly | Monthly (+ vintage) | Full monitoring report → §V appendix |

### 5.3 Competitive alignment (R-01)

| Product | Drift approach | Workbench differentiation |
| ------- | -------------- | ------------------------- |
| Fiddler AI | PSI-style, 30+ ML metrics | Match metric breadth; add OCC tier escalation |
| Solytics NIMBUS | Threshold-triggered re-validation | Match pattern; open implementation |
| ValidMind | Integration-dependent | Native battery, not external dependency |
| Monitaur | Crypto-signed decision logs | Combine drift events with tamper-evident log (R-06) |

---

## 6. Demo integration (feeds R-10)

**Home Credit Default Risk** supports drift demo via:
- Temporal split: train on early applications, monitor on later (simulated production)
- Inject covariate shift on `EXT_SOURCE_*` features to trigger Amber/Red PSI
- Show tier escalation: same drift event → different response for T2 vs T3 model

**German Credit:** Random perturbation of feature distributions for PSI tutorial (simpler, smaller).

---

## 7. OSS / implementation stack

| Component | Library | Role |
| --------- | ------- | ---- |
| PSI/CSI calculation | `evidently` or custom numpy | Feature + score stability |
| KS test | `scipy.stats.ks_2samp` | Distributional comparison |
| Performance metrics | `sklearn.metrics` | AUC, Brier, confusion matrix |
| Calibration | `sklearn.calibration` or custom ECE | Calibration drift |
| Visualization | matplotlib/plotly | Monitoring dashboard |
| Audit binding | Workbench audit module (R-06) | Hash-chained drift events |

**Do not rebuild:** PSI/KS are commodity; differentiate on **tier escalation policy + OCC report integration**.

---

## 8. Implications for Workbench

1. **Implement three-class drift engine** (population, score, performance) with PSI as primary, KS as secondary.
2. **Ship configurable Lewis thresholds** as defaults with documented statistical limitations.
3. **Bind escalation to materiality tier** — same drift event produces different mandated actions by tier; this operationalizes OCC 2026-13 proportionality.
4. **Generate monitoring report section** for OCC §V Ongoing Model Monitoring on every drift run.
5. **Link Red/Critical alerts to re-validation workflow** — not just dashboard warnings.
6. **Include segment-level drift** for fair-lending subgroup stability (bridge to R-03).
7. **Audit log every drift event** with metric snapshot, threshold, tier, and action taken (FINOS mi-4 + mi-21).
8. **Demo:** Home Credit temporal split showing Amber → T3 Red escalation path.

---

## 9. Sources

| ID | Source | Tier | Status | Used for |
| -- | ------ | ---- | ------ | -------- |
| S-38 | OCC Bulletin 2026-13 PDF | 1 | ✅ | Monitoring, materiality, performance deviation |
| S-39 | Lewis (1994) / Siddiqi PSI thresholds | 2 | ⚠ | 0.10/0.25 heuristics |
| S-40 | Western Michigan "Statistical properties of PSI" | 2 | ✅ | Threshold limitations |
| S-41 | Annals of OR 2025 Population Resemblance Statistic | 2 | ⚠ | Sample-size-adjusted alternative |
| S-42 | DC-Guard TechRxiv (Fannie Mae drift policy) | 2 | ⚠ | Tier-gated traffic-light pattern |
| S-43 | SR 11-7 original monitoring language | 1 | ✅ | Early warning metrics, outcomes analysis |
| S-44 | Fiddler AI GRC (R-01) | 3 | ✅ | Competitive PSI monitoring |
| S-07 | Fiddler AI product pages | 3 | ✅ | Industry metric breadth |

---

## 10. Open questions

1. **Sample-size-adjusted PSI:** Implement in v1 or document as v1.1 enhancement?
2. **Real-time vs. batch:** v1 batch (aligns with portfolio demo); streaming adapter in architecture (R-06).
3. **Vendor model drift:** Section VII third-party monitoring — separate ingestion path for vendor score distributions?
4. **Re-tiering automation:** When immaterial model exposure crosses threshold, auto-escalate tier — confirm UX in R-10.
5. **Champion-challenger trigger:** Define whether drift Red auto-promotes challenger — defer to R-06/R-10.
