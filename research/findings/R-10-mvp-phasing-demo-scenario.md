# R-10 — MVP Phasing & Concrete Demo Scenario

**Ticket:** R-10  
**Session:** 5  
**Status:** Complete  
**Research date:** 2026-07-20  
**Depends on:** R-01 through R-09 (all complete)

---

## 1. Executive summary

**Recommendation:** Ship the smallest credible end-to-end slice as a **frozen German Credit validation walkthrough** — pre-trained `XGBClassifier` + labeled CSV → full `validation_run` → OCC 2026-13 seven-section report with appendices A–E → hash-chained audit log with `verify-chain` pass. Build in **four implementation phases (P0–P3)**; treat **P4 (Home Credit + BISG)** as README appendix only.

**Demo entry points:**
- **CLI:** `workbench validate run --config configs/german_credit_baseline.yaml`
- **Notebook:** `notebooks/01_german_credit_validation.ipynb` (primary portfolio surface)
- **P3 second run:** `configs/german_credit_ca_overlay.yaml` (recommended) or `configs/german_credit_co_overlay.yaml`

**Resolved open questions (from R-09 §12):**

| Question | R-10 decision |
| -------- | ------------- |
| State overlay for P3 demo | **`CA` primary** — produces `admt_risk_assessment_summary.json` (stronger artifact); **`CO`** documented as simpler checklist alternative |
| Challenger comparison | **Empty stub** — `challenger_model_id: null`; §V.2 subsection renders "Not performed" |
| PDF in demo path | **Markdown default**; PDF via `--format pdf` / `outputs.report_format: [markdown, pdf]` behind `[pdf]` extra |
| Vendor §VII path | **Mock `VendorModelAdapter`** wrapping same XGB model via local HTTP shim — narrative §VII without real vendor contract |

---

## 2. MVP phasing (P0–P3) with exit criteria

Phasing inherits R-09 §8 ordering. Each phase adds modules and report sections; **do not skip P0** before layering P1–P3.

### P0 — Core validation loop

| Element | Specification |
| ------- | ------------- |
| **Slice** | Ingest → intake gate → materiality tier → federal proxy-discrimination `bias_battery` → OCC report §I–VI → hash-chained audit |
| **Modules active** | `bias_battery` only (`adverse_action_translator: false`, `drift_monitor: false`) |
| **Config** | `configs/german_credit_p0.yaml` |
| **CLI** | `workbench validate run --config configs/german_credit_p0.yaml` |
| **Notebook cells** | §0–§4 in `01_german_credit_validation.ipynb` |

**Exit criteria (all must pass):**

- [ ] `german-credit-xgb-v1.2.joblib` loads; `feature_names_in_` excludes `sex`
- [ ] Intake gate **PASS** (statistical credit model; not excluded category)
- [ ] Materiality engine assigns **T3** (`exposure: 0.15`, `purpose: credit_decisioning`)
- [ ] `bias_battery` completes three layers for `sex` under `federal_ecoa: proxy_discrimination`
- [ ] Report `german_credit_validation_report.md` contains populated §I–VI (§V.3 = "Not run — drift module disabled")
- [ ] Appendices **B** (bias summary) and **E** (audit verification stub) present; A/C/D marked N/A
- [ ] `workbench audit verify-chain` → **PASS** (≥3 events: `validation_run.start`, `bias_battery.result`, `validation_run.complete`, `report.generated`)
- [ ] `bias_battery.result` audit payload includes `jurisdiction_frame` block

### P1 — Federal adverse-action hook

| Element | Specification |
| ------- | ------------- |
| **Slice** | P0 + `adverse_action_translator` + translation methodology artifact |
| **Modules** | `bias_battery`, `adverse_action_translator` |
| **Config** | `configs/german_credit_baseline.yaml` (full federal run minus drift) |
| **CLI** | `workbench validate run --config configs/german_credit_baseline.yaml` |

**Exit criteria:**

