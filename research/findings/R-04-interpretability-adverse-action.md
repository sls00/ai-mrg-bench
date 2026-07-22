# R-04 — Interpretability → Adverse-Action Pipeline

**Ticket:** R-04  
**Session:** 2  
**Status:** Complete  
**Research date:** 2026-07-20  
**Depends on:** R-03 (feature/proxy context)

---

> **Erratum (2026-07-22, R-12/R-14 close-out):** This document's Executive Summary, §2, §5, §9, and §10 originally cited a since-unverified CFPB circular numbered "2026-03" as authority for the translation-methodology requirement below. A dedicated primary-source search (`research/findings/R-12-circular-2026-03-primary-verification.md`) found no such circular on CFPB.gov, in CFPB's Newsroom archive, or in the Federal Register; the only located secondary source (a July 9, 2026 trade-press article) is itself contradicted by CFPB's own indexes and is treated as a false secondary (`research/findings/R-14-r12-r13-closeout-amendment-proposal.md` §3.1). The citation has been removed throughout this document. **The design is unaffected:** the translation-methodology artifact remains anchored in the binding statute/regulation (ECOA §701(d), Reg B §1002.9) plus CFPB's historical Circular 2022-03 and 2023-03 interpretive positions — both formally withdrawn May 12, 2025 (CFPB "Withdrawn Guidance" index) but still persuasive as interpretive history. See R-12 and R-14 for full verification detail.

---

## 1. Executive summary

**Recommendation:** Use **SHAP (TreeSHAP primary, KernelSHAP fallback)** as the core attribution engine for tabular credit models, with a **mandatory four-stage translation pipeline** that produces a **documented mapping methodology artifact** aligned with Reg B §1002.9 and CFPB's historical adverse-action interpretive guidance (see erratum above). LIME is supported only as an optional secondary method with **stability validation** (not default). Native interpretable models (WOE scorecards, logistic regression) use **coefficient-based attribution** as the primary path, with SHAP as cross-check.

**Differentiator (R-01 gap):** No identified competitor exports an auditable factor→reason translation methodology as a first-class artifact. The Workbench should generate this as a versioned, hash-chained document bound to model version.

---

## 2. Regulatory requirements (stable post–R-02)

| Requirement | Source | Status |
| ----------- | ------ | ------ |
| Specific principal reasons for each adverse action | ECOA §701(d); Reg B §1002.9 | ✅ Unchanged |
| Reasons must relate to factors **actually considered or scored** | Reg B commentary; Circular 2023-03 | ✅ |
| Cannot use closest checklist reason if inaccurate | Circular 2023-03 | ✅ |
| Cannot rely on model complexity as defense | Circular 2022-03 | ✅ |
| Post-hoc explanations must be **validated for accuracy** | Circular 2022-03 | ✅ |
| **Document translation methodology** for fair-lending reviewer validation | Reg B §1002.9; historical Circular 2022-03/2023-03 practice | ⚠ Reframed — see erratum above; not a distinct circular requirement |

**Key Circular 2022-03 holding (primary ✅):**

> "While some creditors may rely upon various post-hoc explanation methods, such explanations approximate models and creditors must still be able to validate the accuracy of those approximations, which may not be possible with less interpretable models."

**Circular 2023-03 insufficiency examples (primary ✅):**
- "insufficient projected income" insufficient if real driver was profession
- "purchasing history" insufficient for credit-line reduction — must disclose establishment type, location, goods
- Sample form checklist is **not** automatically sufficient

**Design intent (superseded citation — see erratum above):** The translation-methodology artifact requirement below is *not* sourced to a distinct CFPB circular. It is Workbench design practice, motivated by the historical Circular 2022-03/2023-03 interpretive positions (validated post-hoc explanations; specific, non-checklist reasons) and grounded directly in the binding Reg B §1002.9 specific-reasons requirement.

---

## 3. Interpretability approach comparison

| Method | Strengths | Weaknesses | Workbench role |
| ------ | --------- | ---------- | -------------- |
| **TreeSHAP** | Exact for tree ensembles (XGBoost/LightGBM/RF); fast; consistent; additive | Model-type limited | **Default** for tree models |
| **KernelSHAP** | Model-agnostic | Slow; sampling variance | Fallback for non-tree `.predict_proba()` |
| **Linear coefficients** | Native for logistic/scorecard; directly auditable | Not available for black-box | **Primary** for GLM/scorecard models |
| **LIME** | Model-agnostic; intuitive local linear | **Unstable** across runs; local approximation ≠ actual model | Optional secondary with stability gate |
| **Integrated Gradients** | Deep learning standard | Overkill for v1 tabular credit demo | Defer (LLM/agent path, choice B) |
| **Partial dependence** | Global behavior insight | Not individual-level; not sufficient for §1002.9 | Supplementary only |

### 3.1 Why SHAP over LIME (decision)

