# R-02 — Reg B July 2026 Narrowing: Verification

**Ticket:** R-02  
**Session:** 1  
**Status:** Complete  
**Research date:** 2026-07-20

---

## Executive finding

**VERIFIED ✅** — The "July 2026 Reg B narrowing" referenced in `RESEARCH_FOUNDATION_v2.md` §3.2 is real, but the foundation document **underspecified** what changed. The April 22, 2026 CFPB final rule (Federal Register **91 FR 21620**, document **2026-07804**) is effective **July 21, 2026** and makes three material amendments to Regulation B Subpart A:

1. **Eliminates disparate-impact ("effects test") liability under ECOA/Reg B** — express statement that ECOA does not recognize the effects test.
2. **Narrows the discouragement prohibition** (12 CFR §1002.4(b)) — liability limited to oral/written statements creditors know or should know would cause a reasonable person to believe credit would be denied or offered on less favorable terms **because of a prohibited-basis characteristic**; removes prior breadth covering non-expressive "acts or practices."
3. **Restricts Special Purpose Credit Programs (SPCPs)** for for-profit creditors — new prohibitions/conditions on race/sex/common-characteristic SPCPs.

**What did NOT change (critical for Workbench scope):**

- **Adverse action notice requirements** under ECOA §701(d) and Reg B §1002.9 — **unchanged in substance**.
- **CFPB Circular 2026-03** (May 5, 2026) requirement to document how model outputs translate to consumer-facing explanations — **still operative** for fair-lending reviewers; this is orthogonal to the disparate-impact removal.
- **Disparate treatment** and **proxy discrimination** — explicitly preserved; facially neutral criteria that are proxies for protected characteristics remain actionable.
- **Fair Housing Act** disparate impact — **still enforceable** (Supreme Court *Inclusive Communities*); state fair-lending laws may retain disparate-impact theories.

---

## Source verification

| Source | Tier | Status | Notes |
| ------ | ---- | ------ | ----- |
| Federal Register 91 FR 21620 (2026-07804) | Primary | ✅ | Effective July 21, 2026; removes effects test language |
| CFPB Regulation B landing page (consumerfinance.gov) | Primary | ✅ | Confirms three amendment areas |
| Venable LLP alert (May 2026) | Secondary | ⚠ | Cross-corroborated against FR text |
| Greenberg Traurig alert (May 2026) | Secondary | ⚠ | Notes litigation uncertainty |
| KPMG regulatory alert | Secondary | ⚠ | Confirms July 21 effective date |
| CFPB Circular 2022-03 (adverse action) | Primary | ✅ | Black-box holding still applies to §1002.9 |

**Paywall / inaccessible:** Full Federal Register PDF not independently extracted line-by-line in this session; secondary law-firm summaries corroborate primary FR metadata and effective date. **Recommend spot-check of §1002.9 commentary** before build if adverse-action module language is load-bearing.

---

## Implications for Workbench

### 1. Bias/fair-lending module scope must be reframed (actionable)

| Testing type | Pre–July 2026 framing | Post–July 2026 framing (federal ECOA) |
| ------------ | ---------------------- | ------------------------------------- |
| Adverse impact ratio / four-fifths rule | Primary federal fair-lending statistical test | **Still valuable** for FHA, state law, internal risk management, and OCC MRM "outcomes analysis" — but **no longer a federal ECOA disparate-impact compliance test** |
| Proxy discrimination analysis | Important adjunct | **Elevated to primary federal ECOA statistical concern** alongside disparate treatment |
| Adverse-action reason translation | Required (§1002.9 + Circular 2026-03) | **Unchanged — remains core demo module** |
| Model documentation for reviewer validation | Circular 2026-03 | **Unchanged** |

**Recommendation:** Position the statistical bias module as serving **(a)** OCC 2026-13 outcomes analysis / NIST MEASURE 2.11 / EU AI Act Art. 10, **(b)** FHA and state-law disparate-impact where applicable, and **(c)** proxy-discrimination detection under the revised Reg B — not solely as an ECOA disparate-impact compliance tool.

### 2. Product messaging discipline

- Do **not** claim the Workbench "ensures ECOA disparate-impact compliance" after July 21, 2026.
- Do claim: defensible validation evidence, adverse-action explainability, proxy-risk analysis, and multi-framework documentation.

### 3. Demo scenario

- Adverse-action translator remains the strongest **unchanged** federal hook.
- Bias testing demo should explicitly show **proxy analysis** and **FHA/state-law overlay** toggles to reflect the new legal landscape.

---

## Open questions

1. **Litigation risk:** Multiple secondary sources note courts may challenge CFPB's elimination of effects-test language. Monitor through build phase; do not treat as permanently settled law.
2. **State preemption:** Whether state AI/fair-lending laws fill the federal gap is ticket **R-08** (Session 4).
3. **Section 1071 (small business lending data):** Separate April 2026 Reg B Subpart B rule narrows 1071 scope — out of Workbench v1 unless small-business lending demo is chosen.

---

## Update required in foundation doc (future, not in this pass)

`RESEARCH_FOUNDATION_v2.md` §3.2 should upgrade the flagged claim from "unverified" to "verified with scope correction" — the narrowing is to **disparate impact and discouragement**, not adverse-action explainability.
