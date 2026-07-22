# R-08 — State-Level AI/Lending Laws (CO, CA, NY)

**Ticket:** R-08  
**Session:** 4  
**Status:** Complete  
**Research date:** 2026-07-20  
**Depends on:** R-02 (federal Reg B framing), R-03 (jurisdiction overlay contract)

---

## 1. Executive summary

**Recommendation:** Implement three **state overlay profiles** on the existing `regulatory_frame.state_overlay` toggle. None of the three states **replaces** the federal post–July 2026 proxy-discrimination default; each adds **disclosure, governance, and (for NY insurance) statistical-testing** obligations that the Workbench should surface as labeled evidence artifacts — not as "compliance guarantees."

| Overlay | Primary authority | Effective / compliance | Lending in scope? | Mandatory AIR / disparate-impact testing? |
| ------- | ----------------- | ------------------------ | ----------------- | ----------------------------------------- |
| **CO** | SB 26-189 (replaces SB 24-205) | **Jan 1, 2027** | ✅ Financial/lending consequential decisions | ❌ No statutory statistical battery; existing anti-discrimination law applies |
| **CA** | CPPA **CCPA ADMT regulations** (Cal. Code Regs tit. 11) | Regs effective **Jan 1, 2026**; ADMT compliance **Jan 1, 2027** for pre-existing use | ✅ "Financial or lending services" = significant decision | ⚠ Risk assessment must **consider** discrimination harms; no mandated four-fifths/AIR test |
| **NY** | DFS **Insurance Circular Letter 7 (2024)** | **July 11, 2024** (guidance) | ⚠ **Insurance underwriting/pricing only** — not bank lending | ✅ **Yes** — proxy assessment + 3-step disproportionate-adverse-effects analysis with AIR, SMD, Shapley |

**FINOS ri-22 correction (foundation §3.5):** ✅ Verified — ri-22 flags state law filling the federal gen-AI MRM gap, citing **"Colorado AI Act and California DFPI activity."** The **Colorado** reference is accurate (post-SB 189). The **"California DFPI automated-decision rules"** framing is **partially incorrect** ⚠: enacted ADMT rules are **CPPA/CCPA regulations** under the California Privacy Protection Agency; DFPI enforces existing consumer-financial-protection law (CCFPL) and issued a general AI legal advisory, but **not** a separate ADMT rulemaking parallel to Colorado.

**Gen-AI federal gap:** State laws fill **consumer-facing ADMT governance and anti-discrimination examination expectations** for automated credit/insurance decisions; they do **not** supply a substitute for OCC 2026-13 MRM on gen-AI/agentic systems. Colorado and California ADMT rules apply to ML credit models; NY CL 7 applies to insurance AI regardless of whether the model is "generative."

---

## 2. Colorado — SB 26-189 (Automated Decision-Making Technology)

### 2.1 Legislative status and effective date

| Milestone | Date | Status |
| --------- | ---- | ------ |
| SB 24-205 enacted | May 17, 2024 | Superseded |
| SB 24-205 scheduled effective | June 30, 2026 | ❌ Enforcement blocked (federal court order, April 2026) ⚠ |
| **SB 26-189 signed** | May 14, 2026 | ✅ |
| **SB 26-189 effective** | **January 1, 2027** | ✅ Primary |

**Source:** Colorado General Assembly bill page for SB 26-189 ✅ S-52

### 2.2 Scope — lending applicability

SB 26-189 applies when **automated decision-making technology (ADMT)** is used to **materially influence** a **consequential decision** in covered domains including **"financial or lending services."**

| Term | Definition (statutory summary) |
| ---- | ------------------------------ |
| **ADMT** | Technology processing personal data using computation to generate output (predictions, scores, classifications, etc.) used to make, guide, or assist a decision about an individual |
| **Consequential decision** | Decision relating to access, eligibility, or compensation in education, employment, housing, **financial/lending**, insurance, healthcare, or essential government services/benefits |
| **Material influence** | ADMT output meaningfully affects the decision (not merely informational) |

**GLBA / bank exemption:** ❌ No entity-level exemption for banks or credit unions under SB 189 (narrow exemption removed vs. SB 24-205 bank carve-out) ⚠ S-52 secondary corroboration (Cooley, May 2026).

**ECOA/FCRA safe harbor:** Institutions compliant with ECOA or FCRA adverse-action notice requirements for the same decision **may satisfy** SB 189 post-adverse outcome disclosure obligations for that decision ✅ ⚠ (law-firm secondary; AG rules pending).

### 2.3 Enforcement posture

