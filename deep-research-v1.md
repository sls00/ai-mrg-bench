# AI Model Risk & Governance Workbench — Deep Research v1

**Status:** Research complete (Sessions 1–6)  
**Date:** 2026-07-21  
**Audience:** Build phase — risk/compliance/auditor persona; portfolio-scale demo  
**Foundation (read-only):** `RESEARCH_FOUNDATION_v2.md`  
**Finding files:** `research/findings/R-01` through `R-10`

---

## 1. Executive summary & top recommendations

### 1.1 What to build

Ship an **open, model-agnostic validation workbench** for **traditional ML credit models** that ingests a deployed model + labeled dataset and runs a structured MRM lifecycle: **tiering → validation → bias/proxy testing → adverse-action translation → drift monitoring → audit log → OCC seven-section report**. The user is a **risk/compliance/auditor**, not a lender. v1 is **not** an enterprise GRC platform, lending system, or gen-AI MRM product.

**Compose, don't rebuild:** Fairlearn, Aequitas, SHAP, scipy PSI — differentiate on **structure, regulatory specificity, and evidence chain**, not raw metric novelty.

### 1.2 Primary differentiators (build first, lead messaging)

| # | Differentiator | Module | Evidence |
| - | -------------- | ------ | -------- |
| **1** | Post–July 2026 **proxy-discrimination test suite** + jurisdiction overlays (federal, FHA, CO/CA/NY) | `bias_battery` | ✅ R-02 verified; R-01 gap #4; FINOS ri-16 statistical gap |
| **2** | **OCC 2026-13 literal seven-section** validation report with hash-bound appendices | `report_generator` | ✅ R-01 gap #2; vendors still on SR 11-7 / three-pillar framing |
| **3** | **Documented SHAP → Reg B §1002.9 adverse-action translation methodology artifact** (versioned, hash-bound; encodes historical CFPB Circular 2022-03 / 2023-03 interpretive positions — withdrawn May 12, 2025 — plus Innovation Spotlight practice notes) | `adverse_action_translator` | ✅ R-04 design; ❌ no primary source found for a distinct "2026-03" circular (R-12); market gap vs Holistic/Fiddler attribution-only (R-01) |

### 1.3 Secondary differentiators (v1 build, selective demo)

- FINOS **mi-21 Tier 1–2** hash-chained audit log cited by control ID (`audit_log`)
- Materiality-tiered drift escalation T1/T2/T3 traffic-light (`drift_monitor` + `materiality_engine`)
- Vendor/black-box ingest via `VendorModelAdapter` (OCC §VII)
- Open statistical bias module filling FINOS catalogue gap

### 1.4 v1 scope lock

| In scope | Out of scope (defer) |
| -------- | -------------------- |
| sklearn ingest + CSV; German Credit demo | Enterprise GRC, SaaS multi-tenancy |
| OCC I–VII report (Markdown + optional PDF) | Gen-AI/agentic MRM regulatory completeness |
| Three-layer bias battery + `regulatory_frame` toggles | FCRA key-factors engine, algorithmic debiasing |
| SHAP four-stage adverse-action pipeline | Consumer-facing disclosure generation |
| PSI/KS drift + tier escalation | Real-time Kafka streaming, 50-state overlays |
| SQLite hash-chained audit; CLI + Python SDK | Full FINOS Tier 3 crypto trail (design doc only) |
| State overlays CO / CA / NY (CA demo toggle) | ONNX/PMML ingest (v1.1), Postgres (v2) |

### 1.5 Build order (actionable)

| Phase | Slice | Exit criterion |
| ----- | ----- | -------------- |
| **P0** | Ingest → tier → federal `bias_battery` → report §I–VI → audit | `workbench validate run` + `audit verify-chain` PASS |
| **P1** | + adverse-action translator + Appendix A methodology | `translation_methodology_v1.json` hash-bound |
| **P2** | + drift snapshot + T3 escalation (canonical demo) | §V.3 + `drift.event`; **CI gate minimum** |
| **P3** | + CA state overlay second run | Side-by-side §II diff; `admt_risk_assessment_summary.json` |
| **P4** | Home Credit + BISG (README/notebook only) | Documented architecture; not blocking |

**Canonical demo:** `workbench validate run --config configs/german_credit_full.yaml` → OCC report + appendices A–E → `workbench audit verify-chain` PASS.

### 1.6 Regulatory emphasis

| Priority | Frameworks |
| -------- | ---------- |
| **Primary** | US federal — OCC 2026-13 ✅, ECOA/Reg B ✅ (post–July 2026 proxy framing) |
| **Secondary** | EU AI Act, FINOS AIR |
| **Tertiary** | State law — CO SB 26-189, CA CPPA ADMT, NY DFS CL 7 (insurance) |

### 1.7 Messaging discipline

