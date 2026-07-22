# AI Model Risk & Governance Workbench — Research Foundation v2

**Status:** Greenfield. No repo, no code, no committed scope yet.
**Prepared:** 2026-07-20, by Claude (background session), for Steven Sorenson.
**Supersedes:** `RESEARCH_FOUNDATION.md` (v1), kept in this directory as a record of what changed and why — not for reuse.

> **⚠ Supersession notice (added 2026-07-22, AC0 messaging amendment):** This document is frozen as a launch-pad/historical artifact; its body is not mutated by this notice (R-14 §6 P2) and is excluded from the project's automated messaging-hygiene scan. Two corrections apply to the body below: (1) §3.2's claim that "Circular 2026-03" reaffirms the withdrawn 2022-03/2023-03 circulars is **❌ unsupported** — a dedicated primary-source search (`research/findings/R-12-circular-2026-03-primary-verification.md`) found no such circular on CFPB.gov or in the Federal Register; treat it as unverified, not current CFPB authority. (2) The "Reg B July 2026 narrowing" scope described in §3.2 is superseded by `research/findings/R-02-reg-b-july-2026-verification.md`. **Shipping authority for this project is `deep-research-v1.md` plus `research/findings/R-01` through `R-14` — not this document.** See `research/findings/R-12-circular-2026-03-primary-verification.md` and `research/findings/R-14-r12-r13-closeout-amendment-proposal.md` for full detail.

## 0. Purpose and Scope of This Document

This is the reference document a deep-research pass should be launched _from_, not the deep research output itself. It exists to keep first-principles decisions about architecture, tech stack, and implementation approach rooted in regulatory truth and trusted technical reference material — not in career positioning, hiring-market signal, or the incidental tech choices of unrelated prior projects.

**v2 deliberately excludes, by design decision, three categories of content that were present in v1:**

1. **Job postings, role/hiring-market research, and comp data.** Whether a design choice happens to resemble something in a job posting is not a valid reason to make that choice. The governing test for every requirement in this document is regulatory/standards grounding, not resume alignment.
2. **Any reference to the builder's existing portfolio projects** (a CRE underwriting platform, a Medicare Advantage risk dashboard) or their technology choices. Those projects' stacks were chosen for different problems under different constraints; carrying them forward by default would be convenience bias, not a first-principles conclusion. If the finished Workbench later validates an external model as a demonstration case, that's a build-time decision to make once real requirements are known — not something this foundation document should presuppose.
3. **Unverified competitor/vendor names.** None of the research behind this document actually investigated the existing AI-governance/model-risk-management tooling market. Naming specific companies without having researched them would plant guesses that could bias the real research. Instead, §7 below is a strategy for conducting that research properly.

**Source tiering used throughout this document:**