| Element | Detail |
| ------- | ------ |
| **Enforcer** | Colorado Attorney General |
| **Mechanism** | Colorado Consumer Protection Act — violation = **deceptive trade practice** |
| **Private right of action** | ❌ No new private right under SB 189 |
| **Cure period** | 60-day notice and opportunity to cure before AG action (through **Jan 1, 2030**) |
| **Rulemaking** | AG must adopt rules clarifying post-adverse outcome disclosures by **Jan 1, 2027** |

### 2.4 Protected classes and fairness tests

SB 189 **does not** impose a standalone statistical fairness battery (no mandated AIR, proxy test, or impact assessment in the replacement law). SB 24-205's **algorithmic discrimination** duty-of-care, impact assessments, and AG reporting were **removed** ✅ S-52, S-53 historical.

| Requirement | SB 24-205 (repealed) | SB 26-189 (current) |
| ----------- | -------------------- | ------------------- |
| Risk management policy | ✅ Required | ❌ Removed |
| Annual impact assessment | ✅ Required | ❌ Removed |
| AG reporting | ✅ Required | ❌ Removed |
| Consumer point-of-interaction notice | ✅ | ✅ |
| Post-adverse outcome plain-language description | ✅ | ✅ (within 30 days) |
| Meaningful human review on request | ✅ | ✅ |
| 3-year record retention | ✅ | ✅ |

**Disparate impact / AIR testing required?** ❌ **Not under SB 189.** Existing Colorado and federal anti-discrimination law may still apply to lending decisions; the Workbench should run Layer A (AIR) as **"existing-law outcomes support evidence,"** not "Colorado AI Act disparate-impact compliance."

### 2.5 Human review and disclosure (adverse-action module relevance)

| Obligation | Workbench artifact |
| ---------- | ------------------ |
| Point-of-interaction notice | Checklist field in report §II (out of scope for validation-only demo; document gap) |
| Post-adverse outcome description within 30 days | Cross-reference R-04 adverse-action translator output; flag if principal reasons lack plain-language mapping |
| Human review on request | `governance.approval` / human-appeal workflow stub (R-06); document reviewer authority |

### 2.6 CO overlay config (maps to R-03)

```yaml
regulatory_frame:
  federal_ecoa: proxy_discrimination
  fha_overlay: false
  state_overlay: CO
  state_overlay_profile:
    authority: "Colorado SB 26-189 (effective 2027-01-01)"
    consequential_domain: financial_or_lending
    bias_battery:
      layer_a_outcomes: monitor          # optional — not statutory; supports existing law
      layer_b_error_parity: true         # internal risk default
      layer_c_proxy: true                # federal ECOA default
      disparate_impact_battery: false    # no CO statutory DIA
    human_review_on_request: document    # checklist only in v1
    post_adverse_notice_days: 30
    record_retention_years: 3
```

---

## 3. California — CCPA ADMT regulations (not DFPI standalone rules)

### 3.1 Authority correction

| Source | Role |
| ------ | ---- |
| **CPPA / Cal. Code Regs tit. 11** (ADMT package, Sept 2025) | ✅ **Primary** enacted ADMT rules — S-54 |
| **DFPI** | Enforces CCFPL and existing fair-lending law; **no separate ADMT rulemaking** identified ✅ S-56 |
| **CA Attorney General** | Legal Advisory on application of existing CA law to AI (Oct 2024) — reinforces ECOA/FCRA adverse-action specificity ✅ S-56 |

Foundation §3.5 and FINOS ri-22 reference **"California DFPI automated-decision rules"** — treat as **shorthand for California's ADMT regulatory cluster** (CPPA-led), not a DFPI-specific regulation. **Correct in Workbench labeling:** `California CCPA/CPRA ADMT (CPPA)`.

### 3.2 Effective dates and scope

| Milestone | Date |
| --------- | ---- |
| ADMT regulations adopted | September 2025 (OAL approved Sept 23, 2025) |
| Regulations effective | **January 1, 2026** |
| Compliance for ADMT in use **before** Jan 1, 2027 | **January 1, 2027** |
| Compliance for ADMT deployed **on/after** Jan 1, 2027 | Before deployment |

**Significant decision — lending:** Includes "the provision or denial of **financial or lending services**" (extension of credit, loans, deposit accounts, etc.) ✅ S-55 §7001(ddd), §7200.

**ADMT trigger:** Technology that **replaces or substantially replaces** human decisionmaking (human reviewer must interpret output and retain authority to change decision) ✅ S-55.

### 3.3 Enforcement posture

