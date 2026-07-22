# R-09 — Scope Boundaries & Differentiation Synthesis

**Ticket:** R-09  
**Session:** 4  
**Status:** Complete  
**Research date:** 2026-07-20  
**Depends on:** R-01 (gaps), R-03 (bias module), R-08 (state overlays), R-06 (architecture bindings)

---

## 1. Executive summary

**v1 scope recommendation:** Ship an **open, model-agnostic validation workbench** for **traditional ML credit models** that produces **auditor-facing evidence** across seven integrated capabilities — not an enterprise GRC platform, not a lending system, and not a gen-AI MRM product.

**Primary differentiators (build first):**
1. Integrated **proxy-discrimination battery** + jurisdiction overlays (federal post–Reg B, FHA, CO/CA/NY) — FINOS ri-16 gap
2. **OCC 2026-13 literal seven-section** validation report with hash-bound appendices
3. **CFPB Circular 2026-03 translation methodology artifact** (adverse-action pipeline)

**Secondary differentiators (build in v1, demo selectively):**
4. FINOS **mi-21 Tier 1–2** hash-chained audit log cited by control ID
5. Materiality-tiered drift escalation (R-05)
6. Vendor/black-box ingest path (Section VII)

**Explicitly out of scope for v1:** Enterprise GRC breadth, SaaS multi-tenancy, gen-AI/agentic MRM regulatory completeness, FCRA "key factors" engine, algorithmic debiasing mitigations, full Tier 3 crypto audit trail, NY bank-lending statutory overlay (pending A773B).

---

## 2. v1 scope boundary

### 2.1 In scope (build)

| Capability | Source tickets | Demo? | Document-only? |
| ---------- | -------------- | ----- | -------------- |
| Model-agnostic ingest (sklearn + VendorModelAdapter) | R-06, R-07 | ✅ German Credit | — |
| OCC model-definition intake gate | R-06 | ✅ | — |
| Materiality tiering (exposure × purpose) | R-06, R-05 | ✅ | — |
| Three-layer bias battery + jurisdiction toggles | R-03, R-08 | ✅ sex (German Credit); BISG in Phase 2 | FHA/HMDA optional |
| State overlays CO / CA / NY | R-08 | ⚠ Toggle demo on one run | NY insurance scope note |
| SHAP → adverse-action translator + methodology artifact | R-04 | ✅ | — |
| PSI/KS drift + tier-gated escalation | R-05 | ✅ snapshot | — |
| Hash-chained audit log (FINOS mi-21 Tier 1–2) | R-06 | ✅ verify-chain CLI | Tier 3 design doc |
| OCC seven-section report (Markdown + optional PDF) | R-06, R-07 | ✅ full report | — |
| CLI + Python SDK | R-07 | ✅ | FastAPI thin optional |
| EU AI Act / NIST documentation layer | R-03, R-06 | ⚠ Report crosswalk rows | No separate EU metric set |
| TrajectoryNormalizer protocol stub (choice B) | R-06 | ❌ | ✅ ADR only |

### 2.2 Explicitly out of scope (do not build in v1)

| Item | Rationale |
| ---- | --------- |
| **Gen-AI / agentic MRM regulatory completeness** | OCC 2026-13 explicitly excludes; no US RFI yet (foundation §3.1) |
| **Enterprise GRC** (policy packs, 25-framework checklists, agent registry) | Commodity — Credo, ServiceNow, IBM (R-01) |
| **SaaS multi-tenant product** | Portfolio/demo scale; self-hosted local + Docker (R-07) |
| **Credit decisioning / loan origination** | User persona is risk/compliance/auditor, not lender |
| **FCRA "key factors" adverse-action engine** | Reg B §1002.9 is in scope; FCRA parallel is separate statute |
| **Algorithmic debiasing / fairness constraints** | Legal risk under post–July 2026 proxy-discrimination framing (R-03) |
| **Consumer-facing disclosure generation** (CO point-of-interaction, CA pre-use notice) | Validation workbench, not compliance ops portal — checklist stubs only |
| **Full FINOS Tier 3 crypto trail** | Schema slots only; Monitaur pattern documented (R-06) |
| **model-ledger bidirectional sync** | v2 export hook |
| **ONNX / PMML ingest** | v1.1 unless demo requires |
| **Real-time streaming drift (Kafka)** | Batch v1 (R-05, R-06) |
| **Challenger-model comparison logic** | Slot only; R-10 |
| **50-state overlay expansion** | CO, CA, NY only (R-08) |

