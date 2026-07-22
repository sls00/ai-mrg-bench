# R-01 — Tier 3 Competitive & Prior-Art Landscape (Deep)

**Ticket:** R-01  
**Session:** 1  
**Status:** Complete (Session 1 scope)  
**Research date:** 2026-07-20  
**Analyst access:** Chartis 2024 MRM report (public mirror via Genpact PDF ⚠); Gartner MQ June 2026 (vendor press + secondary summaries ⚠ — full MQ paywalled); primary vendor sites ✅

---

## 1. Executive summary

The market splits into **four distinct layers** that are frequently conflated:

| Layer | What it does | Representative products | Workbench relationship |
| ----- | ------------ | --------------------- | ---------------------- |
| **A. MRM lifecycle platforms** | Inventory, validation workflows, documentation, tiered governance | ValidMind, SAS MRM, Solytics MRM Vault, ModelOp | **Closest analog** — but enterprise-priced, not model-agnostic validation engines |
| **B. AI governance / GRC platforms** | Policy, risk classification, multi-framework assessments, agent registry | Credo AI, IBM watsonx.governance, ServiceNow AI Control, Truyo | Cover breadth; thin on statistical validation depth |
| **C. Observability / monitoring** | Drift, bias metrics in production, LLM guardrails, explainability | Fiddler AI, Arthur AI | Strong post-deployment; weak pre-deployment validation reports |
| **D. Component libraries / OSS** | Fairness metrics, SHAP, bias audits | Fairlearn, Aequitas, FINOS AIGF (framework only) | **Build on top of**, not compete with |

**Gap synthesis (preliminary — informs R-09):** No identified product combines all of:

1. Model-agnostic ingest of arbitrary `.predict()`/`.predict_proba()` models + labeled dataset
2. OCC **2026-13 seven-section** validation report structure (most still mentally organized around SR 11-7 three pillars)
3. Dedicated statistical fair-lending battery with **proxy-discrimination** focus post–Reg B July 2026
4. CFPB Circular 2026-03 adverse-action translation with **documented mapping methodology artifact**
5. FINOS **AIR-DET-021 Tier 2–3** tamper-evident audit trail as a first-class, citable implementation

Enterprise vendors cover subsets; OSS covers components; **the integrated, auditor-facing, open/portfolio-scale workbench remains unoccupied.**

---

## 2. Market structure & analyst signal

### 2.1 Chartis Research — Model Risk Management Solutions 2024

**Status:** ⚠ Secondary access (Genpact-hosted PDF mirror of Chartis report; Chartis primary paywalled)

**Coverage:** 30 providers across validation (credit, derivatives) and governance quadrants:

Acadia (LSEG), Analytics Boutique, BCT Digital, Bloomberg, CIMCON, **CRISIL**, DataRobot, Evalueserve, Finastra, FIS, Genpact, IBM, ICE Data Services, Infosys, KPMG, MathWorks, MatLogica, MetricStream, Mitratech, Numerix, Prometeia, PwC, RiskSpan, **SAS**, TCS, TurinTech, **ValidMind**, Wipro, Wolters Kluwer, Yields

**Category leaders (vendor-corroborated):**
- **SAS** — model governance (top score among 19 vendors) + credit validation
- **CRISIL Integral IQ** — credit validation, derivatives validation, governance excellence
- **ValidMind** — category leader in **all three** quadrants (unique crossover of statistical/AI + traditional quant)

**2026 outlook:** Chartis 2026 report agenda explicitly merges **2024 MRM + 2025 AI governance** studies — confirms market convergence thesis.

### 2.2 Gartner — Magic Quadrant for AI Governance Platforms (June 16, 2026)

**Status:** ⚠ MQ document paywalled; vendor placements corroborated across 3+ secondary sources

| Quadrant | Vendors |
| -------- | ------- |
| **Leaders** | IBM, ServiceNow, Truyo |
| **Visionaries** | Airia, **Credo AI**, **ModelOp**, **Monitaur**, OneTrust |
| **Challengers** | Holistic AI |
| **Niche** | Cranium AI, Relyance AI, Saidot, SAP |

**Note:** Gartner AI Governance MQ ≠ MRM MQ. ModelOp and Monitaur appear here as governance platforms, not pure MRM.

### 2.3 Evident AI Index

**Status:** ✅ Public rankings; **not a vendor landscape** — ranks **banks** on AI maturity (Talent 45%, Innovation 30%, Leadership 15%, Transparency 10%). Useful for understanding buyer sophistication, not competitive products.