- **Tier 1 — Core regulatory and standards truth.** Binding or quasi-binding guidance from regulators (OCC/Fed/FDIC, CFPB) and the two standards bodies whose frameworks are specific and citable enough to build software against by control ID (NIST AI RMF, FINOS AI Governance Framework). This is the ground truth the Workbench's requirements derive from.
- **Tier 2 — Implementation and architecture signal.** Practitioner/technical sources (FinRED, a Databricks engineering blog, Microsoft Research's AgentRx) that don't carry regulatory authority but offer concrete, checkable patterns for _how_ to build against Tier 1's requirements.
- **Tier 3 — Competitive and prior-art landscape.** Not yet researched. §7 is the strategy for closing this gap in the next research pass, before architecture is finalized.

---

## 1. What This Project Is

**One-line pitch:** A model-agnostic tool that ingests a deployed AI/ML model plus a labeled dataset and runs it through a structured, documented model-risk-management lifecycle — risk-tiering, challenger-model comparison, statistical bias/fair-lending testing, drift monitoring, auto-generated validation reports, and ECOA/Reg-B-compliant adverse-action explanation generation — operationalizing model-risk guidance and regulatory frameworks as working software instead of a policy PDF.

**Who the software's user is:** a risk/compliance/model-validation/auditor function in a regulated industry such as our primary demographic, financial services (banking, lending, fintech, investing, trading, FP&A), and more broadly, healthcare, life sciences, industrial / manufacturing, technology, etcetera. The output is a validation report and an audit trail, not for example a credit decision. This is deliberately the _auditor of_ regulated models, not for example a lending tool.

**Why this problem, specifically:** two independent, verifiable facts make this a live rather than a settled problem, which matters because a live gap is where a well-reasoned, from-scratch attempt has genuine value rather than just replicating a known-good answer:

- US bank model-risk guidance was substantially rewritten in April 2026 (see §4.1), and its own text explicitly excludes generative and agentic AI from scope, with a regulator-promised follow-up (an RFI) that — as of this document's date, 2026-07-20 — **still has not been issued.** The rules for exactly the kind of AI system most people mean when they say "AI" today do not yet exist for US banks.
- Fair-lending explainability law (ECOA/Reg B) is stable and long-standing, but its application to "black box" model outputs remains an active compliance problem lenders are still visibly getting wrong (see §4.2) — this is not a solved translation problem with an off-the-shelf answer.

---

## 2. Why This Problem Is Real and Unsolved (Market Context)

Kept brief and clearly separated from the regulatory core below — this is "why does this matter" context, not requirements-bearing material.

- McKinsey (_State of AI Trust in 2026_, fielded Dec 2025–Jan 2026, ~500 organizations with respondents holding direct AI governance/risk/investment responsibility): 88% of organizations use AI in at least one function, 72% use generative AI — but only **6%** qualify as "high performers" (≥5% EBIT impact from AI), and only 39% report any enterprise-level EBIT impact. Nearly two-thirds of leaders cite security/risk concerns — ahead of regulatory uncertainty or technical limitations — as the top barrier to scaling agentic AI. 51% report at least one negative AI consequence, most commonly inaccuracy (~30%). A "responsible AI maturity" score in the same report sits at only 2.3 (up from 2.0 in 2025), with roughly 30% of organizations having mature strategy/governance/agentic controls.
- MIT Project NANDA (150 executive interviews, 350-employee survey, 300 public deployment analyses; "The GenAI Divide," Aug 2025): 95% of generative AI pilots show no measurable P&L impact. Root cause is integration failure and workflow misalignment, not model quality. More than half of GenAI budgets go to sales/marketing tools, while the biggest measured ROI is in back-office automation.
- Gartner: roughly 50% of generative AI projects are abandoned after proof-of-concept, citing poor data quality, inadequate risk controls, escalating cost, and unclear business value (Gartner, "Why Half of GenAI Projects Fail"). Separately, and more concretely sourced: Gartner's June 25, 2025 press release projects **over 40% of agentic AI projects will be canceled by the end of 2027**, over escalating costs, unclear business value, and inadequate risk controls (based on a January 2025 poll of 3,412 webinar attendees on AI investment posture).
- Deloitte (_State of AI in the Enterprise_, 3,235 leaders, Aug–Sept 2025 fielding, 24 countries, 6 industries): only about **one in five** organizations report a mature governance model for autonomous/agentic AI, even though 85% expect to customize agents for their business; an AI skills gap is cited as the single biggest adoption barrier.
- Bain ("CFOs Funded the AI Revolution. Now They're Joining It."): 56% of CFOs are increasing AI investment more than 15% this year, but only **31%** rate AI outcomes in finance as "strongly positive" (rising to 41% among fully-scaled deployments, >60% among top-quartile-mature organizations). Only **15–25%** of finance organizations have scaled AI into full production; the rest are stuck in pilot or limited production. Bain frames the core barrier as **"workflow debt"** — AI bolted onto unchanged processes rather than genuine workflow redesign.

**Synthesis:** across every source checked, the consistent finding is that the bottleneck is governance, integration, and trust infrastructure — not model capability. That is the market fact this project is built to address, and it's a fact about enterprise AI governance broadly, not about any particular hiring market.

---

## 3. Tier 1 — Core Regulatory and Standards Foundation

This is the load-bearing section of the document. Everything below was checked against primary text — direct PDF extraction of the actual regulatory documents and the standards bodies' own source repositories, not secondary summarization — with corrections noted inline where an earlier pass or a secondary source turned out to be wrong or stale.

### 3.1 US Bank Model Risk Management — OCC Bulletin 2026-13 / Fed SR 26-2 (April 17, 2026)

Confirmed by direct extraction of the actual 12-page interagency guidance PDF, issued jointly by the OCC, Federal Reserve, and FDIC.

**What's rescinded:** SR 11-7 (2011), OCC Bulletin 2011-12, the Comptroller's Handbook MRM booklet, OCC Bulletin 1997-24 (credit scoring), OCC Bulletin 2021-19 (BSA/AML models), plus FDIC-specific FIL-22-2017 and FIL-27-2021.

**Structure changed from "three pillars" to seven named sections:** I. Introduction, II. Purpose and Scope, III. Overview of Model Risk and MRM, IV. Model Development and Model Use, V. Model Validation and Monitoring, VI. Governance and Controls, **VII. Vendor and Other Third-Party Products** (newly elevated to its own standalone section — a real structural change from SR 11-7, where vendor risk was folded into the existing pillars). Most existing SR-11-7-era tooling in the market is still built around the old three-pillar mental model; a report generator structured around these actual seven sections is a legitimate, citable differentiator.

**Model definition narrowed (verbatim):**

> "the term 'model' refers to a complex quantitative method, system, or approach that applies statistical, economic, or financial theories to process input data into quantitative estimates. The term 'model' in this guidance excludes simple arithmetic calculations, such as those found within spreadsheets, as well as deterministic rule-based processes and software where there are no statistical, economic, or financial theories underpinning their design or use."

Note "mathematical" was dropped from SR 11-7's original theory list. **Design implication:** an intake gate needs a complexity + theory-basis test ("is this a model under this definition?"), not just "does it produce a number."

**Applicability threshold:** most relevant to banks **>$30B in total assets**, with an explicit "may still apply to smaller institutions with significant model-risk exposure" carve-out — a materiality/proportionality standard, not a bright line.

**Materiality-based risk tiering (the core organizing mechanism, and the most directly implementable piece of this guidance):**

> "Model exposure refers to the significance of the model output to a banking organization's business decisions... can be quantitatively measured (e.g., by portfolio size)." Model purpose is "a qualitative consideration." **"Model purpose, together with model exposure, determines model materiality."**

This is a two-input (quantitative exposure × qualitative purpose) → materiality score → tiered-oversight-rigor model. Immaterial models get lighter treatment (identify + monitor for a future materiality trigger); material models get comprehensive rigor. This is directly implementable as a risk-tiering/scoring engine.

**Validation frequency was de-mandated, not fixed at "annual":**

> "The timing, nature, and frequency of validation activities vary based on model purpose, model methodology, frequency and scope of model changes, data limitations, and other practical constraints."

A separate 2025 OCC clarification (Bulletin 2025-26) had already walked back a common industry misreading that SR 11-7 required annual validation for community banks; the 2026 rewrite reinforces flexible, principles-based cadence. **Design implication:** a configurable cadence tied to materiality tier, not a hard-coded annual cron job.

**Effective challenge redefined around competence/independence/standing, not org-chart separation:**

> performed by individuals with "the appropriate expertise to conduct a critical and objective challenge, sufficient independence to maintain objectivity, as well as the organizational standing and influence to effect any change." Validation quality "depends on the rigor and effectiveness of the review rather than on organizational structure."

**Three named validation components** (map directly onto validation-report sections): Conceptual Soundness, Outcomes Analysis, Ongoing Model Monitoring.

**Vendor/third-party (new standalone Section VII):** sound practice = "developing an understanding of the vendor model, including its conceptual soundness, design, development data, and performance," plus ongoing monitoring/outcome analysis, plus — for customized vendor models — documenting and justifying the customization. Explicitly acknowledges banks often can't get vendor source code, and says the principles still apply regardless.

**Governance:** names "Model Inventory" (called "common industry practice," softly expected) and "Documentation" as explicit governance subcomponents.

**Non-enforceability is prominent and explicit:**

> "This guidance does not set forth enforceable standards or prescriptive requirements; accordingly, non-compliance with this guidance will not result in supervisory criticism against a banking organization" — with a footnote preserving authority to act on unsafe/unsound practices.

**The load-bearing gen-AI carve-out, verbatim (footnote 3 of the primary text):**

> "Generative AI and agentic AI models are novel and rapidly evolving. As such, they are not within the scope of this guidance. Nonetheless, a banking organization's risk management and governance practices should guide the determination of appropriate governance and controls for any tools, processes, or systems not covered in this document. However, the principles described in this guidance apply to traditional statistical and quantitative models and non-generative, non-agentic AI models."

**Correction worth flagging:** the RFI commitment mentioned in regulator press coverage does **not** appear anywhere in the 12-page guidance PDF itself — it's a policy-announcement artifact from the OCC's press release, not part of the operative document. And as of 2026-07-20, **no RFI has actually been published yet.** This is the open regulatory gap referenced in §1 — genuinely open, not a formality about to close.

**A stale-pointer correction, in case a future research pass relies on it:** the Federal Reserve's guidance page previously cited as "the original SR 11-7 text" now serves the 2026 rewrite's content in place, not the 2011 original. Treat SR 11-7 as historical/superseded going forward.

### 3.2 CFPB / ECOA / Regulation B — Adverse Action Explainability

**Statutory anchor (stable, unaffected by guidance churn):** ECOA §701(d), 15 U.S.C. §1691(d)(2)-(3); Regulation B, 12 CFR §1002.9(a)(2)(i), (b)(2). Creditors must give applicants **specific** principal reasons for adverse action.

There are two relevant CFPB circulars: **2022-03** (May 26, 2022), "Adverse action notification requirements in connection with credit decisions based on complex algorithms," and **2023-03** (Sept 19, 2023), which explicitly builds on 2022-03. Both were withdrawn May 12, 2025 (Federal Register notice 2025-08286, part of a 67-document deregulatory withdrawal) and substantively reaffirmed by **Circular 2026-03** (May 5, 2026) — requiring lenders to **document how model outputs are translated into consumer-facing explanations "so fair lending reviewers can independently validate the reasoning."** The underlying statute never moved; only the guidance's administrative status fluctuated.

**What actually makes a reason "specific" vs. insufficient** (pulled verbatim from the 2023-03 PDF — this is the most directly implementable source for the adverse-action module):

- Reasons must "relate to and accurately describe the factors actually considered or scored by a creditor."
- The sample-form checklist is **not** automatically sufficient: "creditors may not rely on the checklist of reasons provided in the sample forms... if those reasons do not specifically and accurately indicate the principal reason(s)... Nor... may creditors rely on overly broad or vague reasons to the extent that they obscure the specific and accurate reasons relied upon."
- Regulation B's own official commentary example: disclose "insufficient bank references," not "insufficient credit references," if only bank/depository references were actually considered.
- Explicit insufficient-reason examples given by CFPB: "insufficient projected income" (insufficient if the real driver was the applicant's profession); "purchasing history" or "disfavored business patronage" for a credit-line reduction (insufficient — must disclose the type of establishment, location, goods purchased, or other relevant considerations).
- Black-box holding: "adverse action notice requirements apply equally to all credit decisions, regardless of whether the technology used to make them involves complex or 'black-box' algorithmic models... that creditors may not understand sufficiently to meet their legal obligations."

**Design implication for the adverse-action module:** it needs (1) a mapping from raw model feature contributions (e.g., SHAP-style attribution) to natural-language factor descriptions specific enough to survive the "purchasing history" insufficiency test, (2) an audit record proving the disclosed reason maps to what was _actually scored_ rather than the nearest checklist category, and (3) a documented, independently-reviewable translation methodology as its own artifact, per the 2026-03 requirement.

One flagged-unverified claim from a secondary source: a supposed July 2026 Reg B narrowing — the source itself labels this "unverified" and it could not be corroborated elsewhere. Do not build on it without independent confirmation.

### 3.3 EU AI Act — Annex III Credit Scoring

**Annex III point 5(b), verbatim:** AI systems "intended to be used to evaluate the creditworthiness of natural persons or establish their credit score, with the exception of AI systems used for the purpose of detecting financial fraud."

**Timeline correction:** the standalone Annex III high-risk compliance deadline for credit scoring was delayed from August 2, 2026 to **December 2, 2027** by the EU Digital Omnibus (approved by Parliament and Council, June 2026). Article 50 transparency obligations (AI-generated content labeling, AI-interaction disclosure) still apply from the original August 2, 2026 date. This means the EU angle is a documentation-standard-to-build-toward, not a near-term forcing function — worth naming precisely for credibility, since most existing tooling in this space likely hasn't caught up to the revised date.

**Article-to-feature mapping:**

| Article    | Title                                           | Feature implication                                                                             |
| ---------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Art. 9     | Risk Management System                          | Ongoing risk-register/review workflow tied to the model                                         |
| Art. 10    | Data and Data Governance                        | Training/validation/test data lineage; bias examination for direct + proxy discrimination       |
| Art. 11    | Technical Documentation (Annex IV)              | Structured doc generator — architecture, training method, performance, limitations              |
| Art. 12    | Record-Keeping (automatic logging)              | The audit-log article — see §3.5 for the direct implementation standard                         |
| Art. 13    | Transparency to Deployers                       | Model card / instructions-for-use artifact                                                      |
| Art. 14    | Human Oversight                                 | A human who can understand and override the score, not a rubber stamp — override workflow       |
| Art. 15    | Accuracy, Robustness, Cybersecurity             | Model validation / challenger-comparison module                                                 |
| Art. 26(5) | Deployer obligations                            | Monitoring duty sits on the bank/lender, not just the vendor                                    |
| Art. 27    | Fundamental Rights Impact Assessment (deployer) | Pre-deployment FRIA workflow                                                                    |
| Art. 43    | Conformity Assessment                           | Self-assessment appears permitted for Annex III credit scoring (worth independent confirmation) |
| Art. 49    | EU Database Registration                        | Registration record/checklist                                                                   |
| Art. 72    | Post-market monitoring                          | Feeds directly into the drift-monitoring module                                                 |

**Provider vs. deployer split, and why it matters for scoping:** providers (model builders) own Arts. 8–17 plus conformity assessment and registration; deployers (a bank using a purchased or in-house model) own human oversight, the FRIA (Art. 27), staff training, and monitoring (Art. 26(5)). The Workbench's realistic target user — a bank running its own or a vendor's model — is principally a **deployer**. This argues for scoping primarily to Arts. 26, 27, 14, and deployer-side monitoring, not full provider-side conformity-assessment tooling.

### 3.4 NIST AI Risk Management Framework

**Top-tier reference — vendor-neutral, implementation-agnostic, and explicitly designed to be operationalized rather than narrated.** Confirmed dates: AI RMF 1.0 — January 26, 2023. Generative AI Profile (NIST AI 600-1) — July 26, 2024. A Critical Infrastructure Profile concept note was released April 7, 2026 (confirmed real).

Full verbatim subcategory tables were extracted directly from the primary PDF (NIST.AI.100-1.pdf, Tables 1–4) across the framework's four functions — Govern, Map, Measure, Manage (19/18/22/13 subcategories respectively). These are checklist-grade and map close to 1:1 onto Workbench features. The subcategories most directly relevant to this project:

- **MEASURE 2.9:** "model explained/validated/documented, output interpreted in context" → the validation-report module.
- **MEASURE 2.11:** "fairness and bias evaluated, results documented" → the bias-testing module.
- **MEASURE 2.6:** "safety evaluated regularly, residual risk within tolerance, fail-safe" → risk-tiering/materiality engine.
- **MANAGE 4.1:** "post-deployment monitoring plans implemented (incl. appeal/override, decommissioning, incident response, change management)" → drift-monitoring + governance workflow.
- **GOVERN 1.6:** "mechanisms in place to inventory AI systems" → model inventory.

The full subcategory tables are long enough that they belong in a dedicated implementation checklist once the repo exists (e.g. `docs/nist-ai-rmf-checklist.md`) rather than inline here — but they are the single best raw material available for a literal, defensible feature checklist, and should be pulled from the primary PDF directly (`nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf`) rather than a secondary summary.

### 3.5 FINOS AI Governance Framework — AIR-DET-021

**Top-tier reference, and the single most implementation-critical source in this document.** FINOS (Fintech Open Source Foundation, part of the Linux Foundation) publishes an open, numbered AI Governance Framework — a rare thing: a citable, financial-industry-specific technical standard a solo builder can actually implement against by control ID, rather than a vague "best practices" claim.

**Full tier definitions, extracted verbatim from the primary source** (`docs/_mitigations/mi-21_agent-decision-audit-and-explainability.md` in the FINOS `ai-governance-framework` repository):

> **Tier 0 — Zero Data Retention.** For low-stakes applications with human oversight. Controls: an Architecture Decision Record justifying minimal retention; basic infra-level security logging (auth/authz failures); human-in-the-loop replaces detailed audit trails; emphasis on preventing data leakage over decision reconstruction.
>
> **Tier 1 — Basic Flow Reconstruction.** For moderate-stakes applications, dev/test environments. Controls: log data/prompt flows to enable reproduction in lab environments; capture input sources, timestamps, tool invocations without detailed reasoning; record final decisions/outcomes; reconstruct "what happened" without "why" — sufficient for debugging/root-cause analysis.
>
> **Tier 2 — Explicit Reasoning Generation.** For production systems with significant business impact, regulated activities, customer-facing decisions. All Tier 1 controls, plus: explicit reasoning generated and logged in advance of tool calls; natural-language explanations of decision logic; confidence scoring and alternative analysis where feasible. _Caveat stated on the same page: this tier incurs extra generation cost, and reasoning may be incomplete if the model provider hides internal reasoning tokens (e.g., OpenAI o1-class models) — "organizations using these models cannot achieve full Tier 3 compliance and should document this limitation in their ADR."_
>
> **Tier 3 — Comprehensive Audit Trail.** For high-risk financial transactions, regulatory compliance scenarios, fully autonomous systems, safety-critical applications. All Tier 1+2 controls, plus: detailed decision-reasoning documentation including logical flow/decision trees; complete contextual capture (customer, business, risk, temporal context); **cryptographic protection and tamper-evident logging**; full regulatory compliance integration; real-time monitoring and anomaly detection.

**The EU AI Act Article 12 bridge, verbatim from the same source:**

> "Technical Requirement under Article 12(1): High-risk AI systems must technically allow automatic recording of events over the system lifetime. Tier 3 audit trail implementations described in this mitigation directly satisfy this requirement; Tier 0 and Tier 1 do not meet the threshold for systems classified as high-risk under Annex III."

Further mapping: Art. 12(2)(a) → capture "guardrail violations, exception paths, and decision boundary crossings"; Art. 12(2)(b) → capture "aggregate behavior metrics, drift indicators, performance over time" (feeds §3.3's Art. 72 post-market monitoring); Art. 12(2)(c) → capture "human review touchpoints, oversight interventions, operational decisions." Critically: **"Article 26(5) places monitoring obligations on the deployer... not only on the provider. Audit trail design must expose appropriate records to deployer audit interfaces, not only to provider-side observability"** — reinforcing the deployer-scoping conclusion from §3.3.

**Tamper-evidence, not just tamper-resistance:** the framework distinguishes the two and recommends "cryptographic hash chaining, signed log segments, or anchoring digests to an append-only transparency log" to raise integrity "from operator-asserted to independently auditable" — a concrete technical direction for the audit-log implementation, independent of any particular tech-stack choice.

**Explicit fair-lending tie-in:** "Ensure decision audit trails support fair lending analysis and regulatory examination requirements."

**Mitigation metadata (machine-checkable):** ID mi-21, type DET (detective control). Mitigates ri-24 (Agent Action Authorization Bypass), ri-25 (Tool Chain Manipulation and Injection), **ri-22 (Regulatory Compliance and Oversight)**. Related mitigations: mi-4 (AI System Observability), mi-11 (Human Feedback Loop). Cross-references ISO 42001, EU AI Act Arts. 12/26/72/13/86, NIST SP 800-53r5 AU-2/AU-3/AU-6/CA-7, IOSCO Supervisory Toolkit.

**Adjacent mitigations worth building against** (the full FINOS catalogue has only 23 mitigations total):

| ID    | Title                                     | Relevance                                                                                                                                                |
| ----- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| mi-4  | AI System Observability                   | Logging/monitoring backbone; explicitly lists fairness/bias/explainability monitoring; mitigates ri-19 (Data Quality and Drift)                          |
| mi-5  | System Acceptance Testing                 | Pre-deployment validation gate; explicitly calls for "diverse demographic data to test for fairness and bias"; mitigates ri-16 (Bias and Discrimination) |
| mi-11 | Human Feedback Loop for AI Systems        | Mitigates ri-16 directly; ties to EU AI Act Art. 14 — the human-override/appeal workflow                                                                 |
| mi-6  | Data Quality Classification & Sensitivity | Data governance foundation, maps to Art. 10                                                                                                              |
| mi-10 | AI Model Version Pinning                  | Challenger-model comparison / versioning                                                                                                                 |
| mi-15 | LLM-as-a-Judge (Automated Evaluation)     | Potential validation-report automation technique                                                                                                         |

**A real gap in FINOS's own catalogue, worth exploiting:** there is **no dedicated statistical bias/fairness-testing mitigation.** Bias/Discrimination (ri-16) is addressed only indirectly via mi-11 (human feedback) and mi-5 (acceptance testing) — no disparate-impact-ratio / adverse-impact-analysis control exists in their catalogue. This is a legitimate, citable differentiation angle for the Workbench: FINOS covers audit/explainability comprehensively but treats bias testing as an afterthought of human review; a dedicated statistical fair-lending testing module fills a gap the standard itself doesn't yet specify.

**Two FINOS reference use-cases directly on point** (found in the repo structure, worth pulling into the research base as primary material, not secondary commentary):

- `uc-1_credit-risk-analysis.md` — "An agent that performs credit risk analysis for small business loan applications." Names ri-1 (info leakage), ri-4 (hallucination), ri-17 (lack of explainability), ri-19 (data quality/drift) as its risks; explicitly flags ECOA/Fair Lending and SR 11-7 as regulatory concerns; classifies itself EU AI Act high-risk under Annex III.
- `uc-3_loan-approval.md` — a full multi-agent loan-approval reference workflow (intake → fraud detection → credit risk → decisioning → pricing → human review → e-signature → disbursement). States explicitly: **"Consistency is enforced by the deterministic policy gates rather than by the AI agents themselves"** — i.e., FINOS's own reference architecture puts AI in an advisory role behind deterministic policy logic for lending decisions. This is a defensible, standards-body-endorsed design precedent independent of any prior project.

**Note on state-level law:** FINOS's own risk documentation for ri-22 flags that state-level AI laws (e.g., the Colorado AI Act, California DFPI automated-decision rules) may fill part of the federal gap left open by §3.1's gen-AI/agentic-AI carve-out. This thread was not independently researched for this document and is flagged as an open question in §8.

### 3.6 Cross-Framework Control Mapping (synthesis)

A single Workbench feature typically satisfies several Tier 1 frameworks' requirements at once:

| Workbench Feature                                                | OCC 2026-13                        | EU AI Act                  | NIST AI RMF            | FINOS AIR                  |
| ---------------------------------------------------------------- | ---------------------------------- | -------------------------- | ---------------------- | -------------------------- |
| Model inventory + materiality/risk-tiering engine                | §VI Governance & Controls          | Art. 9 (risk mgmt system)  | GOVERN 1.6             | —                          |
| Validation report (conceptual soundness / outcomes / monitoring) | §V Model Validation and Monitoring | Art. 11, 15                | MEASURE 2.9            | mi-5                       |
| Statistical bias/fair-lending testing                            | (implied via risk assessment)      | Art. 10                    | MEASURE 2.11           | **gap — differentiator**   |
| Adverse-action reason-code translator                            | (ECOA/Reg B, not MRM itself)       | Art. 13                    | MEASURE 2.9            | —                          |
| Drift monitoring dashboard                                       | §V ongoing monitoring              | Art. 72                    | MANAGE 4.1             | mi-4                       |
| Tamper-evident audit log                                         | (implied via documentation)        | Art. 12                    | GOVERN 4.2             | **mi-21 (primary target)** |
| Human override/escalation workflow                               | §VI governance                     | Art. 14                    | GOVERN 3.2, MANAGE 4.1 | mi-11                      |
| Vendor/third-party model tracking                                | §VII (new)                         | Art. 26(5) deployer duties | MAP 4.1                | —                          |

---

## 4. Tier 2 — Implementation & Architecture Signal

These three sources carry no regulatory authority — they are practitioner/technical sources that inform _how_ to build against Tier 1's requirements. Kept clearly separate so they're never mistaken for requirements themselves.

### 4.1 FinRED (arXiv 2606.19887, June 2026)

A finance-specific LLM red-teaming/evaluation benchmark, deployed in South Korea's Financial Security Institute (FSI) regulatory sandbox for evaluating generative-AI security countermeasures. Its central argument — general-purpose AI safety taxonomies check for surface features (e.g., presence of a disclaimer) rather than substantive, finance-specific harm, and explicitly miss threats named by FATF and EU DORA — is directly relevant if the Workbench's scope ever extends to evaluating LLM-based components (see the open scope question in §8).

**Two-level risk taxonomy** (directly reusable as a structure for any eval/red-team module):

- **Level 1 (5 categories):** R1 Cyber Threats, R2 Financial Crime, R3 Misinformation & Deception, R4 Consumer Rights Violation, R5 Financial ICT Compliance Evasion.
- **Level 2 (examples):** under R1 — digital authentication bypass, asset theft, APT intrusion; under R2 — voice phishing, electronic financial fraud, money-laundering assistance.

### 4.2 Databricks — "Model risk management in 2026: A banker's guide to the revised interagency guidance"

Vendor-authored engineering content — read its specific product claims as sales positioning, not regulatory fact — but it is the richest practitioner-level architecture source found, and its regulatory framing was independently verified against the primary OCC text.

**Lifecycle-to-evidence mapping**, directly reusable as a design pattern for what artifacts each stage of the model lifecycle should produce: data sourcing → lineage + data-quality metrics; feature engineering → feature version history; development → run history/hyperparameters/code commit; independent validation → versioned challenger artifacts + fairness metrics + validator sign-off bound to model version; deployment → promotion history + approver identity + rollback path; monitoring → drift dashboards + threshold breaches + alert history.

**Tier-gated approval logic as pseudocode:**

```
IF model.tier = 'Tier1' THEN
  require_approver_role IN ('MRM_Validator', 'Model_Risk_Committee')
  AND require_dual_control = TRUE
```

**Proposed inventory/log schema:** `models.inventory` (tier, owner, guidance_version, intended_use, dependent_processes), `models.validation_log` (validator_id, validation_scope, issues_found, residual_risk_rating), plus separate GenAI, monitoring, and evidence catalogs.

**Framing worth adopting:** generative/agentic AI is "formally out of scope but [should] inherit the principles" — supervisors and internal audit are already applying MRM expectations by analogy to LLM-based underwriting assistants and copilots even though the guidance's letter excludes them. This supports designing the Workbench's lifecycle stages to be _extensible_ to LLM-based components without claiming compliance-completeness for a category that has no rule yet.

### 4.3 Microsoft Research — AgentRx

A systematic root-cause debugging framework for AI agent failures, directly relevant to the audit-trail/monitoring module's design if the Workbench extends into agentic-component governance.

**Four-stage pipeline:** (1) trajectory normalization — standardizes heterogeneous agent logs; (2) constraint synthesis — auto-generates executable constraints from tool schemas and domain policies; (3) guarded evaluation — step-by-step constraint checking producing an auditable, evidence-backed violation log; (4) LLM-based judging — applies a grounded 9-category failure taxonomy to identify the "Critical Failure Step" (the first unrecoverable error in a trajectory).

Released with an open **AgentRx Benchmark** (115 manually annotated failed trajectories across three domains). Reported gains of +23.6% failure-localization accuracy and +22.9% root-cause-attribution accuracy over baselines; framework and dataset open-sourced.

**Relevance:** the "guarded evaluation → auditable violation log" pattern is a close architectural match for an audit-trail/monitoring module, and the constraint-synthesis-from-domain-policy approach is a natural way to encode model-risk/compliance rules (Tier 1's requirements) as executable checks against agent trajectories, rather than as manual review.

---

## 5. Tier 3 — Competitive & Prior-Art Landscape: Research Strategy

**This has not been researched yet.** No existing MRM/AI-governance vendor or open-source tooling was investigated in the work behind this document — the original source material didn't cite any, and inventing names here would plant unverified guesses into a document meant to keep decisions evidence-based. What follows is a strategy for closing this gap properly in the next research pass, before architecture is finalized.

**Why this matters:** the goal isn't to out-build enterprise vendors — it's to know precisely what's already commodity (don't rebuild it), what patterns are already standard (learn from them), and what's genuinely still missing (the actual differentiation opportunity, of which §3.5's identified FINOS bias-testing gap is one candidate lead, not the only one).

**Source categories to search, in roughly descending order of reliability:**

1. **Analyst market-category reports.** The relevant category names span more than one adjacent space and all should be checked: "AI Trust, Risk and Security Management (AI TRiSM)," "Model Risk Management software," "AI Governance Platforms," "Responsible AI platforms." Chartis Research specifically covers model-risk-management vendor landscapes for financial services (their RiskTech Quadrant reports) and is likely the single best-fit analyst source given this project's specific niche. Gartner/Forrester equivalents should also be checked, and the Evident AI Index (bank-specific AI governance/adoption scoring) is worth a direct look.
2. **Software marketplace/directory listings.** G2, Capterra, and TrustRadius category pages for the same category names above — useful for surfacing smaller/newer vendors that haven't yet made an analyst report, plus real user reviews that reveal what actually works vs. marketing claims.
3. **Open-source landscape.** GitHub topic search (`model-risk-management`, `ai-governance`, `responsible-ai`, `fairness-testing`, `bias-detection`) and "awesome-list" aggregators. Distinguish between full platforms and component libraries — e.g., bias/fairness-testing libraries (such as those implementing four-fifths-rule or disparate-impact-ratio testing) are a different category from full governance platforms, and the Workbench may end up building on top of one rather than competing with it.
4. **Standards-body ecosystem signal.** The FINOS AI Governance Framework's own contributor and member/adopter list is a strong, already-identified lead — companies actively contributing to or citing that framework are demonstrably active in exactly this space, and checking who they are is a natural first move given FINOS is already a Tier 1 source here.
5. **Financial trade press and specialist analyst outlets.** American Banker, Risk.net, and Chartis Research's own articles/vendor comparisons frequently name and compare specific products in this space.
6. **Academic and preprint literature.** arXiv search for "model risk management," "AI governance," and "credit scoring audit" survey papers often includes comparative tables of existing tools as related work — a fast way to get a vetted starting list.
7. **Funding/startup signal.** A funding-database search (Crunchbase, PitchBook, or a free equivalent) for companies tagged "AI governance," "model risk," "responsible AI," or "MLOps compliance" will catch early-stage players not yet covered by analyst reports.
8. **Conference talks and vendor whitepapers.** Industry conferences in this space (e.g., RiskMinds) and vendor-published whitepapers are a lower-trust but useful supplementary source for understanding how vendors position themselves and what claims they make.

**Evaluation criteria to apply once candidates are identified** (this becomes the actual comparison matrix the research pass should produce):

- Which specific regulatory frameworks does the product claim to cover — OCC/Fed MRM, ECOA/Reg B, EU AI Act, NIST AI RMF, FINOS AIR — and how specifically (control-ID-level, or vague "responsible AI" language)?
- Open-source vs. proprietary; self-hosted vs. SaaS-only.
- Target customer segment and size (enterprise-only vs. accessible to smaller institutions).
- Depth of statistical bias/fair-lending testing specifically — does it go beyond what FINOS's own framework covers (§3.5's identified gap), or is it similarly light on this?
- Does any product's audit-logging claims map to a specific named tier or standard (e.g., explicit FINOS AIR-DET-021 tier alignment) — likely none yet, since that mitigation is recent, but worth confirming rather than assuming.
- Real customer proof points and case studies vs. pre-launch/vaporware positioning.
- Pricing and licensing model, where discoverable.

**Expected output of this research pass:** a comparison matrix mapping each identified competitor across the criteria above, culminating in an explicit synthesis of what's not covered by anyone yet — that synthesis, not a guess, should be what drives the Workbench's final differentiation choice.

---

## 6. Open Strategic Questions — Deep-Research To-Do List

Organized by theme. §5 above is itself the first item on this list, already expanded into its own strategy; the remainder covers what's still open once competitive landscape is known.

### 6.1 Data & validation methodology

- **Dataset sourcing for the bias/fair-lending testing module.**
- Decide the specific statistical battery for bias testing: adverse impact ratio / four-fifths rule, standardized mean difference, disparate impact analysis by protected class — and how to handle the reality that US fair-lending law generally restricts direct use of protected-class data in the model itself (proxy-variable analysis, e.g. BISG-style race/ethnicity proxying methodology used by regulators, is its own research question).
- Decide the model-interpretability approach (e.g., SHAP-style attribution vs. alternatives) and how attribution output should feed the adverse-action reason-code translator from §3.2.
- Decide drift-detection methodology (e.g., population stability index, Kolmogorov-Smirnov test) and what should trigger a materiality-tier review escalation per §3.1's exposure×purpose model.

### 6.2 Architecture & tech stack — to be derived from requirements, not precedent

- Model ingestion interface scope: a narrow, well-defined contract (e.g., any model exposing a `.predict()`/`.predict_proba()`-style interface) versus broader format support (ONNX, pickled objects, API-based models). Decide based on what's needed to demonstrate the validation battery convincingly, not on what's easiest.
- The single highest-leverage scope decision: should the Workbench include a first-class path for LLM/agentic model components (per §4.2's "inherit the principles even though out of scope" framing and §3.5's FINOS AIR-DET-021 tiering), or stay scoped to traditional statistical/ML credit models for v1 with gen-AI governance as an explicit phase-2 extension? This is where the project's differentiation thesis is strongest but the regulatory ground is least settled (no RFI yet).
- Audit-log implementation: what does "cryptographic hash chaining / signed log segments / append-only transparency log" (§3.5) actually look like as a concrete, buildable design — a hash-chained log table with a periodically-anchored Merkle root, an existing tamper-evident log primitive, or something else? Evaluate options on their own technical merits against the FINOS requirement, not by default to a familiar tool.
- Report generation: should be structured around the actual OCC 2026-13 seven sections (§3.1) rather than a generic template — the specific technology for producing that report (templating approach, output format) should be chosen based on what best serves that structure and audit-report conventions in this domain, evaluated independently of any other project's prior choices.
- General stack-selection principle: the Python ecosystem's dominance in statistical/ML validation tooling (scikit-learn, XGBoost, SHAP, fairness-testing libraries, and the tooling referenced by NIST/FINOS's own ecosystem) is a legitimate, evidence-based starting hypothesis for the core validation engine — but this should be confirmed against what §5's competitive-landscape research finds real tools in this space actually built on, not assumed from convenience. Database, deployment, and framework choices around that core should follow from the system's actual read/write and audit-log requirements (closer to a batch/analytical workload with append-only logging needs than a high-throughput transactional one), not from familiarity.