| Element | Detail |
| ------- | ------ |
| **Enforcer** | California Privacy Protection Agency (CPPA); AG concurrent authority under CCPA |
| **Penalties** | CCPA civil penalties; risk assessment attestation under penalty of perjury (executive signatory) for cybersecurity audit track |
| **First ADMT attestation** | Risk assessment documentation producible to CPPA/AG on request; annual attestation cycle for cybersecurity audits begins 2028 ⚠ |

### 3.4 Protected classes and fairness tests

CCPA ADMT rules do **not** mandate four-fifths/AIR or a named disparate-impact legal test for lending. They require:

1. **Risk assessment** before using ADMT for significant decisions (§7150) — triggered activity includes ADMT for lending decisions.
2. Assessment must identify **negative impacts** including **discrimination** on protected characteristics (illustrative list §7152).
3. **Safeguards** may include policies/procedures ensuring ADMT "does not unlawfully discriminate" — example, not mandate.
4. Optional consultation with **ADMT bias experts** (§7151).

**Disparate impact / AIR testing required?** ⚠ **Not as a named legal test.** Statistical bias battery output serves as **risk-assessment evidence** for discrimination harms. California **Unruh Civil Rights Act** (general lending public-accommodations context) requires **intentional discrimination** — not general disparate impact ✅ Harris v. Capital Growth (Cal. 1991) ⚠ case law.

**Pending legislation:** AB 1018 (2025–26 session) would require **disparate impact assessments** for covered ADS — **not enacted** as of research date ❌ S-61. Do not build as v1 requirement.

### 3.5 Human review and disclosure

| Obligation | Detail |
| ---------- | ------ |
| **Pre-use notice** | Plain-language ADMT purpose, opt-out rights, access rights, non-retaliation |
| **Opt-out** | Two easy methods (with exceptions) |
| **Human appeal exception** | If consumer can appeal to human who can **overturn** ADMT output, opt-out may not apply |
| **Access** | Consumer right to ADMT information about the decision |

**Adverse-action module:** CCPA ADMT complements — does not replace — Reg B §1002.9. Workbench should export R-04 principal reasons into CA risk-assessment "logic of ADMT" documentation fields.

### 3.6 CA overlay config

```yaml
regulatory_frame:
  federal_ecoa: proxy_discrimination
  fha_overlay: false
  state_overlay: CA
  state_overlay_profile:
    authority: "California CCPA ADMT (Cal. Code Regs tit. 11, CPPA)"
    significant_decision: financial_or_lending
    bias_battery:
      layer_a_outcomes: true               # risk-assessment evidence for discrimination harms
      layer_b_error_parity: true
      layer_c_proxy: true
      disparate_impact_battery: false      # no enacted CA lending DIA statute
    admt_risk_assessment_export: true      # machine-readable summary for §7152 report
    human_appeal_workflow: document        # stub in v1
    pre_use_notice_fields: document        # checklist; not generated in validation-only demo
```

---

## 4. New York — DFS guidance

### 4.1 Scope clarification (critical)

NY "DFS guidance" in the research brief conflates **two distinct tracks**:

| Track | Status | Lending relevance |
| ----- | ------ | ----------------- |
| **Insurance Circular Letter 7 (2024)** | ✅ Finalized July 11, 2024 | **Insurance underwriting/pricing only** — not bank consumer lending |
| **DFS Industry Letter IL 2024-10-16 (AI cybersecurity)** | ✅ Guidance only | **Part 500 cybersecurity** — not fair-lending model validation |
| **Banking Law §103-a (A773 / A773B)** | ❌ **Pending legislation** | Would require **disparate impact analysis** for automated **lending** decision tools |

**Recommendation:** Map `state_overlay: NY` to **DFS CL 7 insurance AI** profile by default, with `product_line: insurance` metadata. For **bank lending** demos, use federal frame + note NY lending bill pending; do not claim CL 7 lending coverage.

### 4.2 Insurance Circular Letter 7 (2024) — primary NY overlay

**Effective:** Issued July 11, 2024; applies to insurers authorized in NY (P&C, life, health, HMO, etc.) ✅ S-57

**Scope:** AIS and ECDIS used to supplement, proxy, or identify "lifestyle indicators" for **underwriting and pricing** — explicitly **not** claims, marketing, or fraud (those are out of scope per circular).

### 4.3 Enforcement posture

| Element | Detail |
| ------- | ------ |
| **Type** | Supervisory guidance — expectations under existing Insurance Law |
| **Enforcer** | NY DFS |
| **Binding force** | Not new statute; failure to meet expectations → examination criticism, enforcement under Insurance Law Art. 26 unfair discrimination provisions |