### 2.4 G2 / marketplace

**Status:** ⚠ MRM is a sub-segment of Enterprise Risk Management on G2 (99 ERM listings). No dedicated high-traffic "Model Risk Management" grid with deep reviews found. Specialized buyers use analyst reports + vendor RFPs, not G2 self-serve.

---

## 3. Open-source & standards-body landscape

### 3.1 FINOS AI Governance Framework (AIGF)

- **Type:** Machine-readable risk/mitigation catalogue (v2.0 adds agentic AI risks)
- **Stars:** ~81 (GitHub, April 2025)
- **Maintainers:** Scott Logic, ControlPlane, Morgan Stanley, Citi, NatWest
- **Adopters/contributors:** BMO, RBC, Bank of America, Microsoft, AWS, Google Cloud, Goldman Sachs (per FINOS press)
- **Gap confirmed:** No statistical bias/fair-lending mitigation (ri-16 addressed only via mi-5 acceptance testing, mi-11 human feedback)
- **Workbench angle:** Implement against control IDs; cite AIR-DET-021 tiers

### 3.2 block/model-ledger (OSS)

- **Type:** Cross-platform model inventory + immutable change graph + MCP server
- **Stars:** ~5 (very early; active releases through July 2026)
- **Maps to:** SR 11-7/SR 26-2, EU AI Act Annex IV, NIST AI RMF (built-in `validate` profiles)
- **Not:** Validation battery, bias testing, or adverse-action module
- **Workbench angle:** Potential **integration target** for inventory/audit subgraph, not competitor

### 3.3 finos-labs/open-eago

- Agent governance control plane (A2A/MCP overlay) — relevant for v1 extensibility path (stakeholder choice B), not v1 core

### 3.4 Fairlearn / Aequitas (component libraries)

| Library | Stars | Strength | Limitation |
| ------- | ----- | -------- | ---------- |
| **Fairlearn** (Microsoft) | ~2k+ | Metrics + mitigation algorithms; NIST ecosystem | No MRM workflow, no regulatory report structure |
| **Aequitas** (DSSG) | ~758 | Bias audit dashboards; Aequitas Flow experimentation pipeline | Policy-audit shaped; not full lifecycle |
| **IBM AIF360** | Academic breadth | Pre/in/post-processing variety | Heavy; academic shape |

**Pattern:** Libraries produce metrics; platforms produce workflows + evidence chains. Workbench should **compose** Fairlearn/Aequitas/SHAP, not rebuild them.

---

## 4. Deep profiles — top 10 candidates

Selection criteria: financial-services MRM relevance, feature depth verifiable from public sources, coverage across layers A–C, plus one OSS signal.

---

### 4.1 ValidMind

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | Purpose-built MRM + AI/agentic governance |
| **Deployment** | Proprietary; SaaS/enterprise (contact sales) |
| **Target segment** | Banks, insurers — mid-to-large regulated FIs |
| **Framework claims** | SR 11-7 / **SR 26-2** (marketing), OSFI E-23, SS1/23, EU AI Act, NAIC — **workflow language, not control-ID maps** |
| **OCC 2026-13 seven sections** | ❌ Not found — still framed around SR 11-7 / three-pillar mental model in public materials |
| **Bias/fair-lending depth** | ⚠ Stress testing, fairness in validation workflows; no published four-fifths/proxy battery |
| **Adverse-action module** | ❌ Not a named product capability |
| **Audit log / FINOS tier** | ⚠ "Immutable audit trails for reasoning traces" (agentic); no AIR-DET-021 tier citation |
| **LLM/agentic** | ✅ Core positioning — policy-as-code, agent governance, execution authority boundaries |
| **Drift monitoring** | ⚠ Via integrations; not native telemetry-first |
| **Proof points** | ✅ Chartis 2024 category leader (all 3 quadrants); Experian Ascend integration (Feb 2025); $8.1M seed (2024) |
| **Pricing** | Contact only |
| **Tech stack** | Python SDK, Jupyter integration, API — Python-centric validation engine |

**Verifier notes:** Strongest **direct competitor** for governance workflow; weakest on standalone statistical fair-lending + adverse-action translation.

---