### 2.3 Extensible but not demoed in v1

| Item | Phase |
| ---- | ----- |
| Home Credit 10k + BISG proxy pipeline | R-10 Phase 2 |
| HMDA FHA overlay toggle | R-10 Phase 3 optional |
| NY DFS CL 7 insurance underwriting dataset | R-10 or document-only |
| MCP server | v2 |
| Postgres production deployment | v2 |

---

## 3. Differentiator ranking

### 3.1 Primary (market gap — build and lead messaging)

| Rank | Differentiator | Evidence | Workbench module |
| ---- | -------------- | -------- | ---------------- |
| **1** | **Post–July 2026 proxy-discrimination test suite** + jurisdiction overlays | R-01 gap #4; R-02 verified; no competitor ships FINOS ri-16 statistical control | `bias_battery` |
| **2** | **OCC 2026-13 seven-section report** (literal I–VII) | R-01 gap #2; vendors still on three-pillar / SR 11-7 framing | `report_generator` |
| **3** | **Circular 2026-03 translation methodology artifact** | R-01 gap #3; R-04 pipeline; Holistic/Fiddler have attribution not Reg B translator | `adverse_action_translator` |

### 3.2 Secondary (strengthen portfolio; demo selectively)

| Rank | Differentiator | Evidence | Workbench module |
| ---- | -------------- | -------- | ---------------- |
| **4** | FINOS **mi-21** tiered audit trail by control ID | R-01 gap #5; Monitaur closest but no FINOS citation | `audit_log` |
| **5** | Open statistical bias module filling FINOS catalogue gap | Foundation §3.5; R-01 gap #6 | `bias_battery` |
| **6** | Materiality-tiered drift → re-validation escalation | R-05; Solytics narrates SR 26-2; no open reference | `drift_monitor` + `materiality_engine` |
| **7** | Model-agnostic validation without enterprise lock-in | R-01 gap #1 | ingest + orchestrator |
| **8** | State overlay toggles (CO/CA/NY) | R-08; tertiary but concrete config | `bias_battery` + report §II |

### 3.3 Commodity (compose, do not rebuild)

Fairlearn/Aequitas metrics, SHAP, PSI dashboards, model inventory tables, generic EU AI Act checklists, approval workflow UI, LLM guardrails — per R-01 §6.

---

## 4. Cross-framework control map (extends foundation §3.6)

Architecture bindings from R-06 added in **Workbench module** column.

| Workbench feature | OCC 2026-13 | ECOA/Reg B | EU AI Act | NIST AI RMF | FINOS AIR | **Module / artifact** |
| ----------------- | ----------- | ---------- | --------- | ----------- | --------- | --------------------- |
| Model inventory + materiality tiering | §VI | — | Art. 9 | GOVERN 1.6 | — | `model_inventory` SQLite; `materiality_engine` |
| Intake gate (model definition) | §IV | — | Art. 11 | MAP 5.1 | mi-5 | `intake_gate` → `validation_run.start` audit event |
| Validation report (3 components) | §V (CS / OA / OMM) | — | Art. 11, 15 | MEASURE 2.9 | mi-5 | `report_generator` sections V.1–V.3 |
| Statistical bias / fair-lending | §V outcomes | Proxy disc. (fed); FHA/state DIA | Art. 10 | MEASURE 2.11 | **gap → mi-5 evidence** | `bias_battery` → `bias_battery.result` |
| State overlay (CO/CA/NY) | §V (outcomes context) | Overlays R-08 | Art. 10 (deployer) | MEASURE 2.11 | ri-22 | `regulatory_frame.state_overlay` in run YAML |
| Adverse-action translator | — (adjacent) | §1002.9; Circ. 2026-03 | Art. 13 | MEASURE 2.9 | — | `adverse_action_translator` → `adverse_action.*` events |
| Translation methodology artifact | §V.1 / Appx A | Circ. 2026-03 | — | — | mi-21 | `translation_methodology_v{N}.json` |
| Drift monitoring + escalation | §V.3 | — | Art. 72 | MANAGE 4.1 | mi-4 | `drift_monitor` → `drift.event` |
| Tamper-evident audit log | §VI (documentation) | — | Art. 12 | GOVERN 4.2 | **mi-21 Tier 1–2** | `audit_log` hash chain |
| Human override / governance | §VI | — | Art. 14 | GOVERN 3.2, mi-11 | mi-11 | `governance.approval` event |
| Vendor / third-party model | **§VII** | — | Art. 26(5) | MAP 4.1 | — | `VendorModelAdapter` + §VII template |
| Protected-class hard reject | §V | Reg B design | Art. 10 | MEASURE 2.11 | mi-5 | ingest schema validation |