### 6.3 Scope & differentiation

- Confirm the final v1 scope boundary between: (a) US bank MRM (OCC 2026-13) as the primary frame, (b) ECOA/Reg B adverse-action translation as a named, demoable module, (c) EU AI Act / FINOS AIR-DET-021 as a secondary "internationally-legible documentation standard" layer rather than a deadline-driven forcing function (per the corrected §3.3 timeline), (d) NIST AI RMF as the structural backbone tying the report/checklist together across frameworks.
- Decide whether the statistical bias-testing module (filling the FINOS gap identified in §3.5) should be the primary, deepest differentiator, or whether effort should spread more evenly across modules — informed by what §5's competitive research finds is actually missing in the market, not decided in isolation from that research.
- Research state-level AI/lending laws (Colorado AI Act, California DFPI automated-decision rules, NY DFS guidance) flagged by FINOS's own ri-22 documentation (§3.5) as potentially filling part of the federal gen-AI/agentic-AI regulatory gap — this could meaningfully change how the "regulatory gray zone" is framed if state law is further ahead than federal guidance in this specific space.

### 6.4 Execution sequencing

- Define MVP phasing: the smallest end-to-end slice that demonstrates the risk-tiering engine → validation report → bias test → adverse-action translator → audit log chain, before adding drift monitoring, dashboards, or gen-AI/agentic extensions.
- Define a specific, concrete demo scenario to build toward — e.g., ingest a toy model trained on public data, run the full lifecycle, and produce a validation report a risk/compliance practitioner would recognize as structurally matching OCC 2026-13's actual seven sections. Concrete enough to build a checklist against, independent of any external audience's specific expectations.