| Criterion | SHAP | LIME |
| --------- | ---- | ---- |
| Per-applicant consistency | High (deterministic given fixed background) | Low (random perturbation sampling) |
| Additive property | Yes — contributions sum to prediction | No |
| Regulatory fit | Maps to "principal reasons" ranking | Requires stability validation per Circular 2022-03 implication |
| Industry adoption | Dominant in credit ML practice ⚠ | Common but flagged as unstable ⚠ |

**Decision:** SHAP default; LIME opt-in with `stability_cv_threshold` gate (recommend: top-3 reason overlap ≥ 90% across 50 runs).

### 3.2 Model-type routing

```
IF model.type IN (XGBClassifier, LGBMClassifier, RandomForest, DecisionTree):
    attribution = shap.TreeExplainer
ELIF model.type IN (LogisticRegression, LinearScorecard):
    attribution = coefficients × (feature_value - reference)
ELIF model.supports_predict_proba:
    attribution = shap.KernelExplainer(background_sample=100)
ELSE:
    REJECT — cannot produce validated adverse-action reasons
```

---

## 4. Adverse-action translation pipeline (core design)

### Stage 1 — Per-applicant attribution

**Input:** Applicant feature vector `x`, trained model `f`, decision threshold  
**Output:** Ranked list of feature contributions to adverse outcome

```python
# Conceptual
shap_values = explainer.shap_values(x)
contributions = rank_by_negative_contribution(shap_values, top_k=4)
# top_k=4: Reg B requires "principal" reasons (typically 1-4)
```

**Rules:**
- Compute at **inference time** per applicant (not global feature importance)
- For credit scoring systems: Official Interpretation permits disclosing factor without explaining creditworthiness relationship (12 CFR 1002, comment 9(b)(2)-4) ✅
- Log raw SHAP values, ranked features, and model version

### Stage 2 — Feature → factor description mapping

**Input:** Ranked feature names + values + SHAP magnitudes  
**Output:** Specific factor descriptions (not checklist codes)

| Raw feature | Insufficient (checklist) | Sufficient (specific) |
| ----------- | ------------------------ | --------------------- |
| `bureau_trades_90d_past_due` | "delinquent past or present credit obligations" | "number of trades 90+ days past due in last 24 months" |
| `utilization_ratio` | "unable to verify credit references" | "revolving credit utilization exceeds 80%" |
| `employment_length_months` | "insufficient length of employment" | "employment history less than 12 months" |

**Mapping table structure (versioned artifact):**

```yaml
mapping_methodology_v1:
  model_id: "german-credit-xgb-v1.2"
  created: "2026-07-20"
  mappings:
    - feature: EXT_SOURCE_2
      factor_description: "external credit score below acceptable threshold"
      reg_b_sample_code: null  # no accurate checklist match — use free text
      specificity_test: pass
    - feature: AMT_INCOME_TOTAL
      factor_description: "income insufficient for requested obligation"
      reg_b_sample_code: null
  rules:
    - "Never map to checklist code unless factor accurately describes scored variable"
    - "Disclose actual data source (bank references vs credit references)"
    - "For engineered features, decompose to consumer-understandable components"
```

### Stage 3 — Fidelity validation

**Purpose:** Satisfy Circular 2022-03 requirement to validate post-hoc explanation accuracy.

| Test | Method | Pass criterion |
| ---- | ------ | -------------- |
| **Rank stability** | Re-run SHAP on same input | Top-k features identical |
| **Perturbation fidelity** | Remove top feature, re-score | Prediction moves in expected direction |
| **Surrogate agreement** | Compare SHAP-ranked vs. actual scorecard points (if scorecard) | Rank correlation ≥ 0.8 |
| **Sample audit** | Human review of N=50 adverse decisions | ≥ 95% reasons judged accurate |
| **LIME stability** (if used) | 50 LIME runs per applicant | Top-3 Jaccard overlap ≥ 0.9 |

**Output:** `fidelity_validation_report.json` bound to model version.

### Stage 4 — Consumer-facing reason generation + audit record

**Input:** Validated factor descriptions  
**Output:**
1. Adverse action notice text (up to 4 principal reasons)
2. Audit log entry per FINOS AIR-DET-021 Tier 2:
   - Input features (hashed or tokenized for demo)
   - Raw attribution values
   - Mapped factor descriptions
   - Mapping methodology version ID
   - Validator sign-off slot (human review for Tier 2+)

```json
{
  "decision_id": "uuid",
  "applicant_ref": "hash",
  "model_version": "german-credit-xgb-v1.2",
  "decision": "adverse",
  "principal_reasons": [
    {"rank": 1, "feature": "checking_status_A12", "description": "insufficient funds in checking account", "shap_value": -0.34},
    {"rank": 2, "feature": "credit_duration", "description": "requested loan term exceeds policy limit for credit profile", "shap_value": -0.21}
  ],
  "mapping_methodology_id": "mapping_methodology_v1",
  "fidelity_validation_id": "fidelity_report_2026-07-20",
  "reg_b_compliance_checks": {
    "specificity": "pass",
    "checklist_avoidance": "pass",
    "factor_actually_scored": "pass"
  }
}
```

