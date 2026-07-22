# Deep Research — Master Orchestration Plan

**Project:** AI Model Risk & Governance Workbench  
**Foundation doc:** `RESEARCH_FOUNDATION_v2.md`  
**Final deliverable:** `deep-research-v1.md` (aggregated from individual finding files)  
**Created:** 2026-07-20  
**Status:** Complete — research program finished (Session 6)

---

## 0. Governing Decisions (from stakeholder answers)

| Decision | Choice |
| -------- | ------ |
| Research priority order | Tier 3 competitive landscape **first** → informs differentiation & stack |
| Output naming | Lowercase, hyphen-delimited (`deep-research-v1.md`) |
| Deliverable style | **Actionable recommendations**, not findings-only |
| LLM/agentic scope (v1) | **B** — extensible lifecycle with optional LLM/agent path from day one; traditional ML credit models as primary demo path |
| Regulatory emphasis | US federal (OCC 2026-13, ECOA/Reg B) primary; EU AI Act + FINOS secondary; state law tertiary |
| Competitive depth | **Deep** — top ~8–10 products, feature-level comparison, proof-point verification |
| Demo scenario | No hard constraints; optimize alignment, usability, completeness/robustness |
| Paywall handling | Use public summaries, marketplaces, vendor sites, OSS; flag inaccessible primary reports |
| Session model | Quality over speed; multiple sessions; individual finding files → final aggregation |
| Reg B July 2026 claim | **Actively verify or debunk** (flagged unverified in foundation §3.2) |

---

## 1. Directory Layout

```
ai-mrg-bench/
├── RESEARCH_FOUNDATION_v2.md          # Launch pad (do not mutate during research)
├── research/
│   ├── deep-research-master-plan.md   # THIS FILE — orchestration source of truth
│   ├── sessions/
│   │   └── session-NN-log.md          # Per-session scope, status, handoff
│   └── findings/
│       ├── R-01-tier3-competitive-landscape.md
│       ├── R-02-reg-b-july-2026-verification.md
│       ├── R-03-bias-fair-lending-methodology.md
│       ├── R-04-interpretability-adverse-action.md
│       ├── R-05-drift-detection-materiality.md
│       ├── R-06-architecture-audit-report-ingestion.md
│       ├── R-07-tech-stack-validation.md
│       ├── R-08-state-ai-lending-laws.md
│       ├── R-09-scope-differentiation-synthesis.md
│       ├── R-10-mvp-phasing-demo-scenario.md
│       └── source-ledger.md           # Running cumulative source ledger
└── deep-research-v1.md                # FINAL — aggregated deliverable (Session 6)
```

---

## 2. Research Ticket Registry

Tickets are **sequenced by dependency**, not arbitrary priority. Tier 3 (R-01) is first because R-06, R-07, R-09, and R-10 depend on its output.

| ID | Title | Depends on | Session target | Status | Finding file |
| -- | ----- | ---------- | -------------- | ------ | ------------ |
| **R-01** | Tier 3 competitive & prior-art landscape (deep) | — | **1** | `complete` | `findings/R-01-tier3-competitive-landscape.md` |
| **R-02** | Reg B July 2026 narrowing — verify/debunk | — | **1** | `complete` | `findings/R-02-reg-b-july-2026-verification.md` |
| **R-03** | Bias/fair-lending statistical methodology | R-01 (gap confirmation) | 2 | `complete` | `findings/R-03-bias-fair-lending-methodology.md` |
| **R-04** | Interpretability → adverse-action pipeline | R-03 | 2 | `complete` | `findings/R-04-interpretability-adverse-action.md` |
| **R-05** | Drift detection & materiality-tier escalation | R-01 | 2 | `complete` | `findings/R-05-drift-detection-materiality.md` |
| **R-06** | Architecture: ingestion, audit log, report structure | R-01, R-05 | 3 | `complete` | `findings/R-06-architecture-audit-report-ingestion.md` |
| **R-07** | Tech stack validation (competitive + requirements) | R-01, R-06 | 3 | `complete` | `findings/R-07-tech-stack-validation.md` |
| **R-08** | State-level AI/lending laws (CO, CA, NY) | — | 4 | `complete` | `findings/R-08-state-ai-lending-laws.md` |
| **R-09** | Scope boundaries & differentiation synthesis | R-01, R-03, R-08 | 4 | `complete` | `findings/R-09-scope-differentiation-synthesis.md` |
| **R-10** | MVP phasing & concrete demo scenario | R-01–R-09 | 5 | `complete` | `findings/R-10-mvp-phasing-demo-scenario.md` |
| **R-11** | Final aggregation → `deep-research-v1.md` | ALL | 6 | `complete` | `deep-research-v1.md` |