### 4.2 SAS Model Risk Management

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | Enterprise MRM suite (incumbent) |
| **Deployment** | Proprietary; on-prem + cloud |
| **Target segment** | Large banks ($30B+ asset cohort per OCC threshold) |
| **Framework claims** | SR 11-7 heritage; EU AI Act, NAIC in marketing — **enterprise GRC integration** |
| **OCC 2026-13 seven sections** | ❌ Not found in public materials reviewed |
| **Bias/fair-lending** | ⚠ Fair lending analytics exist in SAS ecosystem (separate products); not unified in MRM core |
| **Adverse-action** | ❌ |
| **Audit log** | ⚠ Enterprise logging; no FINOS tier alignment |
| **LLM/agentic** | ⚠ Adapting per Chartis ("growing salience of AI models") |
| **Drift monitoring** | ✅ Strong in enterprise deployments |
| **Proof points** | ✅ Chartis category leader 11 consecutive years; 19 vendors in governance quadrant |
| **Pricing** | Enterprise license — high six/seven figures typical |
| **Tech stack** | SAS-native; Python/R bridges |

**Verifier notes:** Commodity at tier-1 banks for inventory/governance; inaccessible to solo builder / portfolio demo scale.

---

### 4.3 Solytics Partners (MRM Vault + NIMBUS Uno)

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | MRM ecosystem — governance + validation + monitoring |
| **Deployment** | Proprietary; private cloud |
| **Target segment** | Large model risk organizations |
| **Framework claims** | **SR 26-2** explicitly (whitepapers post-April 2026); SR 11-7, EU AI Act, SS1/23, OSFI E-23, MAS FEAT |
| **OCC 2026-13 seven sections** | ⚠ Closest public vendor narrative to **materiality-tiered** governance — but not structured as seven named report sections |
| **Bias/fair-lending** | ✅ NIMBUS Uno lists **Fair Lending** as pre-built regulatory solution |
| **Adverse-action** | ⚠ Fair lending module implied; no CFPB Circular 2026-03 mapping artifact |
| **Audit log** | ✅ "Audit trail for all major and minor changes" |
| **LLM/agentic** | ⚠ LLM contextual search in Vault; gen-AI carve-out acknowledged in SR 26-2 whitepaper |
| **Drift monitoring** | ✅ Threshold-triggered re-validation |
| **Proof points** | ⚠ No Chartis quadrant leader status found; strong regulatory content marketing |
| **Pricing** | Contact only |
| **Tech stack** | Integrates Jupyter, SAS, NIMBUS analytics |

**Verifier notes:** Best vendor signal for **SR 26-2 materiality-tiering UX**; still enterprise-only.

---

### 4.4 ModelOp Center

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | Enterprise AI system of record / lifecycle automation |
| **Deployment** | Proprietary |
| **Target segment** | Large enterprises — FSI, healthcare, government |
| **Framework claims** | 25+ templates: SR 11-7, Dodd-Frank, GDPR, EU AI Act, NIST, ISO 42001 — **template-level, not OCC section-level** |
| **OCC 2026-13** | ❌ |
| **Bias/fair-lending** | ⚠ Policy enforcement; not statistical battery-first |
| **Adverse-action** | ❌ |
| **Audit log** | ⚠ Workflow evidence; not cryptographic tier-3 |
| **LLM/agentic** | ✅ Strong — MADE engine, agent delivery workflows (Gartner Visionary 2026) |
| **Drift monitoring** | ⚠ Thinner than observability-native tools |
| **Proof points** | ✅ Gartner MQ Visionary 2026; Fidelity case study; BBSI credit-scoring deployment |
| **Pricing** | Contact only |
| **Tech stack** | 50+ integrations; technology-agnostic inventory |

---

### 4.5 Fiddler AI

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | AI observability + GRC reporting layer |
| **Deployment** | Proprietary SaaS; in-VPC Trust Models for FSI |
| **Target segment** | FSI, healthcare — post-deployment monitoring |
| **Framework claims** | SR 11-7, HIPAA, NAIC, EU AI Act, CA AI bills — **GRC module** |
| **OCC 2026-13** | ❌ Still references SR 11-7 in public GRC pages |
| **Bias/fair-lending** | ✅ Demographic parity, disparate impact tracked in production |
| **Adverse-action** | ⚠ SHAP explainability supports reason derivation; no Reg B translator |
| **Audit log** | ✅ Decision logging; not FINOS-tier cryptographic |
| **LLM/agentic** | ✅ Strong — agent traces, hallucination, PII, prompt injection |
| **Drift monitoring** | ✅ Core competency — PSI-style, data quality, 30+ ML / 50+ LLM metrics |
| **Proof points** | ✅ Named FSI SageMaker deployment; $100M total funding (Series C Jan 2026) |
| **Pricing** | Tiered (per aicompliancevendors.com) |
| **Tech stack** | Cloud-native; AWS SageMaker integration |