- [ ] TreeSHAP attribution on ≥1 adverse decision (sample N=50 for fidelity batch)
- [ ] `translation_methodology_v1.json` + `.md` generated; SHA-256 bound in `adverse_action.methodology_published` event
- [ ] Report **§V.1** populated (conceptual soundness + methodology overview)
- [ ] **Appendix A** present and hash-bound; **Appendix D** (`fidelity_validation_report.json`) present
- [ ] `adverse_action.attribution` Tier-2 events in audit chain (≥1)
- [ ] §V.2 references proxy-risk cross-check from bias battery (R-04 §6 integration)

### P2 — Drift monitoring

| Element | Specification |
| ------- | ------------- |
| **Slice** | P1 + `drift_monitor` on injected covariate-shift monitor split |
| **Modules** | All three: `bias_battery`, `adverse_action_translator`, `drift_monitor` |
| **Config** | `configs/german_credit_full.yaml` (canonical demo config — matches handoff YAML) |
| **Monitor data** | `data/german_credit_monitor.csv` (shifted features; see §4.3) |
| **CLI** | `workbench validate run --config configs/german_credit_full.yaml` |

**Exit criteria:**

- [ ] Score PSI and ≥3 feature CSIs computed vs `german_credit_train.csv` reference
- [ ] At least one feature triggers **Amber** (PSI 0.10–0.25) or **Red** (PSI ≥ 0.25) on monitor split
- [ ] T3 escalation narrative in report **§V.3** (weekly cadence; re-validation scoping language per R-05)
- [ ] `drift.event` audit entry with `alert_level`, `materiality_tier: T3`, `recommended_action`
- [ ] **Appendix C** (`drift_report.json`) hash-bound in `report.generated` event
- [ ] Segment-level PSI on `sex` documented in §V.3 (fair-lending subgroup stability bridge)

### P3 — State overlay differentiation demo

| Element | Specification |
| ------- | ------------- |
| **Slice** | Identical to P2 except `regulatory_frame.state_overlay: CA` (or `CO`) |
| **Config** | `configs/german_credit_ca_overlay.yaml` |
| **CLI** | `workbench validate run --config configs/german_credit_ca_overlay.yaml --output-dir artifacts/run_ca_overlay/` |
| **Notebook** | Final cell: side-by-side §II diff vs baseline run |

**Exit criteria:**

- [ ] Report **§II** shows **two regulatory frames** when compared to baseline (federal-only vs federal + CA ADMT)
- [ ] CA: `admt_risk_assessment_summary.json` artifact emitted (R-08 §3.6)
- [ ] CO (if used instead): post-adverse notice checklist + 3-year retention flag in §II; no new JSON export
- [ ] `bias_battery.result` audit payload adds `state_overlay`, `state_authority`, overlay-specific artifact refs
- [ ] Layer A labeled **"outcomes analysis / risk-assessment evidence"** — not "ECOA disparate-impact compliance"
- [ ] README documents limitation: German/non-US data; overlay is **jurisdictional frame demonstration** only

### P4 — Scale story (optional appendix only)

| Element | Specification |
| ------- | ------------- |
| **Slice** | Home Credit 10k subset + surgeo BISG proxy pipeline |
| **Deliverable** | `notebooks/02_home_credit_bias_proxy.ipynb` + README section; **not** blocking P0–P3 |
| **Exit criterion** | Documented architecture only; no CI gate |

---

## 3. Canonical demo configuration

Baseline full run (P2/P3 base) — binds Sessions 1–4 decisions:

```yaml
# configs/german_credit_full.yaml
validation_run:
  run_id: german-credit-demo-v1
  model: models/german-credit-xgb-v1.2.joblib
  dataset: data/german_credit_validation.csv
  reference_dataset: data/german_credit_train.csv      # drift reference population
  monitor_dataset: data/german_credit_monitor.csv      # injected covariate shift
  decision_column: approval_binary
  label_column: credit_risk                            # ground truth for performance metrics
  protected_attributes:
    - name: sex
      source: direct
      reference_group: male
  regulatory_frame:
    federal_ecoa: proxy_discrimination
    fha_overlay: false
    state_overlay: none                                # P3: CA or CO
  materiality:
    exposure: 0.15
    exposure_unit: portfolio_pct
    purpose: credit_decisioning
  modules:
    bias_battery: true
    adverse_action_translator: true
    drift_monitor: true
  audit:
    finos_tier: 2
    actor: validator@example.com
  outputs:
    report_format: [markdown]                          # add pdf when [pdf] extra installed
    artifact_dir: ./artifacts/{run_id}/
```

