# R-15 — Regulatory Watchlist (W1–W4) Partial Findings

**Ticket:** ad hoc (deep-research workflow `wf_f9f4bfbe-fe4`, launched to resolve deep-research-v1.md §10.3 watchlist items W1–W4)
**Session:** ad hoc close-out
**Status:** **Partial — Search + Fetch stages complete; Verify stage incomplete; Synthesize stage never ran**
**Research date:** 2026-07-21/22
**Depends on:** deep-research-v1.md §10.3 (W1–W4), R-02, R-08

---

## 0. What this document is (read this before the findings)

The originating `/deep-research` workflow run (Scope → Search → Fetch/extract-claims → Verify → Synthesize) hit the session's token/usage limit mid-run. Of 103 total subagent calls, **45 completed and are cached** (1 scope call, 5 search-angle calls, 21 fetch/claim-extraction calls, and 18 adversarial-verification votes); **58 never ran and are not cached** (mostly the remaining adversarial-verification votes and the final synthesis/merge step). Per instruction, **the incomplete Verify stage was deliberately not resumed or re-run** — this document synthesizes only what is already in hand from the 45 completed calls, pulled directly from the workflow's run journal.

**Practical effect on confidence labeling:**
- **W1** is unusually well-verified — all 18 completed adversarial votes happened to land on the same core W1 claim (the 3-vote design over-sampled it before the limit hit), so it carries genuine multi-source adversarial confirmation, not just single-pass extraction.
- **W2, W3, W4** carry **zero completed adversarial votes**. Their findings below rest on the Fetch-stage claim extractions only — each claim was pulled from one fetched page by one extraction agent, cross-referenced by me (not adversarially re-verified) against the other fetched pages where they overlap. Label accordingly: **⚠ single-pass, cross-referenced** rather than ✅ adversarially confirmed.
- No new web research was performed to produce this document — everything below was already sitting in the run journal (the "research legwork" the user asked to be synthesized), not fetched fresh.

---

## 1. Summary table

| Item | Original framing (deep-research-v1.md §10.3) | Updated status | Confidence |
| ---- | --------------------------------------------- | -------------- | :--------: |
| **W1** — Reg B effects-test litigation | "Courts may challenge" (speculative, S-17 law-firm alerts) | **Materialized.** A lawsuit was filed May 27, 2026 — *National Fair Housing Alliance et al. v. CFPB, et al.*, No. 1:26-cv-01820 (D.D.C.) | ✅✅ Very high (18/18 independent adversarial votes confirmed, incl. court docket) |
| **W2** — Colorado SB 26-189 AG rulemaking | Status unknown | Statute **enacted** May 14, 2026. AG rulemaking is in an **informal pre-rulemaking phase only** — no NPRM/draft rule yet; formal rulemaking targeted "end of summer" 2026 | ⚠ Single-pass, multi-source-consistent |
| **W3** — CA CPPA ADMT enforcement | "Compliance date Jan 2027" | Regulation **finalized Sept 2025**, general effective **Jan 1, 2026**; ADMT-specific compliance **Jan 1, 2027**. **No ADMT-specific enforcement action found** (consistent with the built-in lead time — no compliance data reaches CPPA until 2028) | ⚠ Single-pass; absence-of-enforcement is not exhaustively swept |
| **W4** — NY A773 / CA AB 1018 | Both "not enacted" (pending) | Both still **pending, neither enacted nor dead**. NY bill has advanced twice (now print "C") to the Assembly floor calendar but stalled there since Apr 30, 2026. CA AB 1018 rolled into the second year of its 2-year session; a since-debunked rumor claimed it had passed — it has not | ⚠ Single-pass, official-tracker-sourced |

---

## 2. W1 — Reg B effects-test litigation risk: RESOLVED (materialized)

### 2.1 Finding

**A federal lawsuit challenging the CFPB's Regulation B rule was filed on May 27, 2026** — roughly two months before the rule's July 21, 2026 effective date.

