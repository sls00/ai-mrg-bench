# R-03 — Bias/Fair-Lending Statistical Methodology

**Ticket:** R-03  
**Session:** 2  
**Status:** Complete  
**Research date:** 2026-07-20  
**Depends on:** R-01 (gap confirmation), R-02 (Reg B scope correction)

---

## 1. Executive summary

**Recommendation:** Implement a **three-layer statistical battery** with explicit **regulatory-framing toggles** that reflect the post–July 2026 Reg B landscape:

| Layer | Tests | Primary regulatory use (post–July 2026) |
| ----- | ----- | --------------------------------------- |
| **A. Outcomes analysis** | Adverse Impact Ratio (four-fifths), selection-rate parity, SMD on continuous outcomes | FHA disparate impact ✅; state-law overlays ✅; OCC 2026-13 outcomes analysis ✅; **not** federal ECOA disparate-impact compliance ❌ |
| **B. Error-rate parity** | FPR, FNR, equalized odds gaps (Aequitas pattern) | Internal risk management + EU AI Act Art. 10 + NIST MEASURE 2.11 |
| **C. Proxy-discrimination** | Feature↔protected-class correlation, predictive association, proxy-risk ranking | **Primary federal ECOA concern** alongside disparate treatment ✅ |

**Proxy strategy:** BISG (Bayesian Improved Surname Geocoding) per CFPB examination methodology — surname + geocode → probabilistic race/ethnicity — with 2020 Census DHC update (April 2024). Protected-class data must **never** enter the scoring model; it is used only in the validation battery via proxy or held-out demographic fields.

**Demo dataset recommendation:** **German Credit (UCI)** as v1 primary (small, documented, has `sex`); **Home Credit Default Risk (Kaggle)** as scale/realism secondary; optional **HMDA** slice for FHA overlay demo. Compose **Fairlearn** (metrics) + **Aequitas** (audit report structure), do not rebuild.

---

## 2. Regulatory framing (post–R-02)

R-02 verified that effective **July 21, 2026**, Reg B eliminates federal ECOA disparate-impact liability but **preserves**:

- Disparate treatment (including intentional proxy use)
- Adverse-action notice requirements (unchanged)
- CFPB Circular 2026-03 documentation requirements (unchanged)
- FHA disparate impact (Supreme Court *Inclusive Communities*)
- State fair-lending laws (ticket R-08)

The Workbench bias module must therefore expose **jurisdiction overlays** as configuration, not hard-coded assumptions:

```
federal_ecoa_mode: "proxy_discrimination"   # default post-July 2026
overlay_fha_disparate_impact: true|false
overlay_state_law: CO|CA|NY|none            # R-08 will detail
```

**Messaging discipline (from R-02):** Do not claim "ECOA disparate-impact compliance." Do claim: proxy-risk analysis, FHA/state overlay testing, OCC outcomes analysis, EU/NIST documentation.

---

## 3. Recommended statistical battery

### 3.1 Layer A — Outcomes analysis (selection rates)