**P3 overlay delta** — change only `regulatory_frame` and `run_id`:

```yaml
regulatory_frame:
  federal_ecoa: proxy_discrimination
  fha_overlay: false
  state_overlay: CA                                    # or CO
run_id: german-credit-demo-ca-overlay
```

---

## 4. German Credit frozen fixture spec

### 4.1 Source and scope

| Attribute | Value | Source |
| --------- | ----- | ------ |
| **Dataset** | UCI Statlog German Credit | ✅ S-24 |
| **Rows (raw)** | 1,000 | UCI canonical |
| **Model** | `XGBClassifier` (sklearn API) | Trained on train split only |
| **Artifact** | `models/german-credit-xgb-v1.2.joblib` | Frozen at fixture commit |
| **Materiality** | T3 — `exposure: 0.15`, `credit_decisioning` | R-05/R-06 tier table |

### 4.2 File manifest (frozen at fixture freeze commit)

Compute SHA-256 at freeze; pin in `manifests/german_credit_fixture_manifest.yaml`:

```yaml
fixture_version: "2026-07-20"
seed: 42
files:
  - path: data/raw/german_credit_uci.csv
    role: source_of_truth
    rows: 1000
    sha256: "<compute-at-freeze>"
  - path: data/german_credit_train.csv
    role: drift_reference_population
    rows: 700
    sha256: "<compute-at-freeze>"
  - path: data/german_credit_validation.csv
    role: validation_run_primary
    rows: 300
    sha256: "<compute-at-freeze>"
  - path: data/german_credit_monitor.csv
    role: drift_monitor_injected_shift
    rows: 300
    sha256: "<compute-at-freeze>"
  - path: models/german-credit-xgb-v1.2.joblib
    role: pre_trained_model
    sha256: "<compute-at-freeze>"
  - path: configs/feature_mapping_german_credit.yaml
    role: adverse_action_feature_dictionary
    sha256: "<compute-at-freeze>"
derivation_rules_version: "1.0"
```

**Freeze protocol:** Run `scripts/freeze_german_credit_fixtures.py` once; commit manifest hashes; CI verifies hashes before demo notebook execution.

### 4.3 Column derivation rules

#### `sex` (validation-only — never a model feature)

Derived from UCI `personal_status` (Statlog encoding):

| `personal_status` | Derived `sex` |
| ----------------- | ------------- |
| A91 (male : divorced/separated) | `male` |
| A92 (female : divorced/separated/married) | `female` |
| A93 (male : single) | `male` |
| A94 (male : married/widowed) | `male` |
| A95 (female : single) | `female` |

```python
FEMALE_CODES = {"A92", "A95"}
MALE_CODES = {"A91", "A93", "A94"}

def derive_sex(personal_status: str) -> str:
    if personal_status in FEMALE_CODES:
        return "female"
    if personal_status in MALE_CODES:
        return "male"
    raise ValueError(f"Unknown personal_status: {personal_status}")
```

**Ingest hard gate:** `sex` ∈ dataset columns for validation; `sex` ∉ `model.feature_names_in_`.

#### `credit_risk` (ground truth label)

| UCI `class` | `credit_risk` |
| ----------- | ------------- |
| 1 (good) | 1 |
| 2 (bad) | 0 |

#### `approval_binary` (model decision column)

Binary model prediction at threshold 0.5 on validation/monitor rows:

```python
approval_binary = (model.predict_proba(X)[:, 1] >= 0.5).astype(int)
```