---

## 5. Demo vs. document-only (portfolio strategy)

| Artifact | End-to-end demo (R-10) | Document-only |
| -------- | ---------------------- | --------------- |
| German Credit full validation run | ✅ Primary | — |
| OCC seven-section Markdown report | ✅ | — |
| Proxy-discrimination + sex AIR | ✅ | — |
| SHAP → adverse-action reasons + methodology JSON | ✅ | — |
| Audit chain verification | ✅ | — |
| Drift snapshot + T3 escalation narrative | ✅ | — |
| `state_overlay: none` (federal default) | ✅ Default run | — |
| `state_overlay: CO` checklist artifacts | ⚠ One toggled run | Retention/notice legal text |
| `state_overlay: CA` risk-assessment export | ⚠ One toggled run | Pre-use notice consumer copy |
| `state_overlay: NY` CL 7 full DIA | ❌ or synthetic insurance slice | ✅ Scope note in README |
| FHA/HMDA overlay | Optional Phase 3 | ✅ Methodology in report appendix |
| BISG / Home Credit scale | Phase 2 | Pipeline architecture in docs |
| Tier 3 crypto audit | — | ✅ Design appendix |
| Gen-AI / TrajectoryNormalizer | — | ✅ Protocol + ADR |
| EU FRIA / conformity assessment | — | ✅ Control map rows |

---

## 6. Messaging discipline — compliance claims

**Do claim:**
- "Produces **validation evidence** structured for OCC 2026-13 seven-section independent review"
- "**Proxy-discrimination statistical battery** aligned with post–July 2026 federal ECOA framing"
- "**Documented translation methodology** for adverse-action factor mapping (Circular 2026-03 pattern)"
- "Audit trail implements **FINOS AIR-DET-021 Tier 1–2** controls by ID"
- "Jurisdiction overlays for **FHA, Colorado, California ADMT, and NY DFS insurance** testing frames"

**Do not claim:**
- "Ensures ECOA disparate-impact compliance" (federal theory removed R-02)
- "California DFPI certified" (wrong regulator; use CPPA/CCPA ADMT)
- "NY DFS lending compliance" (CL 7 is insurance; lending bill pending)
- "OCC 2026-13 compliant" (guidance is non-enforceable; no safe harbor)
- "EU AI Act conformity assessment complete" (deadline Dec 2027; deployer subset only)
- "Gen-AI / agentic MRM compliant" (explicitly out of OCC scope)
- "Replaces enterprise MRM platform" (ValidMind/SAS territory)

**Report disclaimer (template for §I):**
> This validation report is generated by an analytical workbench for model risk and fair-lending **review support**. It does not constitute legal advice, a regulatory filing, or a determination of compliance with any applicable law.

---

## 7. Build this, not that (R-10 input)

| Build this (v1) | Not that (defer / never) |
| --------------- | ------------------------ |
| `workbench validate run` → full battery → report → audit | Multi-tenant SaaS dashboard |
| Seven Jinja2 OCC section templates | Generic "AI governance" PDF export |
| `bias_battery` with `regulatory_frame` toggles | Standalone Fairlearn notebook only |
| `translation_methodology_v1.json` versioned artifact | LIME-only explanations |
| SQLite hash-chained `audit_log` | Elasticsearch log without chain |
| German Credit XGBoost joblib demo | Production Postgres + K8s |
| VendorModelAdapter for §VII narrative | Vendor source-code ingestion |
| Materiality engine at ingest | Hard-coded annual validation cron |
| State overlay config (CO/CA/NY) | 50-state rule engine |
| Markdown + optional WeasyPrint PDF | DOCX examiner pack |
| CLI + Python SDK | Full REST API product |
| Compose Fairlearn + Aequitas + SHAP | Fork Aequitas dashboards |
| Drift PSI/KS module | evidently SaaS dependency |
| FINOS control ID citations in audit events | Generic "audit trail" marketing |
| TrajectoryNormalizer protocol stub | AgentRx full implementation |
| Detection-only bias flags | Fairlearn reductions / debiasing |