**Verifier notes:** Best **monitoring layer** reference architecture; not a replacement for validation report generator.

---

### 4.6 Holistic AI

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | Bias auditing + AI visibility/discovery |
| **Deployment** | Proprietary |
| **Target segment** | Regulated industries — lending, insurance, hiring |
| **Framework claims** | EU AI Act RAG classification, NIST, ISO 42001, NYC LL144 — **audit-report shaped** |
| **OCC 2026-13** | ❌ |
| **Bias/fair-lending** | ✅✅ **Deepest in market** — SPD, DIR, adversarial robustness, calibration; academic-grade audit reports |
| **Adverse-action** | ⚠ Technical factor attribution; not Reg B-specific reason-code translator |
| **Audit log** | ⚠ Guardian Agents for discovery/enforcement |
| **LLM/agentic** | ✅ Red-teaming, jailbreak research (HAI Labs) |
| **Drift monitoring** | ⚠ Less emphasis than Fiddler |
| **Proof points** | Gartner MQ Challenger 2026; risk/compliance use case #1 per vendor |
| **Pricing** | Contact only (~$15M raised; mid-size vendor) |
| **Tech stack** | Multi-cloud scanning integrations |

**Verifier notes:** Closest on **statistical bias depth**; still not an MRM lifecycle workbench or OCC-structured validator.

---

### 4.7 Monitaur

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | Compliance-first AI governance |
| **Deployment** | Proprietary |
| **Target segment** | Insurance + FSI |
| **Framework claims** | NIST AI RMF, ISO 42001, EU AI Act — **33-control library** mapped to NAIC, Colorado, NY |
| **OCC 2026-13** | ❌ |
| **Bias/fair-lending** | ⚠ Automate Record drift/bias validations; not published statistical battery |
| **Adverse-action** | ❌ |
| **Audit log** | ✅✅ **Cryptographically signed, decision-level logs** — closest commercial analog to FINOS Tier 3 |
| **LLM/agentic** | ✅ Pre-deployment simulation + production monitoring |
| **Proof points** | ✅ Fortune 200 FSI case study (32-day policy, 8× project growth); Forrester Wave Strong Performer Q3 2025 |
| **Pricing** | Contact only; advisory bundling in some tiers |
| **Tech stack** | Integrates existing systems; evidence capture |

---

### 4.8 Credo AI

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | Enterprise AI governance backbone (policy/GRC) |
| **Deployment** | Proprietary |
| **Target segment** | Global enterprises — multi-framework |
| **Framework claims** | EU AI Act, NIST AI RMF, ISO 42001 — **GAIA policy packs**; Forrester Wave Leader Q3 2025 |
| **OCC 2026-13 / SR 26-2** | ❌ Not MRM-specific |
| **Bias/fair-lending** | ⚠ Risk assessments; defers deep testing to partners |
| **Adverse-action** | ❌ |
| **Audit log** | ⚠ Evidence workflows |
| **LLM/agentic** | ✅ Agent registry developing |
| **Proof points** | ✅ Forrester Wave Leader; Gartner MQ Visionary 2026 (listed, placement via secondary) |
| **Pricing** | Enterprise |

**Verifier notes:** Boardroom governance; not validation engine.

---

### 4.9 DataRobot

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | MLOps platform + AI governance module |
| **Deployment** | Proprietary; multi-cloud |
| **Target segment** | Enterprises with mixed AI portfolios |
| **Framework claims** | **Broadest multi-jurisdiction list found:** SR 11-7, EU AI Act, NYC LL144, Colorado SB21-169, CA AB-2013, NIST, EEOC |
| **OCC 2026-13** | ❌ |
| **Bias/fair-lending** | ⚠ Bias detection in platform; champion-challenger |
| **Adverse-action** | ❌ |
| **Audit log** | ⚠ Compliance documentation generation |
| **LLM/agentic** | ✅ Expanding |
| **Proof points** | Chartis 2024 report includes DataRobot; healthcare payer case study |
| **Pricing** | Contact only |

---

### 4.10 block/model-ledger (OSS reference)

