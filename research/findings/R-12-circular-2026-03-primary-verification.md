# R-12 — CFPB Circular 2026-03 Primary-Source Verification (Ticket B7)

**Ticket:** B7 (deep-research-v1.md §10.1)
**Session:** 7 (ad hoc close-out)
**Status:** Complete
**Research date:** 2026-07-21
**Depends on:** R-02 (Reg B July 2026), R-04 (interpretability → adverse-action pipeline)
**Closes:** S-33 open item (source-ledger.md); B7 (deep-research-v1.md §10.1)

---

## 1. Purpose

R-04 and deep-research-v1.md §1.2 item #3, §3.1, and §4.2 all rest a **primary differentiator** — "CFPB Circular 2026-03 translation methodology artifact (SHAP → Reg B reasons)" — on **S-33**, sourced as "CFPB Circular 2026-03 (via R-02 + trade press)," flagged ⚠ (secondary/partial) because the primary circular text was never independently fetched. This ticket (B7) closes that gap by going directly to consumerfinance.gov, the Federal Register, and CFPB's own newsroom/search index.

**Claim under test** (as characterized in R-04 §2 and §5, and deep-research-v1.md §3.1/§4.2):
> "CFPB Circular 2026-03 (May 5, 2026): Reaffirms 2022-03/2023-03 after May 2025 withdrawal; adds explicit requirement to document how model outputs translate to consumer-facing explanations so fair lending reviewers can independently validate."

---

## 2. Executive finding

**❌ NOT FOUND / UNSUBSTANTIATED — "CFPB Circular 2026-03" does not exist as a published primary source.**

After a systematic search of (a) the CFPB circulars index, (b) CFPB's own site search, (c) CFPB's Newsroom press-release archive back through February 2025, and (d) the Federal Register (both full-text search and direct API queries), **no CFPB circular numbered 2026-03, nor any CFPB circular of any number issued in 2025 or 2026, could be located.** The last CFPB circular still listed on the live Guidance index is **Circular 2024-07** (Dec. 30, 2024). **Erratum (R-14):** Circular 2024-07 was **not** withdrawn in the May 12, 2025 wave and remains active; the adverse-action circulars 2022-03 and 2023-03 **were** withdrawn.

Separately, and more consequentially for the Workbench's messaging: **Circular 2022-03 and Circular 2023-03 — the two circulars R-04 relies on as its statutory/interpretive anchor for the adverse-action translation pipeline — were themselves withdrawn by the CFPB on May 12, 2025**, per the Bureau's own "Withdrawn Guidance" index and the underlying Federal Register withdrawal rule (90 FR 20084 / doc. 2025-08286, "Interpretive Rules, Policy Statements, and Advisory Opinions; Withdrawal"). R-04 and R-02 were aware of a "May 2025 withdrawal" in passing, but characterized Circular 2026-03 as having "reaffirmed" 2022-03/2023-03 afterward — that reaffirmation did not happen (as far as any publicly available primary source shows).

The underlying **statute and regulation are unaffected** — ECOA §701(d) and Reg B §1002.9 (the specific-reasons requirement) are not circulars, were not withdrawn, and remain in force. What is unsupported is the claim that CFPB currently has (or ever issued) **guidance specifically requiring a documented SHAP/attribution-to-reason "translation methodology" artifact**. That specific requirement, as framed, has no primary-source basis found in this session.

---

## 3. What was checked