Stored in dataset for reproducibility; bias battery uses **model decisions**, not ground-truth labels, for Layer A selection-rate analysis.

#### Feature encoding

- Categorical UCI attributes → one-hot or ordinal encoding per `configs/feature_mapping_german_credit.yaml`
- **Excluded from model features:** `sex`, `personal_status`, `class`, `credit_risk`, `approval_binary`
- Model inputs: 20 encoded features (typical German Credit XGB pipeline)

### 4.4 Train / validation / monitor splits

| Split | Rows | Method | Purpose |
| ----- | ---- | ------ | ------- |
| **train** | 700 | `train_test_split(test_size=0.30, stratify=credit_risk, random_state=42)` on raw 1k | Model training + drift **reference** population |
| **validation** | 300 | Holdout from above split | Primary `validation_run` dataset |
| **monitor** | 300 | Copy of validation rows + **injected covariate shift** | Drift demo (not temporal) |

**No temporal split** — German Credit has no application date. Drift is **pedagogical covariate shift**, documented as limitation in §II.

### 4.5 Injected covariate shift (monitor split)

Target: trigger **Amber or Red** score PSI at T3 escalation depth (R-05 §6).

| Feature | Shift applied to monitor split | Expected PSI band |
| ------- | ------------------------------ | ----------------- |
| `duration` | Multiply by 1.35 + Gaussian noise σ=2 | 0.15–0.30 (Amber–Red) |
| `credit_amount` | Add +2,000 EUR offset to 40% of rows | 0.10–0.20 (Amber) |
| `installment_commitment` | Resample from train distribution with mean +15% | 0.10–0.18 (Amber) |

**Implementation:** `scripts/inject_monitor_shift.py` with fixed seed; output `german_credit_monitor.csv`. Document shift parameters in Appendix C metadata.

---

## 5. Notebook and CLI entry points

### 5.1 `notebooks/01_german_credit_validation.ipynb` structure

| Section | Content | Phase |
| ------- | ------- | ----- |
| §0 Setup | `%pip install -e ".[notebooks]"`; import SDK | — |
| §1 Fixtures | Load manifest; verify SHA-256 | P0 |
| §2 Register model | Inventory entry; intake gate; tier assignment | P0 |
| §3 Baseline run | `ValidationRun.from_config("configs/german_credit_full.yaml")` | P2 |
| §4 Report walkthrough | Render §I–VII; open appendices A–E | P2 |
| §5 Audit chain | `workbench audit verify-chain` | P2 |
| §6 CA overlay run | Second run; diff §II side-by-side | P3 |
| §7 Vendor narrative (optional) | Mock `VendorModelAdapter` §VII cell | P1+ |
| §8 Limitations | German/non-US; no BISG; injected drift | — |

### 5.2 CLI command reference

```bash
# P0 smoke
workbench validate run --config configs/german_credit_p0.yaml

# Full demo (P2)
workbench validate run --config configs/german_credit_full.yaml

# P3 state overlay
workbench validate run --config configs/german_credit_ca_overlay.yaml \
  --output-dir artifacts/run_ca_overlay/

# Audit verification (required pass)
workbench audit verify-chain --db workbench.db

# Optional PDF
workbench validate run --config configs/german_credit_full.yaml --format markdown pdf
```

---

## 6. Per-run artifact checklist

### 6.1 Required artifacts (P2 full run)

| Artifact | Path pattern | Phase | Bound to audit |
| -------- | ------------ | ----- | -------------- |
| OCC validation report (MD) | `artifacts/{run_id}/german_credit_validation_report.md` | P0+ | `report.generated` |
| OCC validation report (PDF) | `artifacts/{run_id}/german_credit_validation_report.pdf` | P1+ optional | same |
| Report JSON (machine-readable) | `artifacts/{run_id}/report.json` | P0+ | `report.generated` |
| **Appendix A** — translation methodology | `translation_methodology_v1.json`, `.md` | P1+ | `adverse_action.methodology_published` |
| **Appendix B** — bias battery tables | `bias_battery_summary.json` | P0+ | `bias_battery.result` |
| **Appendix C** — drift snapshot | `drift_report.json` | P2+ | `drift.event` |
| **Appendix D** — fidelity validation | `fidelity_validation_report.json` | P1+ | `adverse_action.attribution` |
| **Appendix E** — audit chain summary | `audit_chain_verification.json` | P0+ | `report.generated` |
| CA overlay export (P3 only) | `admt_risk_assessment_summary.json` | P3 CA | `bias_battery.result` |
| SQLite audit DB | `workbench.db` (append-only) | P0+ | — |