---

## 7. Research Methodology for the Deep-Research Phase

- **Primary sources first.** Regulator text and standards-body repositories, with direct document extraction preferred over AI-summarized fetches for any load-bearing quote — two genuine hallucinated quotes were caught this way during the verification pass behind this document, which is reason enough to always sanity-check against the actual source text before treating a quote as safe to build on.
- **Flag secondary sources explicitly** where primary isn't public, and note the gap rather than silently upgrading a secondary claim to load-bearing status.
- **Date everything and re-verify time-sensitive claims.** Regulatory deadlines can and did move materially between the original source material's date and this document's verification pass one day later (§3.3's EU deadline correction is a direct example). Anything reused from this document more than a few weeks old by the time building starts should get a fresh spot-check — §5's competitive landscape most of all, since it hasn't been checked even once yet.
- **Cross-corroborate statistics across at least two independent sources** before treating a number as safe to quote, and prefer tracing a widely-repeated figure back to its actual originating primary report over trusting whichever version is easiest to find (a widely-circulated but ultimately unsourced "89% agentic pilot failure" statistic, encountered and discarded during this document's verification pass, is a direct cautionary example).
- **Output format:** whatever the deep-research phase produces should stay structured enough to keep functioning as a living reference during build — headers matching the eventual architecture's modules, a source ledger, and explicit verified-vs-unverified labeling, matching this document's own convention.

---

## Appendix: Source Ledger

All Tier 1/Tier 2 sources referenced above, with verification status from the 2026-07-20 research pass. "✅" = fetched directly and confirmed against primary text. "⚠" = fetched but with a correction noted inline above.

**Tier 1 — Regulatory & standards primary sources:**

- ✅ OCC Bulletin 2026-13 (occ.treas.gov) + PDF attachment — full text extracted directly
- ⚠ Federal Reserve SR 11-7 guidance page — now serves 2026 content, not the 2011 original; treat as stale pointer
- ✅ Fed SR 26-2 archive page
- ✅ Sullivan & Cromwell, Orrick, Davis Polk law-firm memos on the 2026 rewrite (secondary, cross-corroborated against primary text)
- ⚠ CFPB Circular 2023-03 PDF, Circular 2026-03 coverage — verbatim insufficiency examples extracted; note two distinct predecessor circulars (2022-03 and 2023-03) exist
- ✅ CFPB 2025 withdrawal notice (67 docs, FR 2025-08286, May 12 2025)
- ⚠ EU AI Act Annex III text — deadline correction applies (Dec 2, 2027, not Aug 2, 2026)
- ❌ EBA gap-analysis PDF — high-level memo, not a technical-requirements document; not used for article-level detail
- ✅ NIST AI RMF 1.0 PDF (NIST.AI.100-1.pdf), Generative AI Profile (NIST.AI.600-1.pdf) — full subcategory tables extracted directly
- ✅ FINOS AIR-DET-021 (finos.org + GitHub raw source) — full tier definitions extracted directly; two adjacent use-cases (uc-1, uc-3) discovered via repo structure

**Tier 2 — Implementation/architecture signal:**

- ✅ FinRED (arXiv 2606.19887) — full taxonomy extracted
- ⚠ Databricks practitioner blog — regulatory framing verified against primary text; treat specific product claims as vendor positioning
- ✅ Microsoft Research AgentRx blog — substance fully captured

**Market/adoption context (§2 only, kept brief and separate from the regulatory core):**

- ✅ McKinsey State of AI Trust 2026
- ⚠ MIT NANDA/Fortune coverage — some cited figures (specific payback-period numbers) could not be confirmed and were excluded from this document
- ⚠ Gartner GenAI-failure article and press release — one widely-circulated figure ("89% of agentic pilots fail") was checked and found unsourced, and is excluded; the 40%-cancellation-by-2027 figure is confirmed to a primary Gartner press release and is the one used in §2
- ⚠ Deloitte State of AI in the Enterprise 2026 — governance-maturity figure corrected to "~1 in 5," not a precise 21%
- ✅ Bain, "CFOs Funded the AI Revolution"