| Metric | Definition | Default threshold | Notes |
| ------ | ---------- | ----------------- | ----- |
| **Adverse Impact Ratio (AIR)** | (selection rate of protected group) / (selection rate of reference group) | < 0.80 → flag for review; 0.80–0.90 → monitor; ≥ 0.90 → satisfactory | EEOC four-fifths rule of thumb ✅; **not a legal safe harbor** ⚠ |
| **Selection rate gap** | Absolute difference in approval rates | Institution-defined | Pair with statistical significance (Fisher's exact / chi-square) |
| **Standardized Mean Difference (SMD)** | (μ_protected − μ_reference) / σ_pooled on continuous outcomes (score, APR, limit) | \|SMD\| > 0.10 → monitor; \|SMD\| > 0.30 → practically significant flag | Industry practitioner threshold ⚠; direction must be pre-specified |

**Implementation:** Fairlearn `MetricFrame` for AIR/selection_rate; Aequitas `Bias()` for disparity ratios with configurable reference group and 0.8 fairness threshold.

**Cross-framework mapping:**
- OCC 2026-13 §V Outcomes Analysis — "comparison of model outputs to corresponding outcomes" ✅
- NIST AI RMF MEASURE 2.11 — fairness evaluated and documented ✅
- EU AI Act Art. 10 — bias examination for direct and proxy discrimination ✅

### 3.2 Layer B — Error-rate parity (classification quality by group)

Credit underwriting is a **punitive** decision context (denial harms applicant). Per Aequitas guidance, prioritize:

| Metric | When to use | Threshold |
| ------ | ----------- | --------- |
| **False Positive Rate (FPR) parity** | Denial/adverse decisions — wrongly denying creditworthy applicants | Disparity ratio < 0.8 or > 1.25 → flag (Aequitas default) |
| **False Negative Rate (FNR) parity** | Approval decisions — wrongly approving defaulters | Secondary; monitor for safety |
| **Equalized odds difference** | Holistic error parity | \|difference\| > institution tolerance |

Fairlearn metrics: `false_positive_rate`, `false_negative_rate`, `equalized_odds_difference`.

### 3.3 Layer C — Proxy-discrimination battery (elevated federal priority)

Post–July 2026, this is the **primary federal ECOA statistical concern** when protected-class data cannot be collected at application (non-mortgage) or is held out of the model.

| Test | Method | Output artifact |
| ---- | ------ | --------------- |
| **Feature-proxy correlation** | Pearson/Spearman between each model input and BISG-derived protected-class probability | Proxy correlation matrix |
| **Predictive association** | Train auxiliary classifier: feature → protected class; report AUC/accuracy | Features that reconstruct protected class |
| **Model reliance on proxy features** | SHAP global importance cross-referenced with proxy-correlation ranking | Proxy-risk feature list |
| **Outcome conditioning** | Regression/control for legitimate factors; test residual association with proxy | Residual disparity report |

**Reg B final rule commentary (91 FR 21620):** Commenters requested confirmation that creditors may still use proxy analysis to assess demographic makeup; industry expects proxy analysis to continue for FHA/state obligations and business strategy. ✅ Verified in Federal Register preamble ⚠ (secondary law-firm corroboration in R-02).

**Caution (open question):** Algorithmic debiasing/LDA techniques that explicitly use protected-class data to re-weight outcomes may create **intentional proxy discrimination** exposure under the revised intent-based Reg B framing. Workbench should **detect and flag** such patterns but not prescribe debiasing mitigations in v1. See Pace Analytics analysis ⚠.

### 3.4 Disparate Impact Analysis (DIA) — reframed scope

Traditional DIA (outcomes → business necessity → less discriminatory alternative) remains the **FHA and state-law** framework. For federal ECOA post-July 2026:

- Run DIA battery when `overlay_fha_disparate_impact=true` or state overlay enabled
- Document as "FHA/state outcomes analysis" not "ECOA disparate-impact test"
- Include regression-based outcomes modeling (OCC examination pattern) as optional advanced tier

---

## 4. Protected-class data handling

### 4.1 Model training constraint

**Rule:** Protected characteristics (race, color, religion, national origin, sex, marital status, age, receipt of public assistance, exercise of CCPA rights) must **not** be model inputs. This is a hard validation gate at ingestion.

### 4.2 BISG proxy methodology (recommended)

**Source:** CFPB `cfpb/proxy-methodology` GitHub repository ✅

| Component | Detail |
| --------- | ------ |
| **Method** | Bayesian Improved Surname Geocoding — combines surname probabilities + census block-group demographics |
| **Output** | Probabilistic race/ethnicity assignment (not deterministic label) |
| **2024 update** | April 2024: 2020 Census DHC (Table P11) at block group, tract, and ZIP levels ✅ |
| **Validation** | CFPB 2014 report: BISG correlates more highly with self-reported race than surname-only or geography-only ✅ |
| **Limitations** | Lower accuracy for African American and Hispanic populations; less accurate in diverse neighborhoods ⚠ (Asurity secondary) |

**Workbench implementation:**
1. Accept applicant `surname` + `zip` or `census_block_group` in validation dataset (not scoring features)
2. Run BISG proxy generation (Python port of CFPB Stata logic, or invoke published code)
3. Use probabilistic weights in outcomes analysis (not binary race labels)
4. Document proxy methodology version (2010 vs 2020 Census) in audit artifact

**Alternatives (document but defer):**
- Surname-only / geography-only (less accurate; useful as sensitivity check)
- BIFSG (Bayesian Improved First Name and Surname Geocoding) — marginal accuracy gain ⚠
- ML-based proxy (less transparent; examiners prefer replicable public-data methods per industry practice ⚠)

### 4.3 Mortgage vs. non-mortgage

| Product | Protected-class source | Proxy needed? |
| ------- | --------------------- | ------------- |
| **Mortgage (HMDA-reportable)** | Self-reported HMDA fields (with known quality caveats) | Optional — use HMDA directly for outcomes; BISG as cross-check |
| **Non-mortgage (auto, card, personal)** | Generally not collected at application | **BISG required** for race/ethnicity outcomes analysis |

---

## 5. Demo dataset strategy

### 5.1 Primary: German Credit (UCI Statlog)

| Attribute | Value |
| --------- | ----- |
| **Source** | UCI ML Repository / Kaggle mirror ✅ |
| **Rows** | 1,000 |
| **Protected attribute** | `sex` (and `age` as secondary) |
| **Target** | Credit risk (good/bad) |
| **Why primary** | Small, fast, well-documented, widely used in Fairlearn/AIF360 tutorials; enables matched-pair and AIR demos without BISG complexity |
| **Limitation** | German data, not US lending; no race/ethnicity field |

### 5.2 Secondary: Home Credit Default Risk (Kaggle)

| Attribute | Value |
| --------- | ----- |
| **Source** | Kaggle `home-credit-default-risk` ✅ |
| **Rows** | 307,511 (application_train) |
| **Protected attribute** | None native — inject BISG proxy from `NAME_FAMILY` + region fields, or use `CODE_GENDER` as sex proxy only |
| **Why secondary** | Realistic scale, multi-table structure, industry-standard for PD model demos; 2024 "Model Stability" competition reinforces drift narrative (R-05) |
| **Limitation** | Large download; no US race/ethnicity without proxy |

### 5.3 FHA overlay option: HMDA public data

| Attribute | Value |
| --------- | ----- |
| **Source** | CFPB/FFIEC HMDA public LAR ✅ |
| **Protected attributes** | Race, ethnicity, sex (self-reported) |
| **Why** | Enables FHA disparate-impact overlay demo with real protected-class fields |
| **Limitation** | Mortgage-only; large; requires geographic filtering for demo subset |

### 5.4 Synthetic supplement

| Source | Rows | Use case |
| ------ | ---- | -------- |
| **Fairlearn UCI Default Taiwan** (semi-synthetic `Interest` feature) | 30,000 | Tutorial-faithful bias introduction; adds correlated disparity ⚠ |
| **alerterra/credit_scoring_fairness** (HuggingFace) | 102 | Embedded bias scenarios for regression testing; too small for statistical power ❌ for primary demo |
| **Workbench-generated synthetic** | Configurable | Matched-pair counterfactual testing per WealthSchema playbook ⚠ — build in R-10 if needed |

### 5.5 Recommended demo path (feeds R-10)

```
Phase 1: German Credit → full battery (AIR, SMD, FPR parity, SHAP proxy check on sex)
Phase 2: Home Credit subset (10k rows) → BISG proxy pipeline + scale demo
Phase 3 (optional): HMDA NY slice → FHA overlay toggle demonstration
```

---

## 6. OSS composition (do not rebuild)

| Library | Role in Workbench | Integration point |
| ------- | ----------------- | ----------------- |
| **Fairlearn** | Core metrics (`MetricFrame`, selection_rate, demographic_parity_difference, equalized_odds) | `bias_battery.py` metrics engine |
| **Aequitas** | Audit report structure, disparity ratios, fairness criteria assessment | Report generator / PDF export |
| **CFPB proxy-methodology** | BISG reference implementation | `proxy_generator.py` |
| **SHAP** | Feature attribution for proxy-risk cross-reference (feeds R-04) | Shared with interpretability module |

**Gap filled (R-01):** No competitor ships FINOS ri-16 statistical mitigation; Workbench battery is the differentiation.

---

## 7. Workbench module design (actionable)

### 7.1 Inputs

```yaml
validation_run:
  model: sklearn-compatible .predict() / .predict_proba()
  dataset: labeled CSV/Parquet
  decision_column: approval_binary | score_continuous
  protected_attributes:
    - name: sex
      source: direct | bisg_proxy | hmda
      reference_group: male
  regulatory_frame:
    federal_ecoa: proxy_discrimination
    fha_overlay: false
    state_overlay: none
  thresholds:
    air_review: 0.80
    air_monitor: 0.90
    smd_practical: 0.30
    fpr_disparity: 0.80
```

### 7.2 Outputs (per validation run)

1. **Bias Battery Summary** — pass/flag/review per metric × protected class
2. **Proxy Risk Report** — ranked features by protected-class association
3. **Regulatory Frame Statement** — which tests apply under which jurisdiction overlay
4. **Audit log entry** — FINOS mi-5 acceptance testing evidence; hashes inputs/outputs

### 7.3 Report sections (OCC 2026-13 alignment)

Maps to **§V Outcomes Analysis** and cross-framework row in foundation §3.6.

---

## 8. Implications for Workbench

1. **Build the three-layer battery** (outcomes + error-rate + proxy) as a single orchestrated module with jurisdiction toggles — this is the primary statistical differentiator confirmed by R-01 gap analysis.
2. **Default post–July 2026 framing** to proxy-discrimination primary; keep AIR/four-fifths as FHA/state/internal-risk metrics with explicit labeling.
3. **Use German Credit for v1 demo**; architect BISG proxy pipeline for Home Credit scale demo in R-10.
4. **Compose Fairlearn + Aequitas**; output Aequitas-shaped disparity tables in validation report.
5. **Hard gate:** reject models that include protected-class columns as features.
6. **Do not implement algorithmic debiasing mitigations in v1** — detection and documentation only; debiasing raises Reg B proxy-discrimination questions (open).
7. **EU secondary:** Art. 10 bias examination satisfied by same battery with documentation layer; no separate EU metric set needed for v1.

---

## 9. Sources

| ID | Source | Tier | Status | Used for |
| -- | ------ | ---- | ------ | -------- |
| S-19 | CFPB proxy-methodology GitHub + 2014 report | 1 | ✅ | BISG methodology |
| S-20 | Federal Register 91 FR 21620 preamble (proxy analysis commentary) | 1 | ✅ | Proxy analysis still permitted |
| S-21 | EEOC Uniform Guidelines 4/5ths rule Q&A | 1 | ✅ | AIR threshold origin |
| S-22 | Fairlearn credit loan decisions tutorial | 2 | ✅ | Metric patterns |
| S-23 | Aequitas documentation (dssg.github.io/aequitas) | 2 | ✅ | FPR parity, disparity ratios |
| S-24 | UCI German Credit dataset | 2 | ✅ | Demo dataset |
| S-25 | Kaggle Home Credit Default Risk | 2 | ✅ | Scale demo dataset |
| S-26 | ACM FAccT "four-fifths rule is not disparate impact" | 2 | ⚠ | AIR is screening not legal test |
| S-27 | OCC Comptroller's Handbook Fair Lending | 1 | ⚠ | Examination statistical modeling |
| S-28 | Asurity Advisors BISG overview | 2 | ⚠ | Industry practice corroboration |
| S-29 | Pace Analytics Reg B LDA/proxy post | 2 | ⚠ | Debiasing risk flag |
| S-30 | HuggingFace alerterra/credit_scoring_fairness | 3 | ⚠ | Synthetic test data |

---

## 10. Open questions

1. **BISG Python port:** CFPB publishes Stata; confirm maintained Python implementation or port scope at build time.
2. **Debiasing boundary:** Whether Workbench should ever recommend mitigation algorithms (Fairlearn reductions) or stay detection-only — legal risk under revised Reg B intent test.
3. **State overlays:** Specific metrics required by CO/CA/NY — deferred to R-08.
4. **HMDA race field quality:** Known reporting inconsistencies; document limitations in FHA overlay demo.
5. **Scorecard vs. ML:** For natively interpretable scorecards, proxy battery still applies but SHAP layer may be replaced by coefficient analysis (R-04 handoff).