### 4.4 Protected classes and fairness tests — **most rigorous overlay**

CL 7 **explicitly requires** quantitative fairness testing for insurance AI:

| Test / step | Requirement |
| ----------- | ----------- |
| **Proxy assessment** | Demonstrate ECDIS are not proxies for protected classes; may use data available or **reasonably inferred** (BISG cited as example) ✅ S-57 |
| **Step 1** | Assess **disproportionate adverse effects** by protected class |
| **Step 2** | If prima facie showing → **business necessity** analysis |
| **Step 3** | Search for **less discriminatory alternative** (LDA); repeat annually if no LDA |
| **Named metrics** | **Adverse Impact Ratio**, denial odds ratios, marginal effects, **SMD**, z/t-tests, **Shapley values** / drivers of disparity |
| **Frequency** | Before production; **regular cadence**; on material model changes |
| **Documentation** | Available to DFS on request |

**Disparate impact / AIR testing required?** ✅ **Yes** — for NY insurance overlay. This is the **only** state overlay in v1 scope that **mandates** a full DIA-style battery aligned with Workbench Layer A + proxy + SHAP.

### 4.5 Human review and adverse action

- Insurers must provide **specific reasons** for adverse underwriting decisions; cannot rely solely on vendor non-discrimination claims ✅ S-57
- Governance: board/senior management annual review of ECDIS/AIS policies

### 4.6 NY overlay config

```yaml
regulatory_frame:
  federal_ecoa: proxy_discrimination
  fha_overlay: false
  state_overlay: NY
  state_overlay_profile:
    authority: "NY DFS Insurance Circular Letter 7 (2024)"
    product_line: insurance_underwriting_pricing   # NOT bank_lending
    bias_battery:
      layer_a_outcomes: true               # required — AIR, denial odds, SMD
      layer_b_error_parity: true
      layer_c_proxy: true                    # required — proxy assessment
      disparate_impact_battery: true         # 3-step DIA (Steps 1–3)
      lda_search: document                   # flag only in v1; no mitigation prescribe
    testing_cadence: pre_production_and_ongoing
    annual_governance_review: document
    pending_lending_bill: "NY A773B — not enacted"
```

### 4.7 Pending NY lending legislation (out of v1 scope, watchlist)

**A773B** would require deployers of **automated lending decision-making tools** to conduct **disparate impact analysis** by independent auditor, testing adverse impact by sex, race, ethnicity, and other protected classes ✅ S-59. **Not law** — document in open questions for R-10/R-build.

---

## 5. Cross-state comparison — disparate impact vs. federal Reg B

| Jurisdiction | Federal ECOA (post–July 2026) | State overlay DIA/AIR |
| ------------ | ------------------------------ | --------------------- |
| **Federal default** | Proxy discrimination + disparate treatment; ❌ no federal ECOA disparate impact | — |
| **FHA (mortgage)** | FHA disparate impact still enforceable | Overlay via `fha_overlay: true` (R-03) |
| **Colorado SB 189** | Same federal frame | ❌ No statutory DIA; disclosure/human review |
| **California CCPA ADMT** | Same federal frame | ⚠ Consider discrimination in risk assessment; ❌ no mandated AIR |
| **NY DFS CL 7 (insurance)** | ECOA N/A (insurance) | ✅ Full proxy + disproportionate adverse effects + AIR |

**Workbench messaging:** When `state_overlay: CO|CA`, label Layer A as **"outcomes analysis / risk-assessment evidence"** — not "ECOA disparate-impact compliance." When `state_overlay: NY` + insurance product line, label Layer A as **"DFS CL 7 quantitative discrimination testing."**

---

## 6. FINOS ri-22 state-law flag — corroboration

**Foundation claim (§3.5):** FINOS ri-22 flags state-level AI laws may fill part of the federal gen-AI/agentic-AI carve-out.

**Verification (✅ S-60 primary):** ri-22 states:

> "The US carve-out does not create an unregulated zone… underlying obligations have shifted to a wider set of authorities: fair-lending law (ECOA/Reg B)… **NYDFS Part 500, and state-level AI legislation such as the Colorado AI Act and California DFPI activity.**"

| FINOS claim | R-08 assessment |
| ----------- | --------------- |
| State law fills **some** federal gen-AI gap | ⚠ **Partially** — state ADMT laws govern **automated consequential decisions** regardless of gen-AI label; they do not supply OCC MRM for gen-AI |
| Colorado AI Act | ✅ Accurate — now SB 26-189 |
| California DFPI activity | ⚠ **Imprecise** — enacted rules are **CPPA CCPA ADMT**; DFPI is enforcement/advisory, not rule author |
| NYDFS Part 500 | ⚠ **Different domain** — cybersecurity, not fair-lending statistics (IL 2024-10-16) |
| NY insurance CL 7 | ❌ **Not cited in ri-22** — but is the strongest NY fair-AI statistical guidance |