**Do claim:**
- Produces **validation evidence** structured for OCC 2026-13 seven-section independent review
- **Proxy-discrimination statistical battery** aligned with post–July 2026 federal ECOA framing
- **Documented factor→reason mapping methodology** for examiner/reviewer validation (Reg B §1002.9)
- Audit trail implements **FINOS AIR-DET-021 Tier 1–2** controls by ID
- Jurisdiction overlays for **FHA, Colorado, California ADMT, and NY DFS insurance** testing frames

**Do not claim:**
- "Ensures ECOA disparate-impact compliance" (federal theory removed ✅ S-15)
- "California DFPI certified" (authority is **CPPA/CCPA ADMT** ✅ S-54)
- "NY DFS lending compliance" (CL 7 is **insurance**; lending bill A773B pending ✅ S-59)
- "OCC 2026-13 compliant" (guidance is non-enforceable; no safe harbor)
- "EU AI Act conformity assessment complete" (deadline Dec 2027)
- "Gen-AI / agentic MRM compliant" (explicitly out of OCC scope)
- "Replaces enterprise MRM platform" (ValidMind/SAS territory)
- "Satisfies current CFPB guidance numbered 2026-03" (no such document exists — R-12)
- "Implements current non-withdrawn CFPB circular guidance on AI adverse action" (Circular 2022-03/2023-03 withdrawn May 12, 2025)

**Report §I disclaimer (embed in every report):**

> This validation report is generated by an analytical workbench for model risk and fair-lending **review support**. It does not constitute legal advice, a regulatory filing, or a determination of compliance with any applicable law.

---

## 2. Competitive landscape synthesis (R-01)

### 2.1 Market structure

The market splits into four layers — frequently conflated in vendor marketing:

| Layer | Role | Examples | Workbench relationship |
| ----- | ---- | -------- | ---------------------- |
| **A. MRM lifecycle** | Inventory, validation workflows, documentation | ValidMind, SAS MRM, Solytics, ModelOp | Closest analog — enterprise-priced, not open validation engine |
| **B. AI governance / GRC** | Policy, multi-framework assessments, agent registry | Credo AI, IBM watsonx, ServiceNow, Truyo | Breadth over statistical depth |
| **C. Observability** | Drift, bias in production, LLM guardrails | Fiddler, Arthur AI | Strong post-deployment; weak pre-deployment validation reports |
| **D. OSS components** | Fairness metrics, SHAP, frameworks | Fairlearn, Aequitas, FINOS AIGF | **Build on top of** |

**Analyst signal:** Chartis 2024 MRM (30 vendors ⚠ S-01) + Gartner AI Governance MQ June 2026 (⚠ S-02 paywalled) confirm market convergence of MRM and AI governance. ValidMind is the strongest direct MRM competitor (Chartis leader all three quadrants ✅ S-03).

### 2.2 Comparison matrix (top 10)

| Product | OSS? | OCC/SR MRM | ECOA adverse action | Bias depth | Audit tier 3 | LLM/agent | Proof |
| ------- | ---- | ---------- | ------------------- | ---------- | ------------ | --------- | ----- |
| ValidMind | No | ✅ Strong | ❌ | ⚠ | ⚠ | ✅✅ | ✅✅ |
| SAS MRM | No | ✅ Strong | ❌ | ⚠ | ⚠ | ⚠ | ✅✅ |
| Solytics | No | ✅ SR 26-2 | ❌ | ✅ | ✅ | ⚠ | ⚠ |
| ModelOp | No | ✅ Templates | ❌ | ⚠ | ⚠ | ✅ | ✅ |
| Fiddler | No | ⚠ SR 11-7 | ⚠ SHAP only | ✅ prod | ⚠ | ✅✅ | ✅ |
| Holistic AI | No | ❌ | ⚠ | ✅✅ | ⚠ | ✅ | ✅ |
| Monitaur | No | ⚠ | ❌ | ⚠ | ✅✅ crypto | ✅ | ✅✅ |
| Credo AI | No | ❌ | ❌ | ⚠ | ⚠ | ✅ | ✅✅ |
| DataRobot | No | ✅ | ❌ | ⚠ | ⚠ | ✅ | ✅ |
| model-ledger | **Yes** | ⚠ profiles | ❌ | ❌ | ✅ events | ⚠ | ⚠ early |

Legend: ✅ explicit public evidence | ⚠ partial | ❌ not found

### 2.3 Commodity vs. gap

