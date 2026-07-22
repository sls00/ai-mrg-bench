# R-13 — Competitive Landscape Source Spot-Check (S-01, S-02)

**Ticket:** R-13
**Session:** 1 (spot-check / due-diligence gap-fill on R-01)
**Status:** Complete
**Research date:** 2026-07-21
**Scope:** Primary-source verification of two ⚠-labeled sources underpinning `deep-research-v1.md` §2.1/§2.2 and `R-01-tier3-competitive-landscape.md` §2.1/§2.2 — S-01 (Chartis MRM Solutions 2024, accessed via Genpact PDF mirror) and S-02 (Gartner MQ AI Governance Platforms, June 2026, paywalled). Also checks for independent (non-Chartis, non-Gartner) analyst corroboration of the vendor tiering used in the comparison matrix.

---

## 1. Executive summary

Both S-01 and S-02 hold up better than their ⚠ label implied, but for different reasons — and one specific claim in `deep-research-v1.md` §2.1 needs softening.

- **S-01 (Chartis MRM 2024):** The Genpact-hosted PDF is not an ad hoc "mirror" — it is a Chartis/Infopro Digital–copyrighted, single-license reprint (same distribution model SAS uses for its own Chartis vendor analysis). I read the full 18-page report directly (all three RiskTech Quadrant figures, all six capability tables, exact vendor lists). Its content is independently corroborated, vendor-name-for-vendor-name, star-rating-for-star-rating, by **four separate wire-service press releases** (ValidMind, SAS, CRISIL, Evalueserve), each quoting the same named Chartis chief researcher (Sid Dash) on the record. **Verdict: ✅ Upgrade.**
- **S-02 (Gartner MQ AI Governance Platforms, Jun 2026):** The MQ document itself remains paywalled, but every one of the 13 vendor placements used in R-01/deep-research-v1.md (3 Leaders, 5 Visionaries, 1 Challenger, 4 Niche) is now independently confirmed via direct vendor press releases for 7 of the 13 vendors, plus a detailed independent analyst breakdown (Sanjeev Mohan, ex-Gartner VP Analyst) that lists the identical quadrant assignments. Zero contradictions found across 10 independent sources. **Verdict: ⚠→ strong ⚠ (materially higher confidence); recommend narrative update, not a paywall-access upgrade.**
- **Independent cross-analyst corroboration of the vendor tiering (Forrester Wave, IDC MarketScape, Evident AI Index):** **Not available, and this is a real, structural gap, not a research miss.** Forrester's "AI Governance Solutions, Q3 2025" Wave and IDC's "Unified AI Governance Platforms 2025–2026" MarketScape evaluate a *different, largely non-overlapping* vendor set (Credo AI, IBM, ServiceNow, Dataiku, Microsoft — the Layer B/GRC vendors) than Chartis's "Model Risk Management Solutions" quadrants (ValidMind, SAS, CRISIL, Genpact — Layer A). **No second analyst firm currently rates ValidMind, SAS MRM, or Solytics against each other.** Chartis is the sole quadrant-style source for that specific market segment. Evident AI Index remains, as R-01 already found, a bank-maturity ranking, not a vendor landscape — confirmed, no change.
- **One claim needs softening:** `deep-research-v1.md` §2.1 states ValidMind is "the strongest direct MRM competitor (Chartis leader all three quadrants)" as if triple-quadrant leadership were unique to ValidMind. Having read the primary report, **two other vendors — CRISIL Integral IQ and Evalueserve — also land in the "Category leaders" box in all three quadrants** (derivatives validation, credit validation, model governance). ValidMind's actual differentiator for Workbench-relevance purposes is that it's the only one of the three that is a pure-play, API/SDK-native MRM *software* vendor with modern AI/agentic-governance positioning — CRISIL and Evalueserve are validation/advisory-services firms in the same tier as KPMG/PwC. See §6 for recommended rewording.