---

## 8. Build-priority recommendation for R-10

**MVP phasing order** (smallest path to credible end-to-end demo):

| Phase | Slice | Tickets | Exit criterion |
| ----- | ----- | ------- | -------------- |
| **P0 — Core loop** | Ingest → tier → bias (federal) → report §I–VI → audit | R-06, R-03, R-07 | One `validation_run` produces Markdown report + `audit verify-chain` pass |
| **P1 — Federal hook** | Adverse-action translator + methodology artifact | R-04 | Appendix A bound to audit; §V.1 populated |
| **P2 — Monitoring** | Drift snapshot + tier escalation event | R-05 | §V.3 + `drift.event` in chain |
| **P3 — Differentiation demo** | State overlay toggle (`CA` or `CO`) on second run | R-08 | §II shows two regulatory frames side-by-side |
| **P4 — Scale story** | Home Credit subset + BISG (optional) | R-03, R-07 | Documented in README; not blocking P0 |

**R-10 should use German Credit** as the P0–P2 dataset; defer NY insurance CL 7 full DIA to a supplementary notebook or documented scenario unless synthetic insurance data is trivial to add.

---

## 9. Synthesis inputs — bound conclusions

| # | Input (from prior tickets) | v1 disposition |
| - | -------------------------- | -------------- |
| 1 | Model-agnostic ingest → full validation battery | ✅ P0 — sklearn + CSV |
| 2 | OCC seven-section report literal I–VII | ✅ P0 — primary report structure |
| 3 | Circular 2026-03 translation methodology artifact | ✅ P1 — Appendix A |
| 4 | Post–July 2026 proxy-discrimination suite | ✅ P0 — default federal frame |
| 5 | FINOS mi-21 tiered audit cited by control ID | ✅ P0 — Tier 1–2 implement |
| 6 | Open statistical bias module (FINOS gap) | ✅ P0 — `bias_battery` |
| 7 | State overlay toggles (R-08) | ✅ P3 — one demo toggle |

---

## 10. Implications for Workbench

1. **Lock v1 scope** per §2 — resist GRC feature creep from competitive anxiety (R-01).
2. **Lead portfolio narrative** on differentiators #1–3 (proxy battery + OCC seven sections + translation methodology).
3. **Implement `regulatory_frame` in run YAML** exactly as R-03/R-08 specify; surface in report §II and every `bias_battery.result` audit event.
4. **Ship disclaimer template** in report §I; never auto-generate consumer legal notices.
5. **R-10 MVP** follows §8 phasing P0→P2 minimum; P3 state toggle strongly recommended for differentiation story.
6. **EU/NIST** remain documentation crosswalk rows — no separate build track for v1.

---

## 11. Sources

| ID | Source | Used in |
| -- | ------ | ------- |
| S-01–S-14 | R-01 competitive landscape | Gap synthesis, commodity list |
| S-15–S-18 | R-02 Reg B verification | Federal framing |
| S-19–S-30 | R-03 bias methodology | Battery design |
| S-31–S-37 | R-04 adverse action | Differentiator #3 |
| S-38–S-44 | R-05 drift | Differentiator #6 |
| S-45–S-49 | R-06 architecture | Control map bindings |
| S-50–S-51 | R-07 stack | Scope constraints |
| S-52–S-61 | R-08 state law | Overlay scope, NY/CA corrections |

---

## 12. Open questions (for R-10)

1. Which single state overlay to demo live — `CA` (risk-assessment export) vs `CO` (simpler checklist) vs document-only `NY`?
2. Challenger comparison: empty stub vs minimal AUC delta for German Credit?
3. PDF export in demo path or Markdown-only for portfolio GitHub?
4. Vendor path: mock API demo or narrative-only §VII?