### 6.2 Audit `verify-chain` pass criteria

| Check | Pass condition |
| ----- | -------------- |
| Chain integrity | All `chain_hash` values recompute correctly from genesis |
| Event completeness (P2) | ≥7 event types present for full run |
| Hash binding | `report.generated.artifact_refs` SHA-256 match on-disk files |
| FINOS tier | Events at configured `finos_tier: 2` include reasoning payloads |
| No gaps | `seq_id` monotonic; no missing `prev_hash` links |
| CLI exit code | `workbench audit verify-chain` exits **0** |

**Minimum event sequence (P2 full run):**

1. `validation_run.start`
2. `bias_battery.result`
3. `adverse_action.methodology_published`
4. `adverse_action.attribution` (≥1)
5. `drift.event`
6. `validation_run.complete`
7. `report.generated`

---

## 7. OCC 2026-13 section mapping (German Credit scenario)

### 7.1 Sections I–VII — content and pass/fail

| Section | Title | Populated from | Pass criterion | Fail / N/A |
| ------- | ----- | -------------- | -------------- | ---------- |
| **I** | Introduction | Run metadata, model summary, validator, `guidance_version: OCC-2026-13`, **disclaimer** (R-09 §6) | Model ID, date, scope, disclaimer present | Missing disclaimer |
| **II** | Purpose and Scope | `intended_use`, T3 tier rationale (`exposure 15%` × `credit_decisioning`), **regulatory frames table**, **limitations** (German data, no race/BISG, injected drift) | Tier math shown; limitations explicit; P3 adds overlay row | Claims compliance |
| **III** | Overview of Model Risk and MRM | Inherent risk narrative, exposure context, known model limitations | T3 oversight depth stated | Empty risk discussion |
| **IV** | Model Development and Model Use | Feature inventory (excl. `sex`), training split summary, XGBoost methodology, data lineage to UCI | `sex` excluded from features documented | Protected attr in features |
| **V** | Model Validation and Monitoring | Three components (§V.1–V.3) | All three subsections populated at P2 | §V.3 empty at P2 |
| **VI** | Governance and Controls | Inventory entry, audit summary, FINOS mi-21 Tier 1–2 statement, approval stub | Audit event count + verify-chain status | No audit reference |
| **VII** | Vendor and Third-Party Products | **N/A default** (`vendor_flag: false`) OR mock adapter narrative | §VII states "Not applicable" OR mock vendor assessment complete | Silent omission |

### 7.2 Three validation components (§V.1–V.3)

| Subsection | OCC component | German Credit content |
| ---------- | ------------- | --------------------- |
| **§V.1** | Conceptual Soundness | Intake gate PASS; credit risk theory basis; feature definitions; TreeSHAP global summary; translation methodology overview (P1+) |
| **§V.2** | Outcomes Analysis | Layer A: sex AIR, selection-rate gap, SMD on score; Layer B: FPR/FNR parity; Layer C: proxy correlation + auxiliary classifier AUC; regulatory frame statement (`proxy_discrimination`); challenger stub: "Not performed" |
| **§V.3** | Ongoing Model Monitoring | PSI/KS on monitor split; Amber/Red alert; T3 escalation (validator notification ≤10 days, re-validation scoping); segment PSI by `sex`; cadence: weekly |

### 7.3 Report §I disclaimer (embedded template)

