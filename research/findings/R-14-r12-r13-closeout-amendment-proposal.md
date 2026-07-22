# R-14 — Close-Out of R-12/R-13 Open Questions + Document Amendment Proposal

**Ticket:** R-14  
**Session:** ad hoc (post–Session 6 diligence)  
**Status:** Complete  
**Research date:** 2026-07-21  
**Depends on:** R-12, R-13  
**Purpose:** Independently verify residual low-confidence claims; close open questions from R-12 §9 and R-13 §7; propose a single coherent patch set for project docs (do not apply edits until approved, except optional ledger/open-question annotations below).

---

## 1. Executive verdict

| Ticket | Core finding | Confidence after this close-out |
| ------ | ------------ | ------------------------------- |
| **R-12** | "CFPB Circular 2026-03" is **not a real primary source**; differentiator #3 must be **re-sourced**, not abandoned | ✅ High — primary CFPB guidance index + withdrawn-guidance list + NMP secondary located and **debunked** |
| **R-13** | S-01 upgrade to ✅ is warranted; S-02 stays ⚠ with stronger corroboration; ValidMind "unique triple-leader" claim must be softened; Chartis-only MRM analyst gap is structural | ✅ High for S-01/S-02 narrative; Solytics AI-gov leader ✅ secondary-confirmed |

**Do not block build on these tickets** — the Workbench design (SHAP → Reg B pipeline, OCC seven-section report, proxy battery) remains sound. **Do block any shipping copy that cites "Circular 2026-03" as current CFPB authority.**

---

## 2. Independent verification of low-confidence assertions

### 2.1 R-12 — Circular 2026-03 (confirmed ❌)

| Check this session | Result |
| ------------------ | ------ |
| CFPB live Guidance index (`/compliance/guidance/`, modified Jun 15, 2026) | Last listed circular: **2024-07** (credit card rewards). **No 2025/2026 circulars.** |
| CFPB Withdrawn Guidance index | Explicitly lists **Circular 2022-03** and **Circular 2023-03** withdrawn **May 12, 2025** |
| NMP trade press (R-12 open Q1) | **Located** — see §3.1; invents Circular 2026-03 |
| gov / Federal Register search for `"Circular 2026-03"` | No CFPB primary hit |

**Correction to R-12 wording (minor):** R-12 §2 says Circular 2024-07 was "later withdrawn." That is **incorrect**. Morgan Lewis analysis and the live CFPB Guidance page both show **Circular 2024-07 remains active**. Adverse-action circulars 2022-03 / 2023-03 **were** withdrawn; 2024-07 was not. Recommend a one-line erratum on R-12 (does not change the Circular 2026-03 verdict).

### 2.2 R-13 — Chartis / Gartner (confirmed with nuance)

| Check this session | Result |
| ------------------ | ------ |
| ValidMind Business Wire Chartis triple-leader claim | ✅ Exists; consistent with R-13 |
| Solytics Chartis AI Governance 2026 Category Leader (Apr 13, 2026 Access Newswire / Yahoo / solytics.com) | ✅ Confirms R-13 §4.5 |
| Layer A vs Layer B analyst split (Chartis MRM vs Forrester/Gartner/IDC AI Governance) | ✅ Structural; no second firm rates ValidMind/SAS/Solytics MRM head-to-head |

**Accept R-13 recommendations** on S-01 ✅ upgrade, S-02 strengthened ⚠, ValidMind reword, and Chartis-only footnote.

### 2.3 Prudential-regulator gap fill (R-12 open Q3)

OCC / Fed / FDIC **OCC Bulletin 2026-13** (Apr 17, 2026) revises MRM guidance and explicitly excludes gen-AI/agentic AI from that bulletin’s scope. It does **not** prescribe a documented SHAP→adverse-action translation methodology. **No prudential fill** for the specific Circular 2026-03-shaped claim. Adverse-action duties remain anchored in **ECOA §701(d) / Reg B §1002.9** (statute/regulation), not a new agency circular.

---

## 3. Closed open questions

### 3.1 R-12 Q1 — "NMP May 2026" trade press — **CLOSED**