| Dimension | Assessment |
| --------- | ---------- |
| **Category** | Model inventory + immutable event graph |
| **Deployment** | OSS (Apache 2.0); self-hosted |
| **Framework claims** | SR 11-7/SR 26-2, EU AI Act Annex IV, NIST — **validation profiles in code** |
| **Bias/fair-lending** | ❌ |
| **Adverse-action** | ❌ |
| **Audit log** | ✅ Immutable event log; MCP-native |
| **Proof points** | Early-stage (5 GitHub stars); active July 2026 releases |

**Verifier notes:** Architecture signal for inventory + tamper-evident change log; validates FINOS-aligned OSS demand.

---

## 5. Comparison matrix (top 10)

| Product | OSS? | Self-host? | OCC/SR MRM | ECOA adverse action | EU AI Act | NIST RMF | FINOS AIR | Bias stats depth | Audit tier 3 | LLM/agent | Pricing | Proof quality |
| ------- | ---- | ---------- | ---------- | ------------------- | --------- | -------- | --------- | ---------------- | ------------ | --------- | ------- | ------------- |
| ValidMind | No | Partial | ✅ Strong | ❌ | ✅ | ⚠ | ❌ | ⚠ | ⚠ | ✅✅ | $$$ | ✅✅ |
| SAS MRM | No | Yes | ✅ Strong | ❌ | ⚠ | ⚠ | ❌ | ⚠ | ⚠ | ⚠ | $$$$ | ✅✅ |
| Solytics | No | Yes | ✅ SR 26-2 | ❌ | ✅ | ⚠ | ❌ | ✅ | ✅ | ⚠ | $$$ | ⚠ |
| ModelOp | No | Yes | ✅ Templates | ❌ | ✅ | ✅ | ❌ | ⚠ | ⚠ | ✅ | $$$ | ✅ |
| Fiddler | No | VPC | ⚠ SR 11-7 | ⚠ SHAP only | ✅ | ⚠ | ❌ | ✅ prod | ⚠ | ✅✅ | $$ tiered | ✅ |
| Holistic AI | No | ? | ❌ | ⚠ | ✅ | ✅ | ❌ | ✅✅ | ⚠ | ✅ | $$$ | ✅ |
| Monitaur | No | ? | ⚠ | ❌ | ✅ | ✅ | ⚠ closest | ⚠ | ✅✅ crypto | ✅ | $$$ | ✅✅ |
| Credo AI | No | ? | ❌ | ❌ | ✅✅ | ✅✅ | ❌ | ⚠ | ⚠ | ✅ | $$$$ | ✅✅ |
| DataRobot | No | Yes | ✅ | ❌ | ✅✅ | ✅ | ❌ | ⚠ | ⚠ | ✅ | $$$ | ✅ |
| model-ledger | **Yes** | **Yes** | ⚠ profiles | ❌ | ⚠ | ⚠ | ⚠ | ❌ | ✅ events | ⚠ | Free | ⚠ early |

**Legend:** ✅ = explicit public evidence | ⚠ = partial/indirect | ❌ = not found | $$$ = enterprise contact-sales

---

## 6. What's commodity vs. missing

### Commodity (do not rebuild — integrate or match UX patterns)

- Model inventory with metadata, owner, tier, lifecycle stage
- Approval workflows with role-based gates
- Drift/performance dashboards (PSI, accuracy decay)
- SHAP/LIME explainability for tabular models
- Fairness metrics (demographic parity, DIR) via Fairlearn/Aequitas
- Multi-framework policy checklists (EU AI Act, NIST, ISO 42001)
- GRC evidence export PDFs

### Partially covered (differentiate on **structure and specificity**)

- SR 11-7 / MRM validation reports — many vendors, but **not OCC 2026-13 seven-section structure**
- Materiality-based tiering — Solytics/ValidMind narrate SR 26-2; **no open reference implementation**
- Agentic governance — crowded (ValidMind, ModelOp, Holistic, Fiddler) but regulatory ground unsettled

### Genuinely missing (Workbench differentiation candidates)