---

## 5. Documented translation methodology artifact (Reg B §1002.9)

This is a **standalone, versioned document** — not embedded in code comments. It must be independently reviewable by a fair-lending examiner.

### Required sections

1. **Purpose and scope** — which models, which decision types (denial, counteroffer, unfavorable terms)
2. **Attribution method** — SHAP variant, background dataset, any approximations
3. **Feature inventory** — complete list of model inputs with business definitions
4. **Mapping rules** — feature → factor description logic, including handling of:
   - Engineered/composite features
   - Alternative data sources
   - Non-intuitive ML relationships (permitted per Reg B Official Interpretation)
   - Features with no checklist equivalent (use free text per 2023-03)
5. **Validation protocol** — fidelity tests from Stage 3 with pass/fail criteria
6. **Change control** — how mapping updates are approved when model retrains
7. **Known limitations** — e.g., KernelSHAP sampling variance, proxy features

### Workbench output format

- `translation_methodology_v{N}.md` — human-readable
- `translation_methodology_v{N}.json` — machine-readable (for audit log binding)
- SHA-256 hash stored in tamper-evident audit log (feeds R-06)

**Differentiator:** Export as OCC 2026-13 validation report appendix + standalone examiner packet.

---

## 6. Integration with R-03 bias module

| Integration point | Behavior |
| ----------------- | -------- |
| Proxy-risk features | If feature flagged in proxy battery, adverse-action reason must **not** obscure proxy nature — disclose specific factor, not broad bucket |
| Protected-class columns | Hard reject as model input; if present in dataset for validation only, exclude from attribution |
| FHA/state overlay | Same pipeline; additional review flag if adverse reasons correlate with proxy-protected class |

---

## 7. Alternatives considered and rejected

| Alternative | Why rejected |
| ----------- | ------------ |
| Global feature importance only | Circular 2022-03 requires **individual-level** reasons |
| Checklist auto-selection | Circular 2023-03 explicitly prohibits closest-checklist if inaccurate |
| LIME as default | Instability incompatible with "specific and accurate" standard without heavy validation |
| LLM-generated reasons | Cannot guarantee mapping to actually-scored factors; violates validation requirement |
| Counterfactual-only explanations | Useful supplement but not sufficient alone for §1002.9 principal reasons |

---

## 8. Implications for Workbench

1. **Implement four-stage pipeline** as a named module: `adverse_action_translator` with SHAP core.
2. **Generate translation methodology artifact** as first-class versioned output — primary R-01 differentiation.
3. **Route by model type** — TreeSHAP for XGBoost demo model; coefficient path for scorecard comparison.
4. **Bind audit records** to FINOS AIR-DET-021 Tier 2 (explicit reasoning logged before decision output).
5. **Include fidelity validation** in every validation run — not optional.
6. **Demo narrative:** Show side-by-side insufficient vs. sufficient reason mapping using Circular 2023-03 examples.
7. **Do not claim legal compliance** — claim "structured evidence package for examiner review."
8. **LLM/agent extensibility (choice B):** Defer gen-AI attribution to FINOS Tier 2+ interface; document limitation per mi-21 caveat for hidden-reasoning models.

---

## 9. Sources

| ID | Source | Tier | Status | Used for |
| -- | ------ | ---- | ------ | -------- |
| S-18 | CFPB Circular 2022-03 (primary PDF + web) | 1 | ✅ | Black-box holding, validation requirement |
| S-31 | CFPB Circular 2023-03 PDF | 1 | ✅ | Specificity, checklist insufficiency |
| S-32 | CFPB Innovation Spotlight (AI/ML adverse action) | 1 | ✅ | Official Interpretation flexibility |
| S-33 | Superseded citation — see erratum above; downgraded per R-12/R-14 (no primary source found) | 1 | ❌ | Not used as authority; translation methodology anchored in S-18/S-31/S-32/S-34 instead |
| S-34 | Reg B §1002.9 + Official Interpretation | 1 | ✅ | Statutory anchor |
| S-35 | SHAP (Lundberg & Lee 2017) / shap Python library | 2 | ✅ | Attribution method |
| S-36 | BrightCloud ECOA explainability analysis | 2 | ⚠ | SHAP vs LIME stability |
| S-37 | CFPI interpretable algorithms post | 2 | ⚠ | LIME/SHAP industry context |

---

## 10. Open questions

1. ~~Primary-source spot-check of the unverified "2026-03" circular claim~~ — ✅ **Resolved (R-12/R-14):** no such circular exists on CFPB.gov or the Federal Register; see erratum above.
2. **FCRA adverse action (credit score factors):** Separate from Reg B; v1 scope is Reg B only — confirm no FCRA key-factors module needed.
3. **Counterfactual reasons:** EU/consumer-friendly supplement; not required for US §1002.9 — defer to v2.
4. **Multi-model ensembles:** Attribution aggregation across champion/challenger — R-06 architecture question.
5. **Non-English notices:** Out of v1 scope.