---

## 2. S-01 — Chartis "Model Risk Management Solutions, 2024: Quadrant Update"

### 2.1 What I did

Fetched the Genpact-hosted PDF directly (`https://www.genpact.com/content/dam/genpact/web/documents/Chartis_model_report.pdf`) and read the full 18-page document (Read tool, not just a WebFetch summary). Cross-checked its content against:
- Chartis's own landing page for the same report (chartis-research.com — public metadata only, full content paywalled)
- Four independent vendor press releases announcing their placement in the *same* report
- Genpact's own press release about its *own* placement

### 2.2 Primary document findings (full report, read directly)

**Report:** "Model Risk Management Solutions, 2024: Quadrant Update," Chartis Research (Infopro Digital), published 06 Dec 2024, authors Phil Mackenzie, Ahmad Kataf, Sid Dash. Copyright notice confirms this is a licensed, single-print reprint distributed via Genpact — the same reprint-rights model SAS uses on its own site (`sas.com/.../chartis-model-risk-management-vendor-analysis-*.pdf`), i.e. this is standard analyst-firm reprint distribution, not an unauthorized scrape.

**30 vendors covered** (exact match to R-01 §2.1 list — verbatim confirmed): Acadia (LSEG), Analytics Boutique, BCT Digital, Bloomberg, CIMCON Software, CRISIL, DataRobot, Evalueserve, Finastra, FIS, Genpact, IBM, ICE Data Services, Infosys, KPMG, MathWorks, MatLogica, MetricStream, Mitratech, Numerix, Prometeia, PwC, RiskSpan, SAS, TCS, TurinTech, ValidMind, Wipro, Wolters Kluwer, Yields.

**Three RiskTech Quadrant figures, read directly (not summarized):**

| Quadrant | Vendors in "Category leaders" box (top-right: high market potential + high completeness of offering) |
| -------- | ------------------------------------------------------------------------------------------------------ |
| Fig. 1 — Model validation (derivatives) | CRISIL, Numerix, **ValidMind**, KPMG, PwC, RiskSpan, Evalueserve |
| Fig. 2 — Model validation (credit) | **ValidMind**, CRISIL, Genpact, Evalueserve, KPMG, Prometeia, ICE Data Services, RiskSpan, MathWorks, Acadia, BCT Digital, PwC, TCS, Wipro, DataRobot, Yields, Infosys, SAS |
| Fig. 3 — Model governance | **SAS** (furthest top-right — top score), **ValidMind**, KPMG, DataRobot, Evalueserve, PwC, MathWorks, TCS, IBM, CRISIL, Mitratech, Prometeia, MetricStream, BCT Digital, Yields |

**Capability tables (star ratings, Tables 2/4/6) — spot-checked against vendor claims:**
- **SAS**, model governance table: ★★★★★ on 5 of 6 criteria (model coverage, governance, data mgmt, model inventory, dashboarding), ★★★★ on visualization — matches SAS's own claim of "top score of any vendor" among the **19 vendors** in that quadrant (I counted 19 rows in Table 6 — exact match to R-01's cited figure).
- **ValidMind**, same table: ★★★★★ on 4 of 6 criteria, ★★★★ on 2 — a strong but not top score; ValidMind is in the "Category leaders" box in all three figures, but SAS specifically out-scores it on governance-quadrant completeness.
- **CRISIL**: perfect ★★★★★ sweep in both derivatives (Table 2) and credit (Table 4) tables — the only vendor with a full 5-star sweep in either validation table — and present in the "Category leaders" box in all three figures, same triple-quadrant status as ValidMind.
- **Evalueserve**: also present in the "Category leaders" box in all three figures.

### 2.3 Independent vendor-press corroboration (four separate wire releases)