> This validation report is generated by an analytical workbench for model risk and fair-lending **review support**. It does not constitute legal advice, a regulatory filing, or a determination of compliance with any applicable law.

### 7.4 Report §II limitations block (required)

> **Demo limitations:** This validation uses the UCI German Credit dataset (German domestic credit, circa 1990s). It does not represent US lending populations. No race/ethnicity fields are available; BISG proxy analysis is **not performed**. Population drift is **injected covariate shift** for pedagogical demonstration, not observed production drift. State overlay toggles (P3) illustrate jurisdictional framing only.

---

## 8. P3 second run — what changes (CA vs CO)

Same model, same `german_credit_validation.csv`, same metrics — **only `regulatory_frame` and report/audit framing change**.

### 8.1 Report §II delta

| Field | Baseline (`state_overlay: none`) | CA overlay | CO overlay |
| ----- | -------------------------------- | ---------- | ---------- |
| Active authorities | Federal ECOA (proxy); OCC 2026-13 | + California CCPA/CPRA ADMT (CPPA) | + Colorado SB 26-189 |
| Significant decision | Credit decisioning (federal) | Financial/lending services (ADMT) | Consequential decision — financial/lending |
| Statistical battery label | Proxy-discrimination primary; AIR as outcomes support | Layer A/B/C as **risk-assessment evidence** for discrimination harms | Layer A optional monitor; **no statutory DIA** |
| New §II subsections | — | ADMT risk assessment cross-reference; pre-use notice **checklist stub** (document-only) | Post-adverse notice 30-day checklist; human-review-on-request stub; 3-year retention flag |
| Non-claims | Standard disclaimer | "Does not constitute CPPA certification" | "Does not satisfy CO AG rules (pending Jan 2027)" |

### 8.2 Audit payload delta (`bias_battery.result`)

```json
{
  "jurisdiction_frame": {
    "federal_ecoa": "proxy_discrimination",
    "fha_overlay": false,
    "state_overlay": "CA",
    "state_authority": "California CCPA/CPRA ADMT (CPPA, Cal. Code Regs tit. 11)"
  },
  "overlay_artifacts": [
    {"name": "admt_risk_assessment_summary.json", "sha256": "..."}
  ],
  "layer_a_label": "outcomes_analysis_risk_assessment_evidence"
}
```

CO overlay replaces `overlay_artifacts` with checklist refs only (`co_disclosure_checklist.json`); no ADMT export.

### 8.3 Recommended P3 demo narrative

Run **CA overlay** in notebook §6 — produces tangible JSON export for portfolio reviewers. Document **CO** as one-YAML-line alternative in README for disclosure-focused audiences.

---

## 9. Explicit demo non-goals

| Non-goal | Rationale |
| -------- | --------- |
| **Consumer-facing notices** (CO point-of-interaction, CA pre-use notice text) | Validation workbench, not compliance ops (R-09 §2.2) |
| **NY insurance CL 7 full DIA** | Wrong product line for German Credit bank-lending persona (R-08 §4.1) |
| **Algorithmic debiasing / Fairlearn reductions** | Detection-only; legal risk under post–July 2026 framing (R-03 §3.3) |
| **BISG / race proxy on German Credit** | No US geography or surname fields; defer to P4 Home Credit |
| **FHA / HMDA overlay** | Optional Phase 3+; not in core demo path |
| **Real temporal drift** | Dataset lacks application dates |
| **Production vendor API integration** | Mock adapter only for §VII narrative |
| **Challenger model comparison** | Empty stub v1 |
| **EU AI Act conformity assessment** | Crosswalk rows only (R-09 §2.1) |
| **Gen-AI / TrajectoryNormalizer demo** | Protocol stub / ADR only |
| **Tier 3 crypto-signed audit segments** | Schema slots; design doc only (R-06 §3.2) |

---

## 10. Open build decisions (resolved + remaining)

### 10.1 Resolved in R-10