---

## 3. Per-Ticket Scope Definitions

### R-01 — Tier 3 Competitive Landscape (DEEP)

**Objective:** Identify top ~8–10 credible products/platforms; produce comparison matrix; synthesize commodity vs. gap.

**Source categories (per foundation §5):**
1. Analyst reports (Chartis RiskTech, Gartner AI TRiSM, Forrester, Evident AI Index)
2. G2 / Capterra / TrustRadius category listings
3. GitHub OSS (`model-risk-management`, `ai-governance`, `responsible-ai`, `fairness-testing`)
4. FINOS AI Governance Framework contributors/adopters
5. Trade press (American Banker, Risk.net)
6. Academic surveys (arXiv)
7. Funding signal (Crunchbase/public equivalents)

**Evaluation criteria (matrix columns):**
- Framework coverage specificity (OCC 2026-13, ECOA/Reg B, EU AI Act, NIST AI RMF, FINOS AIR — control-ID level vs. vague)
- Deployment model (OSS / proprietary; self-hosted / SaaS)
- Target segment (enterprise-only vs. accessible)
- Statistical bias/fair-lending depth (beyond FINOS gap)
- Audit-log tier alignment (FINOS AIR-DET-021 explicit or not)
- Customer proof points vs. vaporware
- Pricing/licensing (where discoverable)
- Tech stack (where discoverable)
- LLM/agentic governance support

**Output sections:** candidate inventory → deep profiles (top 8–10) → comparison matrix → gap synthesis → implications for Workbench

---

### R-02 — Reg B July 2026 Narrowing Verification

**Objective:** Confirm or debunk the unverified "July 2026 Reg B narrowing" claim from foundation §3.2.

**Sources:** Federal Register, CFPB rulemaking docket, CFPB circulars, law-firm alerts, trade press. Label verified vs. unverified.

---

### R-03 — Bias/Fair-Lending Statistical Methodology

**Objective:** Recommend specific statistical battery and dataset/proxy strategy.

**Topics:** four-fifths rule / adverse impact ratio, standardized mean difference, disparate impact analysis, protected-class restrictions, BISG-style proxy methodology, public/synthetic dataset options for demo.

---

### R-04 — Interpretability → Adverse-Action Pipeline

**Objective:** Recommend interpretability approach (SHAP vs. alternatives) and mapping pipeline to CFPB Circular 2026-03 "documented translation methodology" requirement.

---

### R-05 — Drift Detection & Materiality Escalation

**Objective:** Recommend drift methods (PSI, KS, etc.), thresholds, and triggers linking drift events to OCC 2026-13 materiality-tier review escalation.

---

### R-06 — Architecture Decisions

**Objective:** Concrete recommendations for model ingestion contract, tamper-evident audit log design, OCC 2026-13 seven-section report generator — informed by R-01 competitive patterns and FINOS AIR-DET-021.

**LLM/agent path:** Design for extensibility (FINOS tiers 0–3) without claiming regulatory completeness for gen-AI.

---

### R-07 — Tech Stack Validation

**Objective:** Confirm or revise Python-centric hypothesis based on competitive landscape + workload profile (batch/analytical + append-only audit).

---

### R-08 — State-Level AI/Lending Laws

**Objective:** Colorado AI Act, California DFPI automated-decision rules, NY DFS guidance — how they fill federal gen-AI gap; tertiary to federal US.

---

### R-09 — Scope & Differentiation Synthesis

**Objective:** Actionable v1 scope boundary recommendation across all frameworks; primary differentiator choice informed by R-01 gap analysis.

---

### R-10 — MVP Phasing & Demo Scenario