1. **Unified model-agnostic validation engine** — ingest arbitrary sklearn-compatible model + labeled CSV/Parquet; run full battery without enterprise platform lock-in
2. **OCC 2026-13 seven-section report generator** — literal section mapping (I–VII), not three-pillar retrofit
3. **ECOA adverse-action translator** with **Circular 2026-03 mapping methodology artifact** (auditable factor→reason pipeline)
4. **Post–July 2026 proxy-discrimination test suite** as primary federal fair-lending statistical layer (see R-02)
5. **FINOS AIR-DET-021 tiered audit trail** implemented and cited by control ID (mi-21) — Monitaur closest commercially; none cite FINOS
6. **FINOS bias-testing gap** — no ri-16 statistical mitigation in AIGF catalogue (foundation §3.5 confirmed)
7. **Open, inspectable, portfolio-scale demo** — end-to-end lifecycle on public data without six-figure procurement

---

## 7. Architectural patterns observed (feeds R-06, R-07)

| Pattern | Who does it | Workbench implication |
| ------- | ----------- | --------------------- |
| **Governance + monitoring split** | ValidMind + Fiddler; ModelOp + Arthur | Plan modular architecture; validation core + optional monitoring adapter |
| **System of record** | ModelOp, Monitaur | Inventory schema is table stakes |
| **Policy-as-code** | ValidMind, ModelOp | Aligns with stakeholder choice B (LLM extensibility) |
| **In-VPC evaluation** | Fiddler Trust Models | Important for FSI; defer for portfolio demo |
| **Python SDK + notebooks** | ValidMind, NIMBUS, Fairlearn ecosystem | **Confirms Python-centric core hypothesis** (pending R-07) |
| **MCP-native governance** | model-ledger, open-eago, FINOS direction | Extensibility path for agent tier without v1 scope creep |

---

## 8. Preliminary recommendations (actionable — refined in R-09)

1. **Do not compete on enterprise GRC breadth** — Credo/ServiceNow/IBM own that layer.
2. **Do compete on integrated validation depth** at portfolio/demo scale: tier → validate → bias/proxy test → adverse-action → audit log → seven-section report.
3. **Primary differentiator (pending R-03/R-04):** statistical fair-lending + adverse-action pipeline, structured for **post–Reg B July 2026** (proxy-first federal framing + FHA/state overlays).
4. **Secondary differentiator:** OCC 2026-13 report structure + FINOS mi-21 tiered audit trail — **no vendor cites FINOS tiers explicitly**.
5. **Compose, don't rebuild:** Fairlearn/Aequitas (metrics), SHAP (attribution), optional model-ledger patterns (inventory events).
6. **LLM/agent path (choice B):** Design FINOS tier interfaces (0–3) in audit module; implement Tier 1–2 for v1 demo; document Tier 3 crypto trail as build target; do not claim gen-AI MRM regulatory completeness.
7. **Stack hypothesis (preliminary):** Python validation core confirmed by competitive norm; final confirmation in R-07.

---

## 9. Sources

| ID | Source | Access | Date |
| -- | ------ | ------ | ---- |
| S-01 | Chartis MRM 2024 report (Genpact PDF mirror) | ⚠ Secondary | 2026-07-20 |
| S-02 | Gartner MQ AI Governance Platforms press/analyst secondary | ⚠ | 2026-07-20 |
| S-03 | ValidMind product brief + Chartis graphics | ✅ | 2026-07-20 |
| S-04 | SAS Chartis 2024 press release | ✅ | 2026-07-20 |
| S-05 | Solytics MRM Vault / SR 26-2 whitepaper | ✅ | 2026-07-20 |
| S-06 | ModelOp.com | ✅ | 2026-07-20 |
| S-07 | Fiddler AI GRC + FSI datasheet | ✅ | 2026-07-20 |
| S-08 | Holistic AI / Fronterio comparison | ⚠ Secondary | 2026-07-20 |
| S-09 | Monitaur platform + case studies | ✅ | 2026-07-20 |
| S-10 | aicompliancevendors.com MRM ranking | ⚠ Secondary aggregator | 2026-07-20 |
| S-11 | getaigovernance.net expert guide | ⚠ Secondary | 2026-07-20 |
| S-12 | FINOS AIGF GitHub + press | ✅ | 2026-07-20 |
| S-13 | block/model-ledger GitHub | ✅ | 2026-07-20 |
| S-14 | Fairlearn + Aequitas GitHub | ✅ | 2026-07-20 |

---

## 10. Open questions for later tickets

- R-03: Which fairness metrics survive Reg B shift as **primary** federal tests?
- R-06: Hash-chained log design — Monitaur commercial pattern vs. model-ledger OSS vs. greenfield
- R-07: Confirm Python stack against Holistic/ValidMind integration patterns
- R-09: Final scope boundary after methodology tickets complete