| Decision | Resolution |
| -------- | ---------- |
| Challenger stub | `challenger_model_id: null`; §V.2 renders "Champion-Challenger Outcomes: Not performed" |
| PDF in demo | Markdown default; PDF via `--format pdf` when WeasyPrint installed |
| Vendor §VII | `notebooks/01` §7 + `configs/german_credit_vendor_narrative.yaml` — `VendorModelAdapter` POSTs to `localhost:8765/mock-score` wrapping same joblib |
| P3 state overlay | **CA primary**; CO alternative documented |
| Drift method | Injected covariate shift on monitor split (not temporal) |

### 10.2 Remaining for build phase

| # | Question | Recommendation |
| - | -------- | -------------- |
| 1 | Exact XGB hyperparameters for v1.2 joblib | Document in `configs/model_training_german_credit.yaml`; freeze after first training run |
| 2 | Sample-size-adjusted PSI in v1? | Defer v1.1; document Lewis limitations in Appendix C (R-05 open Q1) |
| 3 | CO AG rules (Jan 2027) | Monitor; update checklist template pre-production |
| 4 | Fidelity human-review sign-off UX | Tier-2 slot in audit; manual notebook acknowledgment for demo |
| 5 | CI gate: which phase minimum? | **P2 full run** + `verify-chain` in CI; P3 overlay in optional job |

---

## 11. Mock VendorModelAdapter (§VII demo path)

For portfolio narrative without enterprise vendor contract:

```yaml
# configs/german_credit_vendor_narrative.yaml
validation_run:
  <<: *german_credit_full          # anchor to full config
  model:
    type: vendor_api
    adapter: VendorModelAdapter
    endpoint: http://localhost:8765/mock-score
    vendor_name: "Demo Credit Score API"
    vendor_flag: true
  report:
    section_vii: required
```

**Mock server:** `scripts/mock_vendor_server.py` loads same `german-credit-xgb-v1.2.joblib`; returns JSON scores. §VII populates vendor assessment template (conceptual soundness evidence available without source code, score-distribution monitoring plan).

---

## 12. Implications for Workbench

1. **Implement P0→P2 sequentially** — each phase has independent exit criteria; do not merge into a single "big bang" PR without phase gates.
2. **Freeze fixtures early** — manifest SHA-256 pins are CI prerequisites; notebook must not silently retrain model.
3. **`sex` derivation is part of the fixture contract** — document in manifest; never expose to model features.
4. **§II limitations block is mandatory** — German data, no BISG, injected drift; prevents over-claiming.
5. **P3 CA overlay is the differentiation capstone** — side-by-side §II diff in notebook §6 is the portfolio climax.
6. **Audit chain is a demo deliverable** — `verify-chain` PASS screenshot/badge in README.
7. **Challenger and vendor paths are narrative slots** — implement stubs without blocking P0–P2.
8. **Defer P4 to README** — Home Credit + surgeo is scale story, not MVP gate.

---

## 13. Sources

| ID | Source | Used in |
| -- | ------ | ------- |
| S-24 | UCI German Credit dataset | Fixture spec, sex derivation |
| S-03 | ValidMind notebook pattern | Entry point design |
| S-38 | OCC Bulletin 2026-13 | Section mapping I–VII |
| S-45 | FINOS AIR-DET-021 mi-21 | Audit verify-chain criteria |
| S-52–S-54 | R-08 state overlays | P3 §II and audit delta |
| R-03–R-09 | Prior finding files | Phasing, modules, configs (bound; not re-researched) |

No new primary sources required for R-10; fixture freeze will add computed hashes as internal artifacts.

---

## 14. Open questions (handoff to build / R-11)

1. **Hyperparameter lock:** Publish exact XGB params when `german-credit-xgb-v1.2.joblib` is first trained.
2. **CA ADMT template:** Validate `admt_risk_assessment_summary.json` field list against CPPA §7152 after first CPPA enforcement action.
3. **Notebook vs CLI as CI canonical path:** Recommend CLI for CI; notebook for portfolio human review.
4. **A773B / AB 1018 enactment:** If passed before build complete, add overlay profiles in v1.1 (R-08 watchlist).