**Objective:** Smallest end-to-end slice; concrete demo (model, dataset, artifacts produced); checklist against OCC 2026-13 seven sections.

---

### R-11 — Final Aggregation

**Objective:** Merge all finding files + source ledger into `deep-research-v1.md` with executive summary, per-module recommendations, and open questions.

---

## 4. Session Plan (provisional)

| Session | Tickets | Primary focus |
| ------- | ------- | ------------- |
| **1** | R-01, R-02 | ✅ Complete — competitive landscape + Reg B verification |
| **2** | R-03, R-04, R-05 | ✅ Complete — validation methodology trilogy |
| **3** | R-06, R-07 | ✅ Complete — architecture + stack |
| **4** | R-08, R-09 | ✅ Complete — state law + differentiation synthesis |
| **5** | R-10 | ✅ Complete — MVP + demo scenario |
| **6** | R-11 | ✅ Complete — final aggregation |

Sessions may be split further if context limits require it. Update this table after each session.

---

## 5. Quality Gates (every finding file)

- [ ] Primary sources cited with URLs and access date
- [ ] Verified ✅ / secondary ⚠ / unverified ❌ labels on load-bearing claims
- [ ] Statistics cross-corroborated (≥2 independent sources) or flagged
- [ ] Explicit "Implications for Workbench" section
- [ ] Open questions listed where primary source unavailable
- [ ] Master plan ticket status updated

---

## 6. Aggregation Template (for R-11)

`deep-research-v1.md` will contain:

1. Executive summary & top recommendations
2. Competitive landscape (from R-01)
3. Regulatory verification updates (R-02, R-08)
4. Validation methodology (R-03, R-04, R-05)
5. Architecture & stack (R-06, R-07)
6. Scope & differentiation (R-09)
7. MVP phasing & demo (R-10)
8. Cross-framework control map (updated)
9. Source ledger (consolidated)
10. Open questions & next build steps

---

## 7. Session Log

### Session 1 — 2026-07-20

**Scope:** R-01 (Tier 3 competitive landscape, deep); R-02 (Reg B July 2026 verification).  
**Status:** ✅ Complete  
**Finding files:** `findings/R-01-tier3-competitive-landscape.md`, `findings/R-02-reg-b-july-2026-verification.md`  
**Handoff:** See `sessions/session-01-log.md`

### Session 2 — 2026-07-20

**Scope:** R-03 (bias/fair-lending statistical battery); R-04 (interpretability→adverse-action pipeline); R-05 (drift detection & materiality-tier escalation).  
**Status:** ✅ Complete  
**Finding files:** `findings/R-03-bias-fair-lending-methodology.md`, `findings/R-04-interpretability-adverse-action.md`, `findings/R-05-drift-detection-materiality.md`  
**Handoff:** See `sessions/session-02-log.md`

### Session 3 — 2026-07-20

**Scope:** R-06 (architecture: ingestion, audit log, OCC seven-section report); R-07 (tech stack validation).  
**Status:** ✅ Complete  
**Finding files:** `findings/R-06-architecture-audit-report-ingestion.md`, `findings/R-07-tech-stack-validation.md`  
**Handoff:** See `sessions/session-03-log.md`

### Session 4 — 2026-07-20

**Scope:** R-08 (state-level AI/lending laws: CO, CA, NY); R-09 (scope boundaries & differentiation synthesis).  
**Status:** ✅ Complete  
**Finding files:** `findings/R-08-state-ai-lending-laws.md`, `findings/R-09-scope-differentiation-synthesis.md`  
**Handoff:** See `sessions/session-04-log.md`

### Session 5 — 2026-07-20

**Scope:** R-10 (MVP phasing + German Credit concrete demo scenario).  
**Status:** ✅ Complete  
**Finding files:** `findings/R-10-mvp-phasing-demo-scenario.md`  
**Handoff:** See `sessions/session-05-log.md`

### Session 6 — 2026-07-21

**Scope:** R-11 (final aggregation → `deep-research-v1.md`).  
**Status:** ✅ Complete  
**Deliverable:** `deep-research-v1.md` (repo root)  
**Handoff:** See `sessions/session-06-log.md`

---

*Research program complete. All tickets R-01 through R-11 are `complete`.*