| Fact | Detail |
| ---- | ------ |
| Case | *National Fair Housing Alliance et al. v. Consumer Financial Protection Bureau, et al.* |
| Docket | No. 1:26-cv-01820, U.S. District Court for the District of Columbia |
| Filed | May 27, 2026 |
| Plaintiffs | National Fair Housing Alliance (NFHA), Rise Economy (f/k/a California Reinvestment Coalition), BLDS LLC, SolasAI |
| Defendants | CFPB; Acting Director Russell Vought |
| Counsel | Relman Colfax PLLC, Public Citizen Litigation Group, Democracy Forward |
| Rule challenged | CFPB final rule issued April 22, 2026 (91 FR 21620 / Federal Register doc. 2026-07804), effective July 21, 2026 |
| Relief sought | Vacatur under the APA — arbitrary and capricious, contrary to law/ECOA, in excess of statutory authority, procedurally defective (32-day comment period called inadequate given 64,000+ comments received; missing regulatory-flexibility/SBREFA analysis). Separately challenges Acting Director Vought's authority to hold that role under the Federal Vacancies Reform Act |
| Injunctive relief | **Not sought.** No preliminary injunction was requested — the rule remains legally effective and enforceable during the litigation |
| Legal theory | ECOA's "on the basis of" statutory language + legislative history incorporating the Supreme Court's *Griggs* "effects test" + decades of agency interpretation |

### 2.2 Verification depth

This claim (and its component facts — filing date, court, parties, rule challenged, relief sought, no-injunction status) was independently checked by **18 separate adversarial-verification agents**, each explicitly tasked with trying to refute it. All 18 returned `refuted: false`, `confidence: high`. Corroborating sources cited across the 18 votes:

- **Primary/court record:** CourtListener docket **1:26-cv-01820** ("National Fair Housing Alliance v. Consumer Financial Protection Bureau")
- **Party sources:** Relman Colfax case page ([relmanlaw.com/cases-NFHA-versus-Consumer-Financial-Protection-Bureau](https://www.relmanlaw.com/cases-NFHA-versus-Consumer-Financial-Protection-Bureau)); NFHA's own press release ([nationalfairhousing.org/nfha-sues-cfpb-ecoa-rule-change](https://nationalfairhousing.org/nfha-sues-cfpb-ecoa-rule-change/)); Democracy Forward press release ([democracyforward.org](https://democracyforward.org/news/press-releases/fair-housing-and-lending-advocates-sue-cfpb-over-new-rule-gutting-key-anti-discrimination-protections/))
- **Independent legal/trade press:** Mayer Brown client alert ([mayerbrown.com](https://www.mayerbrown.com/en/insights/publications/2026/06/cfpb-sued-over-fair-lending-rule-under-equal-credit-opportunity-act)); Consumer Financial Services Law Monitor ([consumerfinancialserviceslawmonitor.com](https://www.consumerfinancialserviceslawmonitor.com/2026/06/consumer-advocacy-groups-and-other-plaintiffs-challenge-cfpbs-regulation-b-subpart-a-overhaul/)); Banking Dive, HousingWire, RISMedia, MortgagePoint, ICLG, Davis Vanguard, National Law Review, US News/AP wire (named in individual votes, no contradicting report found in any)
- **Rule text:** Federal Register 91 FR 21620 / doc. 2026-07804 ([federalregister.gov](https://www.federalregister.gov/documents/2026/04/22/2026-07804/equal-credit-opportunity-act-regulation-b)) — independently confirms the April 22 issuance / July 21 effective date math (exactly 90 days)

No vote found any contradicting report, dismissal, withdrawal, or injunction. This is the strongest-verified single finding in the entire cache.

### 2.3 Implications for the Workbench

1. **Update deep-research-v1.md §10.3 W1**: change from "monitor" to a resolved factual status — litigation is filed and live, not merely a risk.
2. **New consideration not previously flagged**: the rule remains in force (no injunction sought or granted), so the Workbench's existing "do not claim ECOA disparate-impact compliance" posture (§1.7) is still correct *today*. But because a live APA vacatur suit is pending against the very rule the `regulatory_frame.federal_ecoa: proxy_discrimination` default is built on, **a future court ruling could vacate the rule and reinstate the federal disparate-impact/AIR framing** the Workbench currently treats as secondary (Layer A, non-federal-ECOA use per §3.1). This is a real config-level risk: the default federal frame is downstream of litigation, not settled law. Recommend flagging this explicitly in the Workbench's own documentation/§II limitations block, and adding "CFPB Reg B rule vacated on appeal" as a named trigger condition that should flip `federal_ecoa` back toward an AIR/disparate-impact framing if it occurs.
3. Recommend adding case No. 1:26-cv-01820 to the source ledger as a new, high-confidence primary source superseding S-17's speculative framing.

---

## 3. W2 — Colorado SB 26-189 Attorney General rulemaking: STILL OPEN, materially advanced

### 3.1 Finding

| Fact | Detail | Source |
| ---- | ------ | ------ |
| Enactment | SB 26-189 ("Automated Decision-Making Technology Act") signed by Gov. Polis **May 14, 2026** (passed legislature ~May 9, 2026); repeals and reenacts the original Colorado AI Act (SB 24-205) | [leg.colorado.gov/bills/sb26-189](https://leg.colorado.gov/bills/sb26-189); Crowell & Moring, Consumer Finance Monitor alerts |
| Effective date | January 1, 2027 (confirmed, matches R-08) | Colorado AG's own site (coag.gov/ai/) |
| AG rulemaking status | **Informal pre-rulemaking phase only.** No NPRM, no formal comment period, no draft rule text published as of the research date | [coag.gov/ai/](https://coag.gov/ai/) |
| Pre-rulemaking artifact | A "Pre-Rulemaking Considerations Document" (PDF) was issued by the AG's office in **June 2026**; an informal public-comment window on it closed **July 13, 2026** | [coag.gov pre-rulemaking PDF](https://coag.gov/app/uploads/2026/06/ADMT-Chatbot-Pre-Rulemaking-Considerations-Document.pdf) |
| Formal rulemaking timeline | AG's office states formal notice-and-comment rulemaking (with an actual draft rule) is targeted for **"the end of summer" 2026** | coag.gov/ai/; Ogletree Deakins alert |
| Disclosure-content specifics | **Not yet defined.** The June 2026 pre-rulemaking document restates only the statutory baseline — a 30-day, plain-language disclosure with three required elements: (1) description of the decision and the ADMT's role, (2) instructions for requesting more information about the ADMT (name, version, developer, data types/sources used), (3) an explanation of the individual's rights — and poses open questions to stakeholders about sector-specific content rather than proposing rule text | Colorado AG pre-rulemaking PDF |
| Scope confirmation | Covered "consequential decisions" span employment, housing, **credit**, insurance, health care, education, and essential government services — lending/credit is explicitly in scope | Secondary legal-industry source, May 27, 2026 (exact publication URL not preserved in the cached extraction — flagged as a sourcing gap, see §6) |
| Related law | A separate statute, HB 26-1263 ("Chatbot Safety Act," signed July 1, 2026), shares the Jan 1, 2027 effective date and is being folded into the same AG rulemaking docket, though it doesn't itself mandate rulemaking | coag.gov/ai/ |
| Enforcement structure | AG has exclusive enforcement authority; violations treated as deceptive trade practices under the Colorado Consumer Protection Act; mandatory 60-day notice-and-cure period (this cure-period provision sunsets Jan 1, 2030) | Secondary source, May 27, 2026 (same sourcing-gap note as above) |

### 3.2 Implications for the Workbench

1. **Update deep-research-v1.md §10.3 W2**: not resolved, but no longer "status unknown" — the statute is law, the AG is in a defined pre-rulemaking phase, and there's a concrete next checkpoint ("end of summer 2026" for the formal NPRM). Recommend setting the next watchlist check for **September 2026**.
2. The three-element statutory disclosure baseline (decision description + ADMT-identification instructions + rights explanation) is concrete enough to inform the Workbench's CO overlay checklist (§1.4, §3.2) now, even before the AG's rule text exists — it's the statutory floor the eventual rule will build on.
3. `deep-research-v1.md` §3.2's CO overlay note ("Disclosure checklist; Layer A as 'existing-law support'") remains accurate; no statutory AIR/DIA battery was found or introduced by SB 26-189, consistent with the original R-08 finding.

---

## 4. W3 — California CPPA ADMT enforcement: STILL OPEN, date framing corrected

### 4.1 Finding

| Fact | Detail | Source |
| ---- | ------ | ------ |
| Board adoption | CPPA Board formally adopted the ADMT/risk-assessment/cybersecurity-audit regulations **July 24, 2025** | [cppa.ca.gov/regulations/ccpa_updates.html](https://cppa.ca.gov/regulations/ccpa_updates.html) |
| Finalization | Office of Administrative Law approved the regulations and filed them with the CA Secretary of State **September 22–23, 2025** (OAL's own Notice of Approval is dated Sept 22; CPPA's announcement of the approval is dated Sept 23) | [cppa.ca.gov/announcements/2025/20250923.html](https://www.cppa.ca.gov/announcements/2025/20250923.html); [OAL Notice of Approval PDF](https://www.cppa.ca.gov/regulations/pdf/ccpa_updates_cyber_risk_admt_noa.pdf) |
| **Correction to original framing** | The regulation's **general effective date is January 1, 2026** — not January 2027. **ADMT-specific compliance obligations** specifically are what's phased to **January 1, 2027** (any ADMT use before that date must be compliant by it; any use starting after must be compliant immediately) | Same sources; corroborated independently by a Future of Privacy Forum issue brief |
| Data-submission lag | Businesses don't have to submit risk-assessment information to CPPA until **April 1, 2028** (for assessments conducted 2026–27); cybersecurity audit reports aren't due until **April 1, 2028** at the earliest, staggered further by business size | [FPF issue brief](https://fpf.org/wp-content/uploads/2025/10/FPF_CCPA-Regulations-Issue-Brief.pdf) |
| Enforcement actions found | **None specific to ADMT.** A $1.35M CPPA enforcement action was found in the same period, but it targeted an unrelated violation (failure to update a posted privacy notice annually / opt-out signal handling), not ADMT or risk assessments. CPPA staff separately disclosed "hundreds of investigations... in progress" agency-wide, but none confirmed ADMT-specific | [Privacy World / Hunton, Oct 2025](https://www.privacyworld.blog/2025/10/california-privacy-agency-rolls-out-new-regulations-and-approves-1-35-million-penalty-in-latest-ccpa-enforcement-action/) |
| Rule-text amendments since finalization | **Not confirmed either way** — no amendments surfaced in the sources checked, but the search did not specifically and exhaustively sweep for post-finalization amendments; this should be treated as "none found" rather than "confirmed none exist" | — |
| Scope narrowing (context) | The final rule text was narrowed from the original 2024 draft — it dropped regulation of ADMT that merely "facilitates" (rather than makes) significant decisions, and narrowed the definition of "significant decisions" itself | Secondary source, Oct 2, 2025 |

### 4.2 Why no enforcement action is unsurprising (not itself evidence of anything)

Given the compliance and data-submission timeline above — ADMT compliance isn't mandatory until Jan 1, 2027, and CPPA doesn't receive its first tranche of risk-assessment data until April 2028 — the absence of an ADMT-specific enforcement action as of mid-2026 is expected, not a signal of lax enforcement. **This should be read as "too early for enforcement to have started," not "CPPA enforcement is being tested."**

### 4.3 Implications for the Workbench

1. **Correct deep-research-v1.md §3.2 and R-08's date characterization**: "compliance date Jan 2027" should be clarified as *ADMT-specific* compliance within an already-finalized, already-partially-effective (Jan 2026) regulation — not a rule that itself takes effect in 2027.
2. **Update W3's watchlist framing**: rather than "any enforcement actions," the more useful next checkpoint is **April 2028**, when the first risk-assessment submissions reach CPPA and enforcement becomes practically possible for the first time.
3. `admt_risk_assessment_summary.json` (§1.5 P3, §7.3) should reflect the corrected effective-date structure (general Jan 2026 / ADMT-specific Jan 2027 / data-submission Apr 2028) rather than a single flat "compliance date."

---

## 5. W4 — NY A773 / CA AB 1018: STILL OPEN for both, status materially updated

### 5.1 NY A773 (lending ADMT bill)

| Fact | Detail |
| ---- | ------ |
| Original version tracked in R-08 | A773B (per S-59) |
| Current status | **Superseded.** The bill has been amended twice since: A773B → **A773C** (amended and recommitted to the Codes committee **January 15, 2026**) |
| Current stage | A773C was reported out of committee and advanced to the **Assembly floor calendar** (third reading, calendar #393) on **April 30, 2026** |
| Since then | **No further recorded action** as of the research date — roughly three months dormant on the floor calendar |
| Enacted? | **No.** Has not passed either chamber, not delivered to the Governor, not signed |
| Companion bill | NY Senate bill **S8115** tracks the same amendment stage in parallel |
| Substance (confirmed) | Governs banks' use of automated tools in lending decisions; gives loan applicants a consent/opt-out right; requires annual disparate-impact analyses submitted to the Attorney General — confirms this is the lending-specific bill distinct from the insurance-only NY DFS Circular Letter 7, as R-08 originally characterized it |

Source: New York State Senate's own bill tracker — [nysenate.gov/legislation/bills/2025/A773/amendment/B](https://www.nysenate.gov/legislation/bills/2025/A773/amendment/B) and [.../amendment/C](https://www.nysenate.gov/legislation/bills/2025/A773/amendment/C).

### 5.2 CA AB 1018 (disparate-impact ADS bill)

| Fact | Detail |
| ---- | ------ |
| Introduced | February 20, 2025, by Assembly Member Bauer-Kahan |
| Amendment history | Six recorded amendments: Assembly 4/10/25, 5/1/25; Senate 7/3/25, 7/17/25, **9/5/25** (most recent as of research date) |
| Enacted? | **No.** No chapter number, no Governor action recorded — did not pass as a 2025 bill; rolls into the second year (2026) of the 2025–2026 legislative session |
| Debunked claim | One extraction agent explicitly flagged and **debunked a generic web-search summary that had incorrectly claimed AB 1018 passed both chambers by August 2025** — the official tracker shows no such passage. This is exactly the kind of false-positive the adversarial-verification design exists to catch, and it worked even at the single-extraction-agent level here |
| Substance | Requires developers to evaluate whether "disparate treatment is intended" or "disparate impacts are reasonably likely to occur"; civil penalties up to $25,000 per violation (AG/civil enforcement); requires a plain-language disclosure of the personal characteristics the automated decision system measures |

Source: California Legislature's own bill-history page — [leginfo.legislature.ca.gov, bill_id=202520260AB1018](https://leginfo.legislature.ca.gov/faces/billNavClient.xhtml?bill_id=202520260AB1018).

### 5.3 Implications for the Workbench

1. **Update deep-research-v1.md §10.3 W4**: both bills remain accurately described as "pending, not enacted" — R-08's original characterization holds — but the specifics are now current: NY is at A773C (not B) and stalled on the floor calendar since April 2026; CA AB 1018 has had five further amendments since R-08 and did not pass in 2025.
2. Update `source-ledger.md` S-59 (NY A773B) to point to the current A773C tracker page, and S-61 (CA AB 1018) with the updated amendment date (9/5/2025) and the debunked-passage note as a caution against relying on secondary summaries for bill status.
3. No action needed on Workbench scope — neither bill being enacted would trigger new overlay work (`NY_LENDING` / `CA_ADS` per §10.2 V4) until one actually passes, which hasn't happened.

---

## 6. Limitations of this document

1. **No adversarial verification for W2, W3, or W4.** Per instruction, the incomplete Verify stage was not resumed. Every claim in §3–§5 rests on a single fetch-and-extract pass, informally cross-referenced by me across the ~6 sources that touched each item, not on the project's normal 3-vote adversarial standard. Treat these sections as ⚠, not ✅, until a future session runs actual verification.
2. **Two claims (§3, credit-scope confirmation and enforcement-structure detail) could not be traced back to an exact URL** from the cached journal — the claim-extraction step's output schema captured the claim, its supporting quote, source quality, and publish date, but not the source URL itself, and the two entries in question don't correspond cleanly to any of the 5 search-angle results. They're flagged inline rather than given a fabricated citation.
3. **W3's "no enforcement action found" is a negative result from a limited sweep**, not an exhaustive search of CPPA's enforcement docket — the CPPA's own live announcements feed was only checked back to November 2024 in the cached extraction, which is itself a gap worth closing in a future pass.
4. **This document does not touch `deep-research-v1.md` or `source-ledger.md`.** All recommended edits above are proposals for a human reviewer to apply, consistent with how R-12 and R-13 were handled.