| # | Check | Result |
| - | ----- | ------ |
| 1 | `consumerfinance.gov/compliance/circulars/` (CFPB's circulars index) | Redirects to `/compliance/guidance/` — a full chronological list of every circular/bulletin CFPB has issued since 2011. **Most recent entry: Circular 2024-07 (Dec 30, 2024).** No 2025 or 2026 circular of any number appears. |
| 2 | Direct URL guesses for a `circular-2026-03-*` slug (4 plausible patterns, matching the URL convention CFPB actually uses) | All **404**. |
| 3 | CFPB site search (`consumerfinance.gov/search/?q=Circular 2026-03`) | 71 fuzzy results, none of which is a 2026 circular. Top hits are Circular 2023-03, Circular 2022-03, and the "Withdrawn Guidance" page. |
| 4 | CFPB Newsroom, all press releases Feb 2025 → present (19 filtered results, latest Jun 25, 2026) | No press release announcing any new circular, and no AI/SHAP/adverse-action/explainability item at all. |
| 5 | Federal Register API — full-text search for `"Circular 2026-03"` from CFPB | **`count: 0`.** |
| 6 | Federal Register API — all CFPB documents containing "circular," published ≥ 2025-01-01 | **12 results**, all either OMB Circular A-108 citations (unrelated) or the May 12, 2025 withdrawal rule itself. **Zero are new CFPB circulars.** |
| 7 | Federal Register API — CFPB documents matching "artificial intelligence adverse action" since 2025-01-01 | 3 results: the Reg B final rule (91 FR 21620), and two unrelated policy statements (No-Action Letters, Sandbox). Nothing on SHAP/translation methodology. |
| 8 | Full text of the April 22, 2026 Reg B final rule (91 FR 21620 / doc. 2026-07804), downloaded and grepped | **Zero occurrences** of "SHAP," "attribution," "translation methodology," "adverse action," or any circular citation. Confirms (independently of R-02) that this rule is scoped only to disparate impact / discouragement / SPCP — R-02's own characterization is correct, and §1002.9 adverse-action content is untouched by it. |
| 9 | Circular 2022-03 primary page (fetched directly) | ✅ Live, full text matches R-04's quoted holding verbatim ("such explanations approximate models and creditors must still be able to validate the accuracy of those approximations...") — but see §4 below on withdrawal status. |
| 10 | Circular 2023-03 primary page (fetched directly, corrected URL — R-04 cites the right substance but the ledger doesn't record the actual title) | Page renders an **"Archived content" banner** ("Content has been archived," last modified Apr. 11, 2025) rather than the live circular text. |
| 11 | CFPB "Withdrawn Guidance" index, full text | Explicitly lists: **"Consumer Financial Protection Circular 2022-03: Adverse Action Notification Requirements in Connection With Credit Decisions Based on Complex Algorithms, 87 FR 35864 (June 14, 2022); withdrawn on May 12, 2025"** and **"Consumer Financial Protection Circular 2023-03: Adverse Action Notification Requirements and Proper Use of Sample Forms, ...; withdrawn on May 12, 2025."** |
| 12 | Innovation Spotlight blog (S-32), re-fetched | Still live/archived at its original URL, last modified Jun 25, 2026; content matches R-04's characterization; no mention of Circular 2026-03. |

---

## 4. Claim-by-claim verification

| Claim (source) | Verdict | Basis |
| --------------- | :-----: | ----- |
| "CFPB Circular 2026-03" exists as a published document | ❌ | Not found on consumerfinance.gov, in CFPB's own search index, in CFPB Newsroom (Feb 2025–Jun 2026), or in the Federal Register (0 results for exact-phrase and topical searches) |
| Circular 2026-03 published "May 5, 2026" | ❌ | No such document at that or any nearby date; CFPB press releases around that window (Feb 17, Mar 31, Jun 2, Jun 24, Jun 25 2026) cover unrelated topics (cost estimates, HMDA data, Bilt, complaint system, financial-data reporting standard) |
| Circular 2026-03 "reaffirms 2022-03/2023-03 after May 2025 withdrawal" | ❌ | Withdrawal is confirmed (✅) — both circulars are on CFPB's own "Withdrawn Guidance" list, withdrawn May 12, 2025, per Federal Register doc. 2025-08286 — but no reaffirming circular has been located |
| Circular 2026-03 "adds explicit requirement to document how model outputs translate to consumer-facing explanations" | ❌ | No primary text exists to support this; not present in any 2025–2026 CFPB circular, blog post, or Federal Register document found |
| "Circular 2026-03 translation methodology... still operative" (deep-research-v1.md §3.1, §4.2) | ❌ | Cannot be "operative" — no such circular exists to be operative |
| Circular 2022-03 black-box holding still "operative"/current CFPB guidance (R-04 §2, S-18 ✅ in ledger) | ⚠ **Revise** | Underlying statute/regulation (ECOA §701(d), Reg B §1002.9, Official Interpretation) is unaffected and still binding law — but the **circular itself was formally withdrawn May 12, 2025** per CFPB's own withdrawal index. The circular's *page* on consumerfinance.gov oddly still renders full live text with no archived banner (inconsistent with the withdrawal index — see caveat below), so the practical guidance content is still publicly visible, but its official status as **current CFPB guidance** is not accurate as stated |
| Circular 2023-03 specificity/checklist-insufficiency holding still "operative" (R-04 §2, S-31 ✅ in ledger) | ⚠ **Revise** | Same as above — also on the withdrawal list (May 12, 2025), and unlike 2022-03, its own page **does** show the "Archived content" banner, confirming withdrawn status is reflected on-site |
| Reg B July 2026 rule (91 FR 21620) scoped only to disparate impact/discouragement/SPCP, §1002.9 untouched (R-02) | ✅ | Independently confirmed by downloading and grepping the full 51-page rule text — zero mentions of adverse action, SHAP, attribution, or circulars |
| CFPB withdrew ~39+ guidance documents on May 12, 2025 (context both R-02 and R-04 allude to) | ✅ | Confirmed via Federal Register doc. 2025-08286 ("Interpretive Rules, Policy Statements, and Advisory Opinions; Withdrawal") and the CFPB "Withdrawn Guidance" page, which lists every item with its withdrawal date |

---

## 5. Important context found (not previously in the research findings)

1. **CFPB's 2025–2026 posture is broadly deregulatory**, which makes the "reaffirmation" narrative implausible on its face, independent of the direct-evidence absence above. Newsroom items in the same window include: "CFPB Keeps Its Enforcement and Supervision Resources Focused on Pressing Threats to Consumers" (Apr 30, 2025), a Supervision Division "Humility Pledge" reducing exam scrutiny (Nov 21, 2025), and the blanket May 2025 guidance withdrawal. An agency actively withdrawing guidance and de-prioritizing supervision is not a strong candidate to have quietly issued a **new, more prescriptive** circular on AI model explainability in the same period. This is circumstantial, not primary-source proof of non-existence, but it corroborates the direct search results.
2. **Site inconsistency worth flagging for future spot-checks:** Circular 2022-03's live page shows no "archived" banner and renders full text, while Circular 2023-03's page does show the banner. Both are listed as withdrawn on the same date (May 12, 2025) on CFPB's own index. This could be a CMS lag/inconsistency on CFPB's side rather than a substantive distinction — but anyone citing "Circular 2022-03 is live and current" should know the Bureau's own index disagrees.
3. R-02's headline claim (91 FR 21620, effective July 21, 2026, disparate-impact/discouragement/SPCP amendments) is **independently corroborated** by this session via the Federal Register API and full-text download — this strengthens confidence in R-02's non-Circular-2026-03 findings.

---

## 6. Implications for the Workbench

1. **Do not ship "CFPB Circular 2026-03" as a named, citable authority.** No primary source supports its existence. Any build collateral, demo narrative, or examiner packet referencing "Circular 2026-03" should be corrected or removed before it ships (this was exactly the risk ticket B7 was opened to catch).
2. **The underlying design is still defensible — just needs correct sourcing.** R-04's four-stage SHAP → Reg B translation pipeline is good practice and consistent with real, verified primary sources: Circular 2022-03's black-box holding, Circular 2023-03's specificity/checklist-insufficiency examples, the 2020 Innovation Spotlight blog (S-32), and Reg B §1002.9 + Official Interpretation (S-34) itself. None of those require Circular 2026-03 to exist — the differentiator can be repositioned as "encodes CFPB's 2020–2023 adverse-action guidance (Circular 2022-03, 2023-03) into an auditable artifact," which is both true and still a genuine market gap per R-01.
3. **Flag the withdrawal status explicitly in Workbench documentation.** Since 2022-03 and 2023-03 are formally withdrawn CFPB guidance (even though still reachable at their original URLs, and even though the statute/regulation they interpret remains binding), the Workbench's "do-not-claim" messaging discipline (deep-research-v1.md §1.7, R-04 §8 item 7: "do not claim legal compliance") should be extended to: do not claim the translation-methodology artifact satisfies **current, non-withdrawn CFPB guidance** — frame it instead as aligning with the **statutory** ECOA/Reg B §1002.9 requirement and with **historical CFPB interpretive positions**, which remain persuasive/best-practice evidence even though formally withdrawn as active guidance.
4. **This does not affect the OCC 2026-13 or Colorado/California/NY overlay differentiators** (items #1 and #2 in deep-research-v1.md §1.2) — those rest on separately verified sources (S-15, S-38, S-52–S-58) untouched by this check.

---

## 7. Recommendation on S-33 (source-ledger.md)

**Downgrade S-33 from ⚠ to ❌.**

Rationale:
- ⚠ ("secondary/partial") implies the primary document exists but simply hasn't been independently fetched yet. That is not the situation here: after a direct, multi-angle search of the primary source (CFPB.gov circulars index, CFPB search, CFPB Newsroom, Federal Register full-text and API), **the document itself cannot be located and there is no positive evidence it was ever published.**
- The specific content attributed to S-33 (a "documented translation methodology" requirement, dated May 5, 2026, reaffirming withdrawn 2022-03/2023-03) has **no primary corroboration**. **R-14 close-out:** the "NMP May 2026" secondary was located as NMP Jul 9, 2026 (Andrew Liput) — it **exists but invents Circular 2026-03**; treat as ❌ false secondary (proposed ledger S-84), not as corroboration.
- ❌ is the correct label per the source-ledger's own legend: "unverified or inaccessible" — the primary document cannot be located; the only secondary located is contradicted by CFPB's own indexes.

**Recommended follow-on edits for the human reviewer (not made by this agent, per instructions):**
- `source-ledger.md` S-33: change status ⚠ → ❌; update Notes to "CFPB Circular 2026-03 not found — see R-12; no primary or secondary source located as of 2026-07-21."
- `source-ledger.md` S-18 and S-31 (Circular 2022-03, 2023-03): consider annotating Notes with "Formally withdrawn by CFPB May 12, 2025 (still reachable at original URL); underlying ECOA/Reg B statute unaffected" rather than leaving them as unqualified ✅ "current."
- `deep-research-v1.md` §1.2 item #3: reword the differentiator away from citing "CFPB Circular 2026-03" by name — e.g., "Documented SHAP → Reg B §1002.9 adverse-action translation methodology artifact, aligned with CFPB's 2022-03/2023-03 interpretive history" — and update §3.1's table row and §4.2's "Regulatory anchors" line accordingly.
- `deep-research-v1.md` §10.1 ticket B7: mark resolved, with disposition "Circular 2026-03 not found; differentiator #3 requires rewording — see R-12."
- `research/findings/R-04-interpretability-adverse-action.md` §2, §5, §9, §10 item 1: same correction — remove or heavily caveat the Circular 2026-03 references throughout.

---

## 8. Sources

| ID (proposed) | Source | Tier | Status | Used for |
| -- | ------ | ---- | ------ | -------- |
| S-62 | CFPB Guidance index (`consumerfinance.gov/compliance/guidance/`) | 1 | ✅ | Chronological circular list; confirms 2024-07 is the last-issued circular |
| S-63 | CFPB Circular 2022-03 primary page (re-fetched) | 1 | ✅ | Live text matches R-04 quote; no archived banner despite withdrawal listing |
| S-64 | CFPB Circular 2023-03 primary page (re-fetched, corrected URL) | 1 | ✅ | Confirms "Archived content" status, Apr 11, 2025 |
| S-65 | CFPB "Withdrawn Guidance" index | 1 | ✅ | Explicit withdrawal dates for 2022-03 and 2023-03 (May 12, 2025) |
| S-66 | Federal Register doc. 2025-08286 ("Interpretive Rules, Policy Statements, and Advisory Opinions; Withdrawal," 90 FR 20084, May 12, 2025) | 1 | ✅ | Primary withdrawal rule; lists withdrawn circulars including 2024-06 (last one issued before withdrawal wave) |
| S-67 | Federal Register API — document search, `"Circular 2026-03"`, CFPB agency filter | 1 | ✅ | `count: 0` — direct negative evidence |
| S-68 | Federal Register API — document search, `"circular"`, CFPB, ≥2025-01-01 | 1 | ✅ | 12 results, none a new CFPB circular |
| S-69 | Federal Register doc. 2026-07804 (91 FR 21620, Reg B final rule), full text download | 1 | ✅ | Confirms R-02 scope claim; zero adverse-action/SHAP content |
| S-70 | CFPB Newsroom press-release archive, Feb 2025–Jun 2026 (19 filtered results) | 1 | ✅ | No circular announcement, no AI/explainability item |
| S-71 | CFPB Innovation Spotlight blog (S-32, re-fetched) | 1 | ✅ | Confirms still-live, unchanged, no Circular 2026-03 reference |

---

## 9. Open questions

**All closed in R-14** (`research/findings/R-14-r12-r13-closeout-amendment-proposal.md`):

1. **Trade press ("NMP May 2026")** — ✅ **CLOSED.** Located: NMP Jul 9, 2026 (Liput). Invents Circular 2026-03; false secondary (S-84). Remove as corroboration.
2. **CFPB reissue of AI/adverse-action guidance** — ✅ **CLOSED → watchlist W7.** Unknown; deregulatory posture; monitor only.
3. **OCC/Fed/FDIC gap fill** — ✅ **CLOSED.** OCC 2026-13 does not prescribe a SHAP→reason translation methodology artifact. Anchor remains ECOA/Reg B §1002.9.