**Workbench FINOS mapping:** Log `state_overlay` activation under `bias_battery.result` with `finos_control: mi-5` (acceptance testing) and cross-reference ri-22 in report §II regulatory frame statement.

---

## 7. Implications for Workbench

1. **Implement three overlay profiles** in `bias_battery` — CO (disclosure/human-review checklist), CA (risk-assessment export + Layer A/B/C as evidence), NY (full DIA battery for insurance product line).
2. **Default `state_overlay: none`** for German Credit demo; add HMDA-NY **insurance** or **HMDA FHA** slice in R-10 for overlay demonstration.
3. **Audit log:** Extend `bias_battery.result` payload with `jurisdiction_frame: { federal_ecoa, fha_overlay, state_overlay, state_authority }` per R-06 event catalog.
4. **Report §II:** Literal "Regulatory frames active for this validation run" table listing overlay authority, effective dates, and **explicit non-claims** (e.g., "does not constitute legal compliance determination").
5. **Correct labeling:** Use `California CCPA/CPRA ADMT (CPPA)` not `DFPI ADMT rules` in UI and reports.
6. **NY lending:** Do not enable `state_overlay: NY` for bank lending demos without `product_line: insurance` metadata and user acknowledgment.
7. **No stack blocker** (R-07 confirmed) — overlays are configuration + report templates only.

### 7.1 Overlay toggle behavior summary

| `state_overlay` | Layers enabled | New v1 artifacts |
| --------------- | -------------- | ---------------- |
| `none` | Federal proxy + optional FHA | R-03 default |
| `CO` | A (monitor), B, C | Post-adverse notice checklist; human-review doc stub; 3-year retention flag |
| `CA` | A, B, C | `admt_risk_assessment_summary.json` for §7152 fields |
| `NY` | A, B, C + full DIA | `ny_dfs_cl7_testing_report.json`; proxy + LDA search flags |

---

## 8. Sources

| ID | Source | Tier | Status | Used for |
| -- | ------ | ---- | ------ | -------- |
| S-52 | Colorado SB 26-189 (leg.colorado.gov bill page + summary) | 1 | ✅ | CO scope, effective date, obligations |
| S-53 | Colorado SB 24-205 (leg.colorado.gov — historical) | 1 | ✅ | Repealed requirements comparison |
| S-54 | CPPA regulations page — ADMT package Sept 2025 | 1 | ✅ | CA authority, effective dates |
| S-55 | FPF CCPA ADMT Issue Brief (Oct 2025) | 2 | ⚠ | §7001/§7150/§7200 cross-corroboration |
| S-56 | CA AG Legal Advisory — AI application of existing law (PDF) | 1 | ✅ | DFPI vs CPPA correction; ECOA reaffirmation |
| S-57 | NY DFS Insurance Circular Letter 7 (2024) | 1 | ✅ | NY proxy/DIA/AIR requirements |
| S-58 | NY DFS IL 2024-10-16 AI cybersecurity | 1 | ✅ | Part 500 scope boundary (NOT fair lending) |
| S-59 | NY A773B bill text (legislation.nysenate.gov) | 1 | ✅ | Pending lending DIA — not enacted |
| S-60 | FINOS ri-22 regulatory compliance risk (GitHub primary) | 1 | ✅ | State-law flag corroboration/correction |
| S-61 | CA AB 1018 bill text (leginfo.legislature.ca.gov) | 1 | ✅ | Pending CA disparate impact — not enacted |

---

## 9. Open questions

1. **Colorado AG rules (due Jan 1, 2027):** Post-adverse outcome disclosure content may change; monitor before production CO overlay.
2. **CA CPPA enforcement precedent:** No public enforcement actions on ADMT yet; risk-assessment template may need revision after first cases.
3. **NY A773B / CA AB 1018:** If enacted before build, add `state_overlay: NY_LENDING` / `CA_ADS` profiles in v1.1.
4. **Insurance vs. lending demo:** R-10 should choose whether NY overlay is demonstrated on insurance synthetic data or documented-only for bank lending persona.
5. **ECOA safe harbor mapping:** Whether R-04 adverse-action output fully satisfies CO SB 189 post-adverse disclosures — requires CO AG rules + counsel review.