**Commodity (integrate, don't rebuild):** Model inventory tables, approval workflows, PSI dashboards, SHAP/LIME, Fairlearn/Aequitas metrics, EU AI Act checklists, GRC PDF export.

**Genuinely missing (Workbench opportunity):**

1. Unified model-agnostic validation engine (sklearn + labeled CSV → full battery)
2. OCC 2026-13 **seven-section** report generator (literal I–VII)
3. ECOA adverse-action translator + **Reg B §1002.9 documented translation methodology artifact**
4. Post–July 2026 **proxy-discrimination** suite as primary federal layer
5. FINOS **mi-21** tiered audit trail cited by control ID
6. FINOS **ri-16** statistical bias gap in AIGF catalogue
7. Open, inspectable, portfolio-scale end-to-end demo on public data

### 2.4 Competitive posture

**Do not compete** on enterprise GRC breadth (Credo, ServiceNow, IBM). **Do compete** on integrated validation depth at portfolio scale: tier → validate → bias/proxy → adverse-action → audit → seven-section report. **Compose** Fairlearn/Aequitas/SHAP; optionally integrate model-ledger inventory patterns in v2.

---

## 3. Regulatory updates (R-02, R-08)

### 3.1 Federal — Reg B July 2026 (R-02)

**VERIFIED ✅** — CFPB final rule (Federal Register **91 FR 21620**, effective **July 21, 2026** ✅ S-15):

| Change | Status | Workbench impact |
| ------ | ------ | ---------------- |
| Federal ECOA **disparate-impact** ("effects test") eliminated | ✅ | Do not claim disparate-impact compliance |
| **Discouragement** prohibition narrowed | ✅ | Out of v1 scope |
| **SPCP** restrictions for for-profit creditors | ✅ | Out of v1 scope |
| **Adverse-action notices** (§1002.9) | ✅ Unchanged | Core P1 module |
| "2026-03" circular translation methodology | ❌ Not operative — no primary source found (R-12) | Removed as authority; use Reg B §1002.9 + historical Circular 2022-03/2023-03 (withdrawn May 12, 2025) instead |
| **Proxy discrimination** + disparate treatment | ✅ Preserved | **Primary federal statistical frame** |
| **FHA** disparate impact | ✅ Unchanged | Optional `fha_overlay` toggle |

**Default federal config:**

```yaml
regulatory_frame:
  federal_ecoa: proxy_discrimination
  fha_overlay: false
  state_overlay: none
```

**Bias module reframing:** Layer A (AIR, selection rate) serves FHA, state overlays, and OCC outcomes analysis — **not** federal ECOA disparate-impact compliance. Layer C (proxy battery) is the **elevated federal ECOA concern**.

### 3.2 State overlays (R-08) — tertiary

| Overlay | Authority | Effective | Lending? | Statutory AIR/DIA? | Workbench artifact |
| ------- | --------- | --------- | -------- | ------------------ | ------------------ |
| **CO** | SB 26-189 ✅ S-52 | Jan 1, 2027 | ✅ Financial/lending | ❌ No statutory battery | Disclosure checklist; Layer A as "existing-law support" |
| **CA** | CPPA CCPA ADMT ✅ S-54 | Regs Jan 2026; compliance Jan 2027 | ✅ Financial/lending | ⚠ Risk assessment considers discrimination harms | `admt_risk_assessment_summary.json` |
| **NY** | DFS CL 7 (insurance) ✅ S-57 | July 2024 | ⚠ Insurance only | ✅ Proxy + 3-step DIA with AIR | Document-only for bank-lending demo |

**Corrections from foundation:**
- California ADMT rules are **CPPA/CCPA** (not DFPI standalone rulemaking) ✅ S-56
- FINOS ri-22 "California DFPI" reference is shorthand for California ADMT cluster ⚠
- NY **A773B** lending ADMT bill pending — not enacted ✅ S-59
- CA **AB 1018** disparate-impact ADS bill pending ✅ S-61

**P3 demo recommendation:** `state_overlay: CA` primary (tangible JSON export); `CO` as simpler checklist alternative.

---

## 4. Validation methodology (R-03, R-04, R-05)

### 4.1 Three-layer bias battery (R-03)

| Layer | Tests | Primary use (post–July 2026) |
| ----- | ----- | ---------------------------- |
| **A. Outcomes** | AIR (four-fifths), selection-rate gap, SMD | FHA ✅; state overlays ✅; OCC §V outcomes ✅; **not** federal ECOA DIA ❌ |
| **B. Error parity** | FPR, FNR, equalized odds (Aequitas pattern) | EU Art. 10; NIST MEASURE 2.11; internal risk |
| **C. Proxy-discrimination** | Feature↔protected correlation, auxiliary classifier AUC, SHAP cross-ref | **Primary federal ECOA** ✅ |

**Thresholds (defaults, configurable):**

| Metric | Flag |
| ------ | ---- |
| AIR | < 0.80 review; 0.80–0.90 monitor; ≥ 0.90 satisfactory ⚠ S-21 |
| SMD | \|SMD\| > 0.10 monitor; > 0.30 practically significant ⚠ |
| FPR disparity | < 0.8 or > 1.25 flag ⚠ S-23 |

**Protected-class rule:** Never in model features; validation-only in dataset with `source: direct | bisg_proxy | hmda`. Hard reject at ingest if protected attribute ∈ `feature_names_in_`.

**BISG proxy (Phase 2 / Home Credit):** CFPB methodology ✅ S-19; implement via `surgeo` ✅ S-50 with documented divergence from Stata reference.

**Detection-only:** No algorithmic debiasing in v1 — legal risk under post–July 2026 intent-based Reg B framing ⚠ S-29.

### 4.2 Adverse-action pipeline (R-04)

**Four-stage pipeline** → `translation_methodology_v{N}.json` artifact:

| Stage | Input → Output |
| ----- | -------------- |
| **1. Attribution** | Applicant features → TreeSHAP (default) / KernelSHAP / coefficients |
| **2. Factor mapping** | Feature names → specific factor descriptions (not checklist codes) |
| **3. Fidelity validation** | Perturbation tests, rank stability, N=50 human audit sample |
| **4. Consumer reasons + audit** | Up to 4 principal reasons; Tier-2 `adverse_action.*` events |

**Model routing:** TreeSHAP for tree ensembles; coefficients for GLM/scorecards; KernelSHAP fallback; **reject** if no validated attribution path.

**SHAP over LIME:** Deterministic, additive, industry-dominant ⚠ S-35; LIME opt-in with stability gate only.

**Regulatory anchors:** §1002.9 ✅ S-34 (statutory anchor); Circular 2022-03 ✅ S-18 and Circular 2023-03 ✅ S-31 (historical CFPB interpretive positions — formally withdrawn May 12, 2025, per CFPB's Withdrawn Guidance index; persuasive as interpretive history, not current guidance); CFPB Innovation Spotlight ✅ S-32. No primary source found for a distinct "2026-03" circular (R-12); S-33 downgraded to ❌ and not used as authority.

### 4.3 Drift detection & materiality escalation (R-05)

**Three drift classes:** population (PSI/CSI/KS), score stability, performance (AUC/Gini/Brier/ECE).

**PSI thresholds (Lewis heuristics ⚠ S-39):**

| PSI | Action |
| --- | ------ |
| < 0.10 | Green — log |
| 0.10–0.25 | Amber — investigate |
| ≥ 0.25 | Red — escalate per tier |

**Materiality tiers:**

| Tier | Exposure | Purpose | Cadence |
| ---- | -------- | ------- | ------- |
| T1 | < 1% | Non-regulatory | Quarterly |
| T2 | 1–10% | Business support | Monthly |
| T3 | > 10% or credit decisioning | Regulatory | Weekly + event-driven |

German Credit demo: **T3** (`exposure: 0.15`, `credit_decisioning`).

**T3 Red escalation:** Validator notification ≤ 10 days; re-validation scoping; §V.3 narrative. **Critical:** Red + FHA AIR < 0.80 → immediate suspension flag.

**Implementation:** scipy KS + custom numpy PSI (reject evidently for v1 — R-07). Segment-level PSI on `sex` bridges fair-lending subgroup stability.

---

## 5. Architecture & stack (R-06, R-07)

### 5.1 Four architectural pillars

| Pillar | v1 design |
| ------ | --------- |
| **Ingestion** | joblib/pickle sklearn contract + CSV/Parquet; `VendorModelAdapter` for §VII; OCC intake gate |
| **Audit log** | Greenfield hash-chained SQLite; FINOS mi-21 Tier 1–2; Tier 3 design doc |
| **Report generator** | Jinja2 → Markdown (+ optional WeasyPrint PDF); literal OCC I–VII |
| **Orchestration** | `ValidationRun` + materiality engine + module slots |

### 5.2 Ingestion contract (summary)

```yaml
model_ingest:
  format: joblib | vendor_api
  interface: [predict, predict_proba?]
dataset_ingest:
  required: [features, label, decision_column]
  optional: [protected_attributes]  # validation-only
```

**Intake gate:** Reject spreadsheet arithmetic, deterministic rules, models without statistical/economic theory basis (OCC model definition ✅ S-38).

### 5.3 Audit log schema (FINOS mi-21)

Hash-chained append-only `audit_log` table: `seq_id`, `event_type`, `payload_hash`, `prev_hash`, `chain_hash`, `finos_control`, `finos_tier`, `artifact_refs`.

**Key event types (P2 full run):** `validation_run.start` → `bias_battery.result` → `adverse_action.methodology_published` → `adverse_action.attribution` → `drift.event` → `validation_run.complete` → `report.generated`

**CLI:** `workbench audit verify-chain` — chain integrity, hash binding, monotonic `seq_id`.

**Decision:** Greenfield hash chain (not Monitaur dependency, not model-ledger alone — snapshots not end-to-end chained ⚠ S-46).

### 5.4 Report structure

Seven Jinja2 templates in `templates/occ_2026_13/`:

| Section | Content |
| ------- | ------- |
| I | Introduction + disclaimer |
| II | Purpose, scope, regulatory frames, limitations |
| III | Model risk overview |
| IV | Development and use |
| V.1 | Conceptual soundness |
| V.2 | Outcomes analysis (bias battery) |
| V.3 | Ongoing monitoring (drift) |
| VI | Governance and controls |
| VII | Vendor/third-party (mock adapter or N/A) |

**Appendices:** A (translation methodology), B (bias summary), C (drift), D (fidelity), E (audit verification).

### 5.5 Tech stack (confirmed)

| Layer | Choice | Status |
| ----- | ------ | ------ |
| Runtime | Python 3.11+ | ✅ |
| Bias | Fairlearn + Aequitas | ✅ |
| Interpretability | SHAP | ✅ |
| Drift | scipy + custom PSI | ✅ |
| BISG | surgeo (demo) | ✅ ⚠ census lag |
| Database | SQLite (inventory + audit) | ✅ |
| Reports | Jinja2 → MD + WeasyPrint PDF | ✅ |
| API | CLI + Python SDK; FastAPI optional | ✅ |
| Deployment | Local + Docker | ✅ |
| Extensibility | TrajectoryNormalizer protocol stub (choice B) | ADR only |

---

## 6. Scope & differentiation (R-09)

### 6.1 Build this, not that

| Build (v1) | Defer / never |
| ---------- | ------------- |
| `workbench validate run` → full battery → report → audit | Multi-tenant SaaS dashboard |
| Seven OCC Jinja2 section templates | Generic "AI governance" PDF |
| `bias_battery` with `regulatory_frame` toggles | Standalone Fairlearn notebook only |
| `translation_methodology_v1.json` versioned artifact | LIME-only explanations |
| SQLite hash-chained audit | Elasticsearch without chain |
| German Credit XGBoost demo | Production Postgres + K8s |
| State overlay config (CO/CA/NY) | 50-state rule engine |
| Detection-only bias flags | Fairlearn reductions / debiasing |

### 6.2 Demo vs. document-only

| Artifact | Demo | Document-only |
| -------- | ---- | ------------- |
| German Credit full validation | ✅ Primary | — |
| OCC seven-section report | ✅ | — |
| Proxy + sex AIR | ✅ | — |
| SHAP → reasons + methodology JSON | ✅ | — |
| Audit verify-chain | ✅ | — |
| Drift + T3 escalation | ✅ | — |
| CA overlay (`state_overlay: CA`) | ✅ P3 | — |
| CO overlay | ⚠ Alternative | Checklist legal text |
| NY insurance CL 7 DIA | ❌ | ✅ Scope note |
| BISG / Home Credit | Phase 2 | Pipeline docs |
| Tier 3 crypto audit | — | ✅ Design appendix |
| Gen-AI / TrajectoryNormalizer | — | ✅ Protocol + ADR |

---

## 7. MVP phasing & demo (R-10)

### 7.1 German Credit canonical walkthrough

| Attribute | Value |
| --------- | ----- |
| Dataset | UCI Statlog German Credit (1,000 rows) ✅ S-24 |
| Model | `XGBClassifier` → `german-credit-xgb-v1.2.joblib` |
| Protected attribute | `sex` (derived from `personal_status`; **not** a model feature) |
| Materiality | T3 — `exposure: 0.15`, `credit_decisioning` |
| Splits | train 700 / validation 300 / monitor 300 (injected covariate shift) |

**Entry points:**
- CLI: `workbench validate run --config configs/german_credit_full.yaml`
- Notebook: `notebooks/01_german_credit_validation.ipynb`
- P3: `configs/german_credit_ca_overlay.yaml`

### 7.2 Phase exit criteria (summary)

**P0:** Intake PASS; T3 tier; federal `bias_battery` three layers; report §I–VI; `verify-chain` PASS (≥3 events).

**P1:** TreeSHAP on N=50 adverse decisions; Appendix A + D; `adverse_action.*` events; §V.1 populated.

**P2 (CI minimum):** Score PSI + feature CSIs; Amber/Red on monitor split; §V.3 T3 escalation; Appendix C; 7-event audit sequence.

**P3:** CA overlay — §II two-frame diff; `admt_risk_assessment_summary.json`; Layer A labeled "outcomes analysis / risk-assessment evidence."

### 7.3 Required artifacts (P2 full run)

| Artifact | Appendix | Audit event |
| -------- | -------- | ----------- |
| `german_credit_validation_report.md` | — | `report.generated` |
| `translation_methodology_v1.json` | A | `adverse_action.methodology_published` |
| `bias_battery_summary.json` | B | `bias_battery.result` |
| `drift_report.json` | C | `drift.event` |
| `fidelity_validation_report.json` | D | `adverse_action.attribution` |
| `audit_chain_verification.json` | E | `report.generated` |

### 7.4 §II limitations block (mandatory)

> **Demo limitations:** UCI German Credit (German domestic credit, circa 1990s). Not US lending populations. No race/ethnicity; BISG **not performed**. Drift is **injected covariate shift**, not production drift. State overlays illustrate jurisdictional framing only.

### 7.5 Explicit non-goals

Consumer notices, NY insurance full DIA, algorithmic debiasing, BISG on German Credit, FHA/HMDA in core path, real temporal drift, production vendor API, challenger comparison (empty stub), EU conformity assessment, Tier 3 crypto demo.

---

## 8. Consolidated cross-framework control map

Extends foundation §3.6 with ECOA/Reg B column and Workbench module bindings (R-09 §4).

| Workbench feature | OCC 2026-13 | ECOA/Reg B | EU AI Act | NIST AI RMF | FINOS AIR | **Module / artifact** |
| ----------------- | ----------- | ---------- | --------- | ----------- | --------- | --------------------- |
| Model inventory + materiality tiering | §VI | — | Art. 9 | GOVERN 1.6 | — | `model_inventory`; `materiality_engine` |
| Intake gate (model definition) | §IV | — | Art. 11 | MAP 5.1 | mi-5 | `intake_gate` → `validation_run.start` |
| Validation report (CS / OA / OMM) | §V | — | Art. 11, 15 | MEASURE 2.9 | mi-5 | `report_generator` §V.1–V.3 |
| Statistical bias / fair-lending | §V outcomes | Proxy disc. (fed); FHA/state DIA | Art. 10 | MEASURE 2.11 | **gap → mi-5 evidence** | `bias_battery` → `bias_battery.result` |
| State overlay (CO/CA/NY) | §V context | Overlays R-08 | Art. 10 deployer | MEASURE 2.11 | ri-22 | `regulatory_frame.state_overlay` |
| Adverse-action translator | — adjacent | §1002.9 (statutory); historical Circ. 2022-03/2023-03 | Art. 13 | MEASURE 2.9 | — | `adverse_action_translator` |
| Translation methodology artifact | §V.1 / Appx A | §1002.9; historical Circ. 2022-03/2023-03 | — | — | mi-21 | `translation_methodology_v{N}.json` |
| Drift monitoring + escalation | §V.3 | — | Art. 72 | MANAGE 4.1 | mi-4 | `drift_monitor` → `drift.event` |
| Tamper-evident audit log | §VI | — | Art. 12 | GOVERN 4.2 | **mi-21 Tier 1–2** | `audit_log` hash chain |
| Human override / governance | §VI | — | Art. 14 | GOVERN 3.2 | mi-11 | `governance.approval` event |
| Vendor / third-party model | **§VII** | — | Art. 26(5) | MAP 4.1 | — | `VendorModelAdapter` + §VII template |
| Protected-class hard reject | §V | Reg B design | Art. 10 | MEASURE 2.11 | mi-5 | ingest schema validation |

---

## 9. Consolidated source ledger

Legend: ✅ primary verified | ⚠ secondary/partial | ❌ unverified or inaccessible

| ID | Source | Tier | Used in | Status |
| -- | ------ | ---- | ------- | ------ |
| S-01 | Chartis MRM Solutions 2024 (Genpact PDF mirror) | 3 | R-01 | ⚠ |
| S-02 | Gartner MQ AI Governance Platforms Jun 2026 | 3 | R-01 | ⚠ |
| S-03 | ValidMind product brief + Chartis graphics | 2/3 | R-01, R-10 | ✅ |
| S-04 | SAS Chartis 2024 press release | 3 | R-01 | ✅ |
| S-05 | Solytics MRM Vault / SR 26-2 whitepaper | 3 | R-01 | ✅ |
| S-06 | ModelOp.com product pages | 3 | R-01 | ✅ |
| S-07 | Fiddler AI GRC + FSI datasheet | 3 | R-01, R-05 | ✅ |
| S-08 | Holistic AI + Fronterio comparison blog | 3 | R-01 | ⚠ |
| S-09 | Monitaur platform + case studies | 3 | R-01 | ✅ |
| S-10 | aicompliancevendors.com MRM ranking | 3 | R-01 | ⚠ |
| S-11 | getaigovernance.net expert guide | 3 | R-01 | ⚠ |
| S-12 | FINOS AIGF GitHub + press releases | 1 | R-01 | ✅ |
| S-13 | block/model-ledger GitHub | 3 | R-01 | ✅ |
| S-14 | Fairlearn + Aequitas GitHub | 3 | R-01 | ✅ |
| S-15 | Federal Register 91 FR 21620 (Reg B) | 1 | R-02 | ✅ |
| S-16 | CFPB Regulation B landing page | 1 | R-02 | ✅ |
| S-17 | Venable / GT / KPMG Reg B alerts | 2 | R-02 | ⚠ |
| S-18 | CFPB Circular 2022-03 (adverse action) | 1 | R-02, R-04 | ✅ |
| S-19 | CFPB proxy-methodology GitHub + 2014 report | 1 | R-03 | ✅ |
| S-20 | Federal Register 91 FR 21620 preamble | 1 | R-03 | ✅ |
| S-21 | EEOC Uniform Guidelines 4/5ths rule Q&A | 1 | R-03 | ✅ |
| S-22 | Fairlearn credit loan decisions tutorial | 2 | R-03 | ✅ |
| S-23 | Aequitas documentation | 2 | R-03 | ✅ |
| S-24 | UCI German Credit dataset | 2 | R-03, R-10 | ✅ |
| S-25 | Kaggle Home Credit Default Risk | 2 | R-03, R-05 | ✅ |
| S-26 | ACM FAccT four-fifths rule paper | 2 | R-03 | ⚠ |
| S-27 | OCC Comptroller's Handbook Fair Lending | 1 | R-03 | ⚠ |
| S-28 | Asurity Advisors BISG overview | 2 | R-03 | ⚠ |
| S-29 | Pace Analytics Reg B LDA/proxy post | 2 | R-03 | ⚠ |
| S-30 | HuggingFace alerterra/credit_scoring_fairness | 3 | R-03 | ⚠ |
| S-31 | CFPB Circular 2023-03 PDF | 1 | R-04 | ✅ |
| S-32 | CFPB Innovation Spotlight (AI/ML adverse action) | 1 | R-04 | ✅ |
| S-33 | Unverified CFPB circular numbered "2026-03" (via R-02 + trade press) — not found on CFPB.gov or Federal Register (R-12) | 1 | R-04 | ❌ |
| S-34 | Reg B §1002.9 + Official Interpretation | 1 | R-04 | ✅ |
| S-35 | SHAP library / Lundberg & Lee | 2 | R-04 | ✅ |
| S-36 | BrightCloud ECOA explainability analysis | 2 | R-04 | ⚠ |
| S-37 | CFPI interpretable algorithms post | 2 | R-04 | ⚠ |
| S-38 | OCC Bulletin 2026-13 PDF | 1 | R-05, R-06, R-10 | ✅ |
| S-39 | Lewis (1994) / Siddiqi PSI thresholds | 2 | R-05 | ⚠ |
| S-40 | Western Michigan PSI statistical properties | 2 | R-05 | ✅ |
| S-41 | Annals of OR 2025 Population Resemblance Statistic | 2 | R-05 | ⚠ |
| S-42 | DC-Guard TechRxiv drift policy paper | 2 | R-05 | ⚠ |
| S-43 | SR 11-7 original monitoring language | 1 | R-05 | ✅ |
| S-44 | Fiddler AI GRC (R-01 cross-ref) | 3 | R-05 | ✅ |
| S-45 | FINOS AIR-DET-021 mi-21 | 1 | R-06, R-10 | ✅ |
| S-46 | block/model-ledger guarantees.md | 2 | R-06, R-07 | ✅ |
| S-47 | Monitaur platform + MLA whitepaper | 3 | R-06 | ✅ |
| S-48 | Databricks MRM 2026 banker guide | 2 | R-06 | ⚠ |
| S-49 | Microsoft Research AgentRx | 2 | R-06 | ✅ |
| S-50 | surgeo PyPI + documentation | 2 | R-07 | ✅ |
| S-51 | evidently AI drift/PSI docs | 2 | R-07 | ⚠ |
| S-52 | Colorado SB 26-189 | 1 | R-08 | ✅ |
| S-53 | Colorado SB 24-205 (historical) | 1 | R-08 | ✅ |
| S-54 | CPPA regulations — ADMT package | 1 | R-08 | ✅ |
| S-55 | FPF CCPA ADMT Issue Brief (Oct 2025) | 2 | R-08 | ⚠ |
| S-56 | CA AG Legal Advisory — AI + existing CA law | 1 | R-08 | ✅ |
| S-57 | NY DFS Insurance Circular Letter 7 (2024) | 1 | R-08 | ✅ |
| S-58 | NY DFS IL 2024-10-16 AI cybersecurity | 1 | R-08 | ✅ |
| S-59 | NY A773B bill text (pending) | 1 | R-08 | ✅ |
| S-60 | FINOS ri-22 regulatory compliance | 1 | R-08, R-09 | ✅ |
| S-61 | CA AB 1018 bill text (pending) | 1 | R-08 | ✅ |

**Internal artifacts (build-time):** Fixture SHA-256 hashes in `manifests/german_credit_fixture_manifest.yaml` — recorded at freeze commit, not external sources.

---

## 10. Open questions & next build steps

### 10.1 Build phase (owner: build)

| # | Question | Recommendation |
| - | -------- | -------------- |
| B1 | XGB hyperparameters for v1.2 joblib | Document in `configs/model_training_german_credit.yaml`; freeze at first training run |
| B2 | Aequitas Python 3.11+ compatibility | Verify at build; pin or fork if needed |
| B3 | WeasyPrint Docker deps (libcairo/pango) | Document in README for `[pdf]` extra |
| B4 | Fidelity human-review sign-off UX | Tier-2 audit slot; manual notebook acknowledgment for demo |
| B5 | CI canonical path | **CLI** for CI (`P2` + `verify-chain`); notebook for portfolio review |
| B6 | Hypothesis tests for audit chain | Mirror model-ledger pattern ✅ S-46 |
| B7 | ~~Primary-source spot-check of the unverified "2026-03" circular claim~~ | ✅ **Resolved (R-12/R-14):** No such circular exists on CFPB.gov or in the Federal Register. Differentiator #3 reworded to Reg B §1002.9 + historical Circular 2022-03/2023-03 (withdrawn May 12, 2025). The Jul 9, 2026 trade-press article (S-84) is a false secondary — do not cite as corroboration. |
| B8 | `admt_risk_assessment_summary.json` field list | Map to CPPA §7152; refine after first enforcement |

### 10.2 v1.1 enhancements (owner: v1.1)

| # | Item | Trigger |
| - | ---- | ------- |
| V1 | Sample-size-adjusted PSI | R-05; document Lewis limitations in v1 Appendix C |
| V2 | ONNX ingest | Demo need only |
| V3 | Postgres production deploy | Multi-user requirement |
| V4 | surgeo 2020 Census DHC update | Accuracy gap on Home Credit demo |
| V5 | CFPB Stata BISG Python port | If surgeo divergence material |
| V6 | FastAPI auth | External deployment |
| V7 | Champion-challenger minimal AUC delta | Portfolio story upgrade |
| V8 | Tier 3 Ed25519 signed audit segments | HSM vs software key decision |

### 10.3 Watchlist (owner: watchlist)

| # | Item | Monitor |
| - | ---- | ------- |
| W1 | Reg B effects-test litigation | Courts may challenge CFPB elimination ⚠ S-17 |
| W2 | Colorado AG rules (Jan 2027) | Post-adverse disclosure content; update CO checklist |
| W3 | CA CPPA ADMT enforcement | First cases may revise risk-assessment template |
| W4 | NY A773B / CA AB 1018 enactment | Add `NY_LENDING` / `CA_ADS` overlay profiles |
| W5 | CO AG rules ECOA safe harbor mapping | Counsel review for R-04 output vs SB 189 disclosures |
| W6 | Section 1071 small-business lending | Out of v1 unless demo pivots |
| W7 | CFPB reissue of adverse-action/AI explainability guidance | Unknown; deregulatory posture 2025–2026 (May 2025 mass withdrawal). Monitor CFPB circulars/Federal Register; do not pre-claim reaffirmation (R-14 §3.2) |

### 10.4 Resolved in research (no further action)

- Hash-chained log: greenfield (not Monitaur/model-ledger dependency) — R-06
- Python stack confirmed — R-07
- Federal fairness metrics: proxy-discrimination primary — R-02/R-03
- P3 state overlay: CA primary — R-10
- Challenger: empty stub — R-10
- PDF: Markdown default, optional WeasyPrint — R-10
- Vendor §VII: mock `VendorModelAdapter` — R-10
- v1 scope boundary locked — R-09

### 10.5 First build sprint checklist

1. Scaffold Python package: CLI (`workbench validate`, `workbench audit verify-chain`), SDK (`ValidationRun`)
2. Implement P0: ingest gate, materiality engine, `bias_battery`, report §I–VI, SQLite audit chain
3. Freeze German Credit fixtures + manifest SHA-256; `scripts/freeze_german_credit_fixtures.py`
4. P1: `adverse_action_translator` + `translation_methodology_v1.json`
5. P2: `drift_monitor` + injected monitor shift; wire §V.3; CI gate
6. P3: `regulatory_frame.state_overlay: CA`; `admt_risk_assessment_summary.json`
7. Ship `notebooks/01_german_credit_validation.ipynb` + README with limitations, verify-chain badge, do-not-claim list

---

*Research program complete. Individual finding files remain authoritative for ticket-level detail; this document is the build-phase synthesis.*