**Found:** [National Mortgage Professional — "CFPB Issues AI Underwriting Guidance On Adverse Action Notices"](https://nationalmortgageprofessional.com/news/cfpb-issues-ai-underwriting-guidance-adverse-action-notices), by Andrew Liput, **published Jul 9, 2026** (R-04 said "NMP May 2026" — date was approximate/wrong; article is July).

**What NMP claims:** On May 5, 2026, CFPB issued Circular 2026-03 requiring lenders to document how model outputs translate to consumer-facing explanations.

**Disposition:** Secondary source **exists** but is **false relative to primary sources**. Treat as ❌ **hallucinated / erroneous trade press** — do **not** use as corroboration. Likely origin of S-33 / differentiator #3 mis-citation in R-04. Add to ledger as **S-84** (see §5).

Update R-12 §7 note: replace "no secondary source located" with "secondary located (NMP Jul 9, 2026) but contradicted by CFPB primary indexes — ❌."

### 3.2 R-12 Q2 — Will CFPB reissue AI/adverse-action guidance? — **CLOSED → watchlist**

**Disposition:** Unknown; agency posture 2025–2026 is broadly deregulatory (May 2025 mass withdrawal). Add to `deep-research-v1.md` §10.3 as **W7**: monitor CFPB circulars / FR for any reissued adverse-action/AI guidance; do not pre-claim reaffirmation.

### 3.3 R-12 Q3 — OCC/Fed/FDIC fill? — **CLOSED**

**Disposition:** No. OCC 2026-13 does not create a translation-methodology artifact requirement. Keep statutory Reg B §1002.9 + historical Circular 2022-03/2023-03 interpretive content as design anchors; do not invent a prudential circular substitute.

### 3.4 R-13 Q1 — Solytics Chartis AI Governance leader — **CLOSED**

**Disposition:** Incorporate into competitive narrative: Solytics proof points upgrade from "⚠ no Chartis leader status" → "✅ Chartis Category Leader, AI Governance Solutions 2026 (separate from 2024 MRM report)." Does **not** change Workbench scope (still compose-OSS / not enterprise GRC).

### 3.5 R-13 Q2 — Source ID collision S-62+ — **CLOSED**

**Disposition:** Assign sequential IDs — R-12 sources **S-62–S-71**; R-13 sources **S-72–S-83**; NMP **S-84**. Do not use R-13’s originally proposed overlapping S-62–S-73 numbering.

### 3.6 R-13 Q3 — Genpact PDF evidence freeze — **CLOSED → build optional**

**Disposition:** Optional `research/evidence/` hash of Genpact Chartis PDF at build/docs freeze; not blocking research close-out. Recommend if examiner-facing portfolio narrative cites Chartis figures heavily.

---

## 4. Impact on differentiator #3 (messaging)

**Keep the capability; change the authority claim.**

| Before (unsafe) | After (defensible) |
| --------------- | ------------------ |
| "CFPB Circular 2026-03 translation methodology artifact" | "Documented SHAP → Reg B §1002.9 adverse-action translation methodology artifact" |
| Implies current CFPB circular requires the artifact | Frames artifact as encoding **binding statute/regulation** + **historical** CFPB Circular 2022-03 / 2023-03 interpretive positions (withdrawn May 12, 2025) + Innovation Spotlight (S-32) |
| "Circular 2026-03 pattern" in do-claim list | "Documented factor→reason mapping methodology for examiner/reviewer validation (Reg B §1002.9)" |

**Still a market gap** (R-01): Holistic/Fiddler ship attribution, not a versioned, hash-bound Reg B translation artifact. Regulatory force is **statutory**, not "current circular compliance."

**Add to do-not-claim:**
- "Satisfies current CFPB Circular 2026-03" (document does not exist)
- "Implements current non-withdrawn CFPB circular guidance on AI adverse action" (2022-03/2023-03 withdrawn)

---

## 5. Proposed source-ledger updates

### 5.1 Amend existing rows

| ID | Change |
| -- | ------ |
| **S-01** | Status ⚠ → **✅**; Notes: full Genpact licensed reprint read (R-13); cross-confirmed by ValidMind/SAS/CRISIL/Evalueserve wire releases |
| **S-02** | Keep **⚠**; Notes: MQ paywalled; all 13 placements cross-confirmed via 7 vendor press + Sanjeev Mohan independent writeup (R-13); zero contradictions |
| **S-18** | Keep ✅ for primary text existence; Notes: **Formally withdrawn May 12, 2025** (S-65); statute/Reg B unaffected; page may still render live text |
| **S-31** | Same withdrawal annotation as S-18 |
| **S-33** | Status ⚠ → **❌**; Notes: Circular 2026-03 **not found** on CFPB.gov or FR (R-12); only secondary is NMP Jul 9 2026 (S-84), which invents the circular |

### 5.2 Append new rows (reconciled IDs)

| ID | Source | Tier | Used in | Status | Notes |
| -- | ------ | ---- | ------- | ------ | ----- |
| S-62 | CFPB Guidance index | 1 | R-12 | ✅ | Last circular listed: 2024-07 |
| S-63 | CFPB Circular 2022-03 primary page (re-fetch) | 1 | R-12 | ✅ | Text matches R-04; withdrawn per S-65 |
| S-64 | CFPB Circular 2023-03 primary page (re-fetch) | 1 | R-12 | ✅ | Archived banner; withdrawn |
| S-65 | CFPB Withdrawn Guidance index | 1 | R-12 | ✅ | 2022-03 & 2023-03 withdrawn 2025-05-12 |
| S-66 | FR 2025-08286 / 90 FR 20084 (withdrawal rule) | 1 | R-12 | ✅ | Mass guidance withdrawal |
| S-67 | FR API `"Circular 2026-03"` CFPB → count 0 | 1 | R-12 | ✅ | Negative evidence |
| S-68 | FR API CFPB "circular" ≥2025-01-01 | 1 | R-12 | ✅ | No new CFPB circulars |
| S-69 | FR 2026-07804 / 91 FR 21620 full text | 1 | R-12 | ✅ | Confirms R-02; no AA/SHAP content |
| S-70 | CFPB Newsroom Feb 2025–Jun 2026 | 1 | R-12 | ✅ | No circular announcement |
| S-71 | Innovation Spotlight re-fetch (S-32) | 1 | R-12 | ✅ | No Circular 2026-03 |
| S-72 | Chartis MRM 2024 full PDF (Genpact reprint) | 3 | R-13 | ✅ | Same doc as S-01; full read |
| S-73 | ValidMind Chartis press (Business Wire) | 3 | R-13 | ✅ | Triple Category Leader claim |
| S-74 | SAS Chartis press (PR Newswire) | 3 | R-13 | ✅ | Top governance score / 19 vendors |
| S-75 | CRISIL Chartis press | 3 | R-13 | ✅ | Triple Category Leader |
| S-76 | Evalueserve Chartis press | 3 | R-13 | ✅ | Triple Category Leader |
| S-77 | Chartis-research.com report landing (metadata) | 3 | R-13 | ⚠ | Existence/authors; full text paywalled |
| S-78 | Gartner MQ vendor press bundle (7 vendors) | 3 | R-13 | ✅ | Corroborates S-02 placements |
| S-79 | Sanjeev Mohan Medium MQ breakdown | 2 | R-13 | ✅ | Independent all-13 placement match |
| S-80 | getaigovernance.net Gartner MQ post | 3 | R-13 | ⚠ | Cross-check Niche/Challenger |
| S-81 | Forrester Wave AI Governance Q3 2025 | 3 | R-13 | ⚠ | Layer B set; no ValidMind/SAS/Solytics |
| S-82 | IDC MarketScape Unified AI Gov 2025–26 | 3 | R-13 | ⚠ | Same Layer B finding |
| S-83 | Solytics Chartis AI Governance 2026 leader press | 3 | R-13 | ⚠ | Separate report from S-01 |
| S-84 | NMP Liput article Jul 9 2026 (Circular 2026-03 claim) | 3 | R-14 | ❌ | **False secondary** — invents nonexistent circular |

---

## 6. Optimal document amendment plan (priority order)

### P0 — Must amend before any public/demo copy cites circulars

| Doc | Section | Action |
| --- | ------- | ------ |
| **`deep-research-v1.md`** | §1.2 #3 | Reword differentiator (remove Circular 2026-03 name); cite R-12/R-14 + S-34/S-18/S-31/S-32 with withdrawal caveat |
| **`deep-research-v1.md`** | §1.7 do-claim / do-not-claim | Replace "Circular 2026-03 pattern"; add do-not-claims in §4 above |
| **`deep-research-v1.md`** | §3.1 table row on Circular 2026-03 | Mark ❌ not operative; point to R-12 |
| **`deep-research-v1.md`** | §4.2 Regulatory anchors | Statute/Reg B + withdrawn circulars (historical) + S-32; drop S-33 as authority |
| **`deep-research-v1.md`** | §10.1 B7 | Mark **resolved** → Circular 2026-03 not found; see R-12/R-14 |
| **`deep-research-v1.md`** | §10.3 | Add W7 (CFPB reissue watch) |
| **`research/findings/source-ledger.md`** | S-01, S-02, S-18, S-31, S-33 + S-62–S-84 | Apply §5 |
| **`research/findings/R-04-…md`** | §2, §5, §9, §10 | Errata block or inline strike: Circular 2026-03 unsupported; NMP is false secondary |

### P1 — Competitive accuracy (non-blocking for P0 build)

| Doc | Section | Action |
| --- | ------- | ------ |
| **`deep-research-v1.md`** | §2.1 | Soften ValidMind sentence per R-13 §6 (CRISIL/Evalueserve also triple Category Leaders; ValidMind = most Workbench-relevant pure-play software) |
| **`deep-research-v1.md`** | §2.2 | Footnote: Chartis sole MRM quadrant source; Forrester/IDC/Gartner cover Layer B |
| **`research/findings/R-01-…md`** | §4.3 Solytics proof points | Update Chartis leader status via S-83 (AI Governance 2026, not 2024 MRM) |
| **`research/findings/R-09-…md`** | §3.1 #3 | Align differentiator wording with deep-research-v1 rewrite |

### P2 — Orchestration / hygiene

| Doc | Action |
| --- | ------ |
| **`research/deep-research-master-plan.md`** | R-04 objective: drop "Circular 2026-03" phrase → "Reg B §1002.9 documented translation methodology"; register R-12/R-13/R-14 as complete diligence tickets; Session 7 log |
| **`research/findings/R-12-…md`** | Erratum: 2024-07 **not** withdrawn; §9 open Qs → closed (point to R-14); fix §7 "no secondary" language |
| **`RESEARCH_FOUNDATION_v2.md`** | **Do not mutate** unless stakeholder requests; if ever updated, flag Circular 2026-03 claim and Reg B July 2026 as verified-with-corrections via R-02/R-12 |

### Explicit non-goals for this amendment wave

- Do **not** drop adverse-action module from P1 phasing
- Do **not** demote differentiator #3 out of the top three — only re-anchor authority
- Do **not** treat NMP as partially correct
- Do **not** claim OCC 2026-13 fills the explainability circular gap

---

## 7. Suggested patch text (copy-ready)

### 7.1 Differentiator #3 (replace row in deep-research-v1 §1.2)

| # | Differentiator | Module | Evidence |
| - | -------------- | ------ | -------- |
| **3** | **Documented SHAP → Reg B §1002.9 adverse-action translation methodology artifact** (versioned, hash-bound; encodes historical CFPB Circular 2022-03 / 2023-03 interpretive positions — withdrawn May 12, 2025 — plus Innovation Spotlight practice notes) | `adverse_action_translator` | ✅ R-04 design; ❌ Circular 2026-03 not found (R-12); market gap vs Holistic/Fiddler attribution-only (R-01) |

### 7.2 ValidMind sentence (replace deep-research-v1 §2.1 analyst signal)

> Analyst signal: Chartis 2024 MRM (30 vendors ✅ S-01/S-72) confirms MRM ↔ AI-governance convergence. ValidMind, CRISIL Integral IQ, and Evalueserve are each Category leaders across all three 2024 quadrants; SAS holds the top score in the governance quadrant (19 vendors). **ValidMind is the most Workbench-relevant comparator** as the only pure-play, API/SDK-native MRM software vendor among the triple leaders (CRISIL/Evalueserve are closer to validation/advisory-services profiles). Chartis remains the only analyst firm with quadrant-style coverage of traditional bank MRM software as a distinct category (Forrester/IDC/Gartner cover adjacent Layer B AI-governance platforms — R-13).

### 7.3 B7 disposition (deep-research-v1 §10.1)

| # | Question | Recommendation |
| - | -------- | -------------- |
| B7 | Circular 2026-03 primary PDF spot-check | **Resolved (R-12/R-14):** Circular **does not exist** on CFPB.gov or Federal Register. Differentiator #3 reworded to Reg B §1002.9 + historical Circular 2022-03/2023-03. NMP Jul 9 2026 (S-84) is false secondary. |

---

## 8. Recommended next action for the human / build agent

1. **Approve this amendment plan** (or edit priorities).
2. Apply **P0 patches** to `deep-research-v1.md`, `source-ledger.md`, and R-04 errata in one commit.
3. Apply **P1** competitive softens when convenient.
4. Proceed with **P0→P2 build** using corrected messaging; keep `translation_methodology_v1.json` as a first-class artifact.

*If you want these P0/P1 edits applied in-repo next, say so and they can be executed as a single amendment pass.*