| Vendor | Source | Claim | Cross-check against primary PDF |
| ------ | ------ | ----- | -------------------------------- |
| ValidMind | [Business Wire, 6 Dec 2024](https://www.businesswire.com/news/home/20241206365623/en/ValidMind-Recognized-as-a-Three-Time-Category-Leader-in-Chartis-Research%E2%80%99s-Model-Risk-Validation-2024-Report); [ValidMind blog](https://validmind.com/blog/validmind-recognized-as-a-three-time-category-leader-in-chartis-research-model-risk-validation-2024-report/) | "Category leader in all three quadrants"; quotes Sid Dash on ValidMind's cross-over of statistical/AI + traditional quant validation | ✅ Matches — ValidMind is in the Category-leaders box in Figs. 1, 2, 3 |
| SAS | [PR Newswire, 30 Jan 2025](https://www.prnewswire.com/news-releases/sas-named-by-chartis-as-a-leader-for-model-risk-management-302364465.html); [sas.com](https://www.sas.com/en_us/news/analyst-viewpoints/chartis-risktech-quadrant-model-risk-management.html) | "11th straight year" leader; top score among 19 vendors in governance; quotes Sid Dash on "growing salience of AI models" | ✅ Matches — SAS is furthest top-right in Fig. 3; Table 6 has 19 rows; SAS has near-perfect star sweep |
| CRISIL | [PR Newswire, Jan 2025](https://www.prnewswire.com/news-releases/crisil-integral-iq-wins-multiple-recognitions-in-the-chartis-risktech-model-risk-management-2024-quadrants-report-302359629.html) | "Multiple recognitions" across MRM quadrants | ✅ Matches — CRISIL in Category-leaders box in all 3 figures; perfect star sweep in Tables 2/4 |
| Evalueserve | [evalueserve.com](https://www.evalueserve.com/news/evalueserve-named-category-leader-by-chartis-research-in-three-model-risk-management-quadrants/) | "Category Leader... in Three Model Risk Management Quadrants" | ✅ Matches — Evalueserve in Category-leaders box in all 3 figures |
| Genpact | [genpact.com](https://www.genpact.com/insight/chartis-names-genpact-a-leader-in-model-risk-management-solutions) | Leader in credit validation quadrant only | ✅ Matches — Genpact appears in credit quadrant (Fig. 2) category-leaders box; appears in "Enterprise solutions" (not category leaders) in Fig. 3 governance — Genpact's own release correctly does *not* claim a governance-quadrant leader spot |

No contradictions found anywhere across five independent corroborating parties (four vendors + Chartis's own site metadata).

### 2.4 Verdict on S-01

**✅ Upgrade recommended.** This is no longer "secondary access via third-party mirror" — it is (a) a licensed reprint of the primary document, content read in full, and (b) independently corroborated on every checkable data point (vendor list, quadrant placement, star ratings, vendor counts, named-analyst quotes) by four separate, on-the-record wire-service press releases from four different companies. The only residual caveat: I cannot 100% rule out that Genpact's hosted PDF differs from Chartis's paid-subscriber master copy (e.g., a later addendum), but the "printing limited to a single copy" / Infopro Digital copyright footer indicates this is the licensed distribution copy, not a stripped-down excerpt.

---

## 3. S-02 — Gartner Magic Quadrant for AI Governance Platforms (June 2026)

### 3.1 What I did

Could not access the Gartner document itself (`gartner.com/en/documents/8006369` — paywalled, as expected). Instead corroborated every vendor placement in R-01's S-02 table against (a) direct vendor press releases/pages and (b) an independent analyst's detailed breakdown.

### 3.2 Corroboration table

| Quadrant (per R-01/deep-research-v1.md) | Vendor | Corroborating source | Type |
| --- | --- | --- | --- |
| Leader | IBM | [ibm.com announcement](https://www.ibm.com/new/announcements/ibm-recognized-as-a-leader-in-gartner-magic-quadrant-for-ai-governance-platforms) | Direct vendor press |
| Leader | Truyo | [PR Newswire, 22 Jun 2026](https://www.prnewswire.com/news-releases/truyo-named-a-leader-in-the-2026-gartner-magic-quadrant--for-ai-governance-platforms-302806625.html) | Direct vendor press |
| Leader | ServiceNow | [Sanjeev Mohan / Medium](https://sanjmo.medium.com/inside-gartners-first-ai-governance-platform-magic-quadrant-fa1f182f75e9) | Independent analyst secondary |
| Visionary | Credo AI | [credo.ai recognition page](https://www.credo.ai/recognition/gartner-magic-quadrant-ai-governance-platforms-2026) | Direct vendor press |
| Visionary | ModelOp | [modelop.com/gartner](https://www.modelop.com/gartner); [modelop.com blog](https://www.modelop.com/blog/modelop-named-visionary-gartner-magic-quadrant-ai-governance-platforms) | Direct vendor press |
| Visionary | Monitaur | [Business Wire, 30 Jun 2026](https://www.businesswire.com/news/home/20260630461104/en/Monitaur-Recognized-as-Visionary-in-the-Inaugural-2026-Gartner-Magic-Quadrant-for-AI-Governance-Platforms) | Direct vendor press |
| Visionary | OneTrust | [onetrust.com resources](https://www.onetrust.com/resources/gartner-magic-quadrant-for-ai-governance-platforms-2026-report/) | Direct vendor press |
| Visionary | Airia | [airia.com blog](https://airia.com/blog/airia-named-as-a-visionary-in-the-2026-gartner-magic-quadrant-for-ai-governance-platforms/) | Direct vendor press |
| Challenger | Holistic AI | Sanjeev Mohan / Medium; [getaigovernance.net](https://getaigovernance.net/blog/gartner-lists-3-leaders-of-ai-governance) | Independent secondary (2 sources agree) |
| Niche | Cranium AI, Relyance AI, Saidot, SAP | Sanjeev Mohan / Medium; getaigovernance.net | Independent secondary (2 sources agree) |

Sanjeev Mohan (independent industry analyst, formerly VP Analyst at Gartner covering data/AI, now running his own advisory) published a detailed, vendor-by-vendor breakdown of the full 13-vendor MQ — including quadrant assignments, per-vendor commentary (e.g., ModelOp "ties IBM for top scores in AI Agent Governance" but "offers no public SaaS option"), and independent market commentary ("There is no single winner. Pick your use case first, then pick your platform"). This is a non-vendor, non-Gartner-employee source and it matches R-01's S-02 table exactly — all 13 vendors, all four quadrant tiers, zero discrepancies.

**Market context corroborated too:** both vendor press and the independent Medium piece agree this is Gartner's *first-ever* dedicated AI Governance Platforms MQ (13 vendors, market growing from ~$65M in 2024 to a projected ~$1.4B by 2030 at ~67.5% CAGR) — consistent with R-01's framing of this as an emergent, newly-formalized category.

### 3.3 Verdict on S-02

**⚠ retained, but confidence materially strengthened — not a paywall-access upgrade, but a corroboration upgrade.** The underlying Gartner MQ document is still inaccessible, so the ⚠ (paywalled primary) label is technically still correct. But R-01's original note ("vendor press + secondary summaries — full MQ paywalled") undersold how solid the corroboration actually is: 7 of 13 vendor placements are confirmed by that vendor's own dated press release, and the remaining 6 are confirmed by an independent (non-Gartner, non-vendor) analyst's detailed writeup that agrees point-for-point with the vendor-sourced placements. No source anywhere contradicts another. Recommend the ledger note be updated to something like: *"MQ document paywalled; all 13 vendor placements cross-confirmed via 7 direct vendor press releases + 1 independent ex-Gartner analyst breakdown; zero contradictions."*

---

## 4. Independent cross-analyst corroboration attempt (Forrester Wave / IDC MarketScape / Evident AI Index)

### 4.1 Forrester Wave: AI Governance Solutions, Q3 2025

Confirmed to exist ([Forrester report page](https://www.forrester.com/report/the-forrester-wave-tm-ai-governance-solutions-q3-2025/RES184849)). Leaders: **Credo AI**, **IBM** (both also appear in Gartner's MQ — consistent). Monitaur: Strong Performer + "Customer Favorite" ([Monitaur/Business Wire, 27 Aug 2025](https://www.businesswire.com/news/home/20250827550651/en/Monitaur-Recognized-as-a-Customer-Favorite-in-Groundbreaking-AI-Governance-Market-Assessment)) — also consistent with its Gartner Visionary status. Holistic AI is mentioned in coverage of this Wave for its "Guardian Agents" runtime capability.

**Critically: I found no evidence ValidMind, SAS, or Solytics were evaluated in this Wave at all.** This Forrester report evaluates the Layer B "AI governance/GRC" vendor set, not Layer A "MRM lifecycle" vendors. (One WebSearch result summary initially conflated Monitaur's Forrester scoring language with ValidMind — I checked this directly and it does not hold up; ValidMind's own site and press make no mention of a Forrester Wave placement. Flagging this explicitly since it could otherwise get miscited downstream.)

### 4.2 IDC MarketScape: Worldwide Unified AI Governance Platforms, 2025–2026

Confirmed to exist (20 vendors evaluated). Leaders: **Dataiku**, **IBM**, **Microsoft** ([Microsoft Security Blog, 14 Jan 2026](https://www.microsoft.com/en-us/security/blog/2026/01/14/microsoft-named-a-leader-in-idc-marketscape-for-unified-ai-governance-platforms/); [IBM](https://www.ibm.com/new/announcements/ibm-named-a-leader-in-the-2025-idc-marketscape-worldwide-unified-ai-governance-platforms-2025-vendor-assessment); [Dataiku](https://www.dataiku.com/blog/idc-ai-governance-leader)). Again, **no evidence of ValidMind, SAS, or Solytics appearing in this vendor set** — same Layer B/broader-governance scope as the Forrester Wave and Gartner MQ, not the Layer A MRM category.

### 4.3 Evident AI Index

No new work needed — R-01 §2.3 already correctly characterizes this as a bank-maturity ranking (Talent/Innovation/Leadership/Transparency), not a vendor competitive landscape. Confirmed still accurate; not usable for vendor-tiering corroboration.

### 4.4 Structural finding

**There is currently no analyst firm other than Chartis that publishes a quadrant/wave/marketscape specifically for "Model Risk Management software" as a category.** Forrester, Gartner, and IDC have all converged on covering "AI Governance Platforms" as the emergent category, and that vendor set (IBM, ServiceNow, Credo AI, ModelOp, Monitaur, Holistic AI, OneTrust, Dataiku, Microsoft, Truyo, Airia, etc.) barely overlaps with Chartis's MRM vendor set (ValidMind, SAS, CRISIL, Genpact, Evalueserve, KPMG, PwC, DataRobot, etc.) — DataRobot and IBM are the only names that appear in both worlds among the vendors this project tracks. This means **the specific competitive claim "ValidMind is the strongest direct MRM competitor" cannot be, and structurally never could be, cross-checked against a second analyst firm** — not because the research was incomplete, but because no second firm rates that specific market segment. This is worth stating explicitly in the workbench-facing document rather than leaving it implied by a lone ⚠ tag.

### 4.5 Bonus finding — Chartis's own newer report shifts Solytics's status

Chartis published a separate, newer **"RiskTech Quadrant for AI Governance Solutions, 2025/2026"** (distinct from the 2024 MRM report S-01 covers). **Solytics Partners was named Category Leader** in that report ([Yahoo Finance / Solytics press](https://finance.yahoo.com/sectors/technology/articles/solytics-partners-named-category-leader-130000450.html); [sas.com reference](https://www.sas.com/en_us/news/analyst-viewpoints/chartis-risktech-quadrant-ai-governance-solutions.html)). This postdates and supersedes R-01 §4.3's "⚠ No Chartis quadrant leader status found" note for Solytics — Solytics *is* now a Chartis category leader, just in the newer AI Governance quadrant, not the 2024 MRM one that S-01 covers. Flagged for R-09/future-ticket awareness; out of scope to resolve fully here since it's a different report than the one S-01 cites.

---

## 5. Sources used in this spot-check (proposed new ledger entries)

| Proposed ID | Source | Tier | Access | Notes |
| ----------- | ------ | ---- | ------ | ----- |
| S-62 | Chartis "Model Risk Management Solutions, 2024: Quadrant Update" — full PDF via genpact.com (licensed reprint) | 3 | ✅ Read in full | Same document as S-01; full text/figures/tables read directly, not summarized |
| S-63 | ValidMind Chartis-recognition press release (Business Wire + validmind.com) | 3 | ✅ | Corroborates S-01/S-03 |
| S-64 | SAS Chartis-recognition press release (PR Newswire + sas.com) | 3 | ✅ | Corroborates S-01/S-04; 19-vendor governance count confirmed |
| S-65 | CRISIL Chartis-recognition press release (PR Newswire) | 3 | ✅ | New — CRISIL triple-quadrant status confirmed |
| S-66 | Evalueserve Chartis-recognition press release (evalueserve.com) | 3 | ✅ | New — Evalueserve triple-quadrant status confirmed |
| S-67 | Chartis-research.com public report landing page (metadata only) | 3 | ✅ (metadata) / ❌ (full text paywalled) | Confirms authors, date, existence; no vendor data public |
| S-68 | Gartner MQ AI Governance Platforms — vendor press releases (IBM, Truyo, Credo AI, ModelOp ×2, Monitaur ×2, OneTrust, Airia) | 3 | ✅ | Corroborates S-02; 7 of 13 vendors direct-confirmed |
| S-69 | Sanjeev Mohan (independent ex-Gartner analyst) — "Inside Gartner's First AI Governance Platform Magic Quadrant," Medium, Jul 2026 | 2 | ✅ | Non-vendor, non-Gartner corroboration of all 13 MQ placements |
| S-70 | getaigovernance.net — "Gartner's First AI Governance Magic Quadrant" | 3 | ⚠ Secondary | Same site as existing S-11; used only as a second cross-check on Niche/Challenger tier |
| S-71 | Forrester Wave: AI Governance Solutions, Q3 2025 (report page + Credo AI/Monitaur press) | 3 | ⚠ Secondary (report itself paywalled) | Confirms Layer B vendor set does not include ValidMind/SAS/Solytics |
| S-72 | IDC MarketScape: Worldwide Unified AI Governance Platforms, 2025–2026 (Microsoft/IBM/Dataiku press) | 3 | ⚠ Secondary (report itself paywalled) | Same finding as S-71 |
| S-73 | Solytics Partners Chartis AI Governance Solutions 2026 category-leader press (Yahoo Finance/SAS reference) | 3 | ⚠ Secondary | Bonus finding, §4.5; different report than S-01 |

*(I have not edited `source-ledger.md` — these IDs are proposals for whoever integrates this ticket.)*

---

## 6. Recommendation

**On S-01 (Chartis MRM 2024, Genpact mirror):**
**Upgrade from ⚠ to ✅**, with an updated note along the lines of: *"Full 18-page report read directly via licensed Genpact reprint (Infopro Digital copyright, single-print license — standard analyst-firm reprint distribution, not an unauthorized scrape); vendor list, quadrant placements, and star ratings independently cross-confirmed by four separate wire-service press releases (ValidMind, SAS, CRISIL, Evalueserve) quoting the same named Chartis analyst."* This clears the bar for ✅ under this project's own legend ("primary verified").

**On S-02 (Gartner MQ AI Governance Platforms Jun 2026):**
**Keep as ⚠** (the MQ document itself is still paywalled — that fact hasn't changed), but **strengthen the note**: *"MQ paywalled; all 13 vendor placements (3 Leaders / 5 Visionaries / 1 Challenger / 4 Niche) independently cross-confirmed via 7 direct vendor press releases + 1 independent ex-Gartner-analyst breakdown; zero contradictions across 10 sources checked."* This is meaningfully more confidence than the current bare "⚠ vendor press + secondary summaries" note conveys, even though the access tier is unchanged.

**On the specific claim in `deep-research-v1.md` §2.1 ("ValidMind is the strongest direct MRM competitor... Chartis leader all three quadrants ✅ S-03"):**
**Soften/reword.** Triple-quadrant "Category leader" status is **not unique to ValidMind** — CRISIL Integral IQ and Evalueserve also land in the Category-leaders box in all three 2024 quadrants per the primary report. Recommend replacing the sentence with something like:

> *"Analyst signal: Chartis 2024 MRM (30 vendors ✅ S-62/S-01) confirms market convergence of MRM and AI governance. ValidMind, CRISIL Integral IQ, and Evalueserve are each 'Category leaders' across all three 2024 quadrants (derivatives validation, credit validation, model governance); SAS holds the single top score in the governance quadrant specifically (19 vendors evaluated). ValidMind is the most Workbench-relevant of these because it is the only pure-play, API/SDK-native MRM software vendor among them with modern AI/agentic-governance positioning — CRISIL and Evalueserve compete more as validation/advisory-services firms (comparable in profile to KPMG/PwC in the same quadrants) than as software platforms."*

This keeps the underlying competitive-positioning conclusion (ValidMind is the most relevant direct comparator for an integrated MRM+AI-governance software workbench) but removes the implication that "leader in all 3 quadrants" is a unique differentiator, which the primary source does not support.

**On the general vendor-tiering claim in the §2.2 comparison matrix:**
**Flag, don't retract.** No independent second-analyst-firm corroboration is available or obtainable for the ValidMind/SAS/Solytics/ModelOp tiering as a set, because Forrester, Gartner, and IDC's current AI-governance-platform coverage evaluates a structurally different (Layer B) vendor population than Chartis's MRM coverage (Layer A). Recommend adding a footnote to `deep-research-v1.md` §2.2 stating this explicitly, e.g.: *"Note: Chartis is currently the only analyst firm publishing quadrant-style coverage of traditional bank MRM software as a distinct category; Forrester Wave (AI Governance Solutions, Q3 2025) and IDC MarketScape (Unified AI Governance Platforms, 2025–2026) evaluate an adjacent but largely non-overlapping vendor set and cannot independently confirm or contradict ValidMind/SAS/Solytics's relative positioning."* This is a transparency addition, not a walk-back — nothing found in this spot-check contradicts the existing tiering, and the Chartis-sourced facts now have stronger multi-party corroboration than before this ticket.

---

## 7. Open items for downstream tickets

**All closed / dispositioned in R-14** (`research/findings/R-14-r12-r13-closeout-amendment-proposal.md`):

- **Solytics Chartis AI Governance 2026 Category Leader** — ✅ CLOSED. Incorporate into R-01 / deep-research-v1 competitive narrative (S-83). Confirmed via Access Newswire / Yahoo / solytics.com (Apr 13, 2026).
- **Source ID collision** — ✅ CLOSED. Use R-12 → S-62–S-71; R-13 → S-72–S-83; NMP → S-84 (R-14 §5). Do not apply this ticket’s original overlapping S-62–S-73 proposals as written.
- **Genpact PDF evidence freeze** — ✅ CLOSED → optional build/docs task. Hash into `research/evidence/` if Chartis figures are cited in examiner-facing materials; not blocking research close-out.
