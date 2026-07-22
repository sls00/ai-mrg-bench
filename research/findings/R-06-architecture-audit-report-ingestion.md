# R-06 — Architecture: Ingestion, Audit Log, Report Structure

**Ticket:** R-06  
**Session:** 3  
**Status:** Complete  
**Research date:** 2026-07-20  
**Depends on:** R-01 (competitive patterns), R-03–R-05 (module contracts), R-05 (drift escalation)

---

## 1. Executive summary

**Recommendation:** Build a **modular, Python-centric validation workbench** with four architectural pillars:

| Pillar | v1 design |
| ------ | --------- |
| **Ingestion boundary** | Narrow sklearn-compatible contract + labeled CSV/Parquet; OCC model-definition intake gate; vendor path via `VendorModelAdapter` |
| **Audit log** | **Greenfield hash-chained append-only table** (SQLite v1) implementing FINOS **mi-21 Tier 1–2**; Tier 3 crypto trail documented as build target (Monitaur-inspired, not vendor-dependent) |
| **Report generator** | **Literal OCC 2026-13 seven-section** Jinja2 → Markdown (+ optional PDF); three validation components mapped to §V subsections |
| **System shape** | Validation core + optional monitoring adapter + materiality engine + challenger slot (R-10) |

**Open questions resolved this session:**

| # | Question | Decision |
| - | -------- | -------- |
| 1 | Audit log: Monitaur vs model-ledger vs greenfield? | **Greenfield hash chain** for validation audit; optional **model-ledger export hook** for inventory events (v2) |
| 2 | SQLite vs Postgres vs DuckDB? | **SQLite** for v1 inventory + audit (WAL, append-only); Postgres production path; DuckDB analytical read layer only |
| 3 | Report format v1? | **Markdown primary** + optional PDF via WeasyPrint |
| 4 | Vendor/black-box ingest? | **`VendorModelAdapter`** sklearn shim over scoring API |
| 6 | MCP v1 or v2? | **v1 interface hook only**; MCP server implementation deferred to v2 |
| 8 | Materiality re-tiering? | **Event-driven exposure check** on each validation/monitoring run; governance event + cadence update |

---

## 2. Model ingestion contract

### 2.1 Boundary interface (v1)

The Workbench accepts at the boundary:

```yaml
model_ingest:
  # Path A — serialized in-process model (primary demo)
  format: joblib | pickle
  interface:
    required: [predict]
    optional: [predict_proba]
  framework_hint: sklearn | xgboost | lightgbm | null

  # Path B — vendor/black-box API (Section VII)
  format: vendor_api
  adapter: VendorModelAdapter
  endpoint: https://...
  auth: env_var_ref
  response_mapping:
    score_field: probability_of_default
    feature_order: [EXT_SOURCE_1, EXT_SOURCE_2, ...]

  # Path C — deferred
  format: onnx  # v1.1 optional; not required for German Credit demo

dataset_ingest:
  format: csv | parquet
  required_columns:
    - features: list[str]          # must match model input schema
    - label: str                    # ground-truth outcome
    - decision_column: str         # approval_binary | score_continuous
  optional_columns:
    - protected_attributes:         # validation-only; NEVER model inputs
        - name: sex
          source: direct | bisg_proxy | hmda
          reference_group: male
```

**Narrow contract rationale (✅ foundation §6.2):** Fairlearn, SHAP, and scipy all expect in-memory tabular arrays. A sklearn-compatible `.predict()` / `.predict_proba()` surface is sufficient for the German Credit and Home Credit demos without format sprawl.

### 2.2 OCC 2026-13 model-definition intake gate

Before any validation run, apply the **model definition test** (OCC Bulletin 2026-13, primary ✅ S-38):

> "the term 'model' refers to a complex quantitative method, system, or approach that applies statistical, economic, or financial theories to process input data into quantitative estimates… excludes simple arithmetic calculations… deterministic rule-based processes… where there are no statistical, economic, or financial theories underpinning their design or use."

**Intake gate logic:**

```python
def passes_model_definition(metadata: ModelMetadata) -> GateResult:
    if metadata.methodology_type in ("spreadsheet_arithmetic", "deterministic_rules"):
        return REJECT("Excluded under OCC 2026-13 model definition")
    if not metadata.has_statistical_economic_or_financial_theory_basis:
        return REJECT("No theory basis documented")
    if metadata.complexity_tier == "trivial":
        return REJECT("Below complexity threshold")
    return PASS
```

**Required metadata at ingest** (feeds materiality engine):

| Field | Purpose | Maps to |
| ----- | ------- | ------- |
| `model_id`, `version` | Identity + versioning | Inventory, audit binding |
| `owner`, `validator` | Governance | §VI |
| `intended_use` | Qualitative purpose input | Materiality tier |
| `exposure` (quantitative) | Portfolio $, decision volume, % of book | Materiality tier |
| `methodology_type` | Intake gate | §IV |
| `theory_basis` | Intake gate narrative | §IV Conceptual Soundness |
| `vendor_flag` | Routes Section VII | §VII |
| `guidance_version` | `OCC-2026-13` | Report header |

### 2.3 Protected-class hard reject (R-03 binding)

At schema validation:

1. Compare `model.feature_names_in_` (or declared feature list) against protected-class column registry.
2. **Hard reject** if any protected attribute appears as a model input.
3. Protected attributes in the **dataset only** (for validation battery) are permitted with `source: direct | bisg_proxy | hmda` annotation.

### 2.4 Format recommendations (demo-driven, not convenience-driven)

| Format | v1 role | Rationale |
| ------ | ------- | --------- |
| **joblib/pickle** | ✅ Primary | German Credit XGBoost demo; sklearn ecosystem norm (ValidMind pattern ✅ S-03) |
| **Vendor API wrapper** | ✅ Required path | OCC §VII — banks often lack vendor source code ✅ S-38 |
| **ONNX** | ⚠ v1.1 | Adds onnxruntime dependency; no demo dataset requires it |
| **PMML** | ❌ Defer | Legacy scorecard shops; out of portfolio scope |

### 2.5 VendorModelAdapter contract

Black-box vendor models enter through a thin sklearn shim:

```python
class VendorModelAdapter:
    """sklearn-compatible wrapper for third-party scoring APIs."""

    def __init__(self, endpoint: str, feature_order: list[str], ...): ...

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        # POST batch or row; map response → (n_samples, 2) array
        ...

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        proba = self.predict_proba(X)
        return (proba[:, 1] >= self.threshold).astype(int)

    @property
    def feature_names_in_(self) -> np.ndarray:
        return np.array(self.feature_order)
```

**Section VII artifact:** vendor assessment record capturing conceptual soundness evidence available without source code, customization documentation, and ongoing monitoring plan (score-distribution ingest only).

---

## 3. Tamper-evident audit log (FINOS AIR-DET-021)

### 3.1 Competitive evaluation

| Option | Strengths | Weaknesses | v1 decision |
| ------ | --------- | ---------- | ----------- |
| **Monitaur** (commercial) | Cryptographically signed decision-level logs ✅ S-47; closest FINOS Tier 3 analog | Proprietary; enterprise pricing; not composable | **Pattern reference**, not dependency |
| **block/model-ledger** (OSS) | Append-only event log; MCP-native; SR 26-2 profiles ✅ S-46 | Inventory/discovery focus; snapshots content-addressed but **not yet hash-chained end-to-end** ⚠ S-46 guarantees.md | **Integration hook** for inventory events (v2), not core audit store |
| **Greenfield hash chain** | Full control; binds validation artifacts; cites FINOS mi-21 by control ID | Build cost | **v1 implementation** |

**Decision:** Implement a **greenfield hash-chained append-only audit log** inspired by Monitaur's tamper-evidence pattern and FINOS mi-21 verbatim guidance (✅ S-45):

> "cryptographic hash chaining, signed log segments, or anchoring digests to an append-only transparency log raise integrity from operator-asserted to independently auditable."

model-ledger's own documentation acknowledges chained Merkle hashing as a **deliberate future change**, not current capability ⚠ — insufficient alone for Tier 3 claims.

### 3.2 Tier interface design (0–3)

| Tier | v1 scope | Controls implemented |
| ---- | -------- | -------------------- |
| **Tier 0** | Interface only | ADR stub; no retention |
| **Tier 1** | ✅ Demo default for T1 models | Event type, timestamp, actor, input refs (hashed), output refs, model version |
| **Tier 2** | ✅ Production demo for T2/T3 | Tier 1 + explicit reasoning payloads (adverse-action attribution, mapping methodology version, confidence) |
| **Tier 3** | 📋 Documented build target | Tier 2 + Ed25519 signed segments + optional digest anchoring; cite control ID in design doc |

**v1 implements Tier 1–2.** Tier 3 is architected (schema slots for `signature`, `anchor_digest`) but not required for portfolio demo.

### 3.3 Hash-chained log schema

```sql
CREATE TABLE audit_log (
    seq_id          INTEGER PRIMARY KEY AUTOINCREMENT,  -- monotonic
    event_id        TEXT NOT NULL UNIQUE,               -- UUID
    event_type      TEXT NOT NULL,                      -- see §3.4
    timestamp_utc   TEXT NOT NULL,                      -- ISO-8601
    model_id        TEXT NOT NULL,
    model_version   TEXT NOT NULL,
    materiality_tier TEXT NOT NULL,                     -- T1|T2|T3
    actor           TEXT NOT NULL,                      -- user/service id
    payload_json    TEXT NOT NULL,                      -- event-specific body
    payload_hash    TEXT NOT NULL,                      -- SHA-256(payload_json)
    prev_hash       TEXT NOT NULL,                      -- payload_hash of seq_id-1 (genesis: zeros)
    chain_hash      TEXT NOT NULL,                      -- SHA-256(prev_hash || payload_hash || metadata)
    finos_control   TEXT NOT NULL,                      -- e.g. mi-21, mi-4, mi-5
    finos_tier      INTEGER NOT NULL,                   -- 0-3
    artifact_refs   TEXT                              -- JSON array of {name, sha256}
);
-- Append-only enforced at application layer; no UPDATE/DELETE grants
```

**Verification CLI:** `workbench audit verify-chain [--from seq] [--to seq]` recomputes chain_hash and reports breaks.

### 3.4 Event catalog (bound to Session 2 modules)

| Event type | FINOS control | Tier | Trigger | Payload highlights |
| ---------- | ------------- | ---- | ------- | ------------------ |
| `validation_run.start` | mi-5 | 1 | Validation orchestrator | scope, dataset hash, config hash |
| `validation_run.complete` | mi-5 | 1 | Battery finished | pass/fail summary, duration |
| `bias_battery.result` | mi-5 | 2 | R-03 module | metrics by layer, jurisdiction frame, AIR/FPR flags |
| `adverse_action.attribution` | mi-21 | 2 | R-04 Stage 1–4 | SHAP values, principal reasons, mapping_methodology_id |
| `adverse_action.methodology_published` | mi-21 | 2 | Mapping artifact created | methodology version, SHA-256 |
| `drift.event` | mi-4 | 1–2 | R-05 engine | PSI/KS/AUC values, alert_level, tier escalation action |
| `report.generated` | mi-21 | 1 | Report builder | report section hashes, OCC section checklist |
| `materiality.retier` | — | 1 | Exposure threshold crossed | old_tier, new_tier, trigger_exposure |
| `governance.approval` | mi-11 | 2 | Human sign-off | approver, scope, residual risk |
| `guardrail.violation` | mi-21 | 2 | Policy check fail | Art. 12(2)(a) mapping |

### 3.5 EU AI Act Article 12 mapping

| Art. 12 requirement | Audit log capture |
| ------------------- | ----------------- |
| **12(2)(a)** guardrail violations, exception paths | `guardrail.violation`, intake gate rejects, protected-class hard reject |
| **12(2)(b)** drift/performance aggregates | `drift.event` with metric snapshots; validation performance summaries |
| **12(2)(c)** human review touchpoints | `governance.approval`, adverse-action validator sign-off slot (R-04) |
| **Art. 26(5)** deployer monitoring | Export API / Markdown audit packet for deployer (not provider-only) |

### 3.6 LLM/agent extensibility (choice B)

Design a **trajectory normalization interface** inspired by AgentRx (✅ S-49) without implementing gen-AI MRM:

```python
class TrajectoryNormalizer(Protocol):
    """AgentRx Stage 1 analog — normalize heterogeneous agent logs to audit schema."""

    def normalize(self, raw_trace: dict) -> list[AuditEvent]:
        """Map tool calls, prompts, decisions → Tier 1/2 audit events."""
        ...
```

- v1: Protocol + stub adapter; credit-model validation uses direct module events.
- v2: Implement normalizer for multi-agent loan workflow (FINOS uc-3 pattern).
- Document mi-21 caveat for hidden-reasoning models (o1-class) per FINOS primary text ✅ S-45.

---

## 4. OCC 2026-13 seven-section report generator

### 4.1 Design principle

Reports are structured around **literal OCC section titles** (I–VII), not a three-pillar retrofit. Each section is a Jinja2 template partial; content is populated from module outputs and inventory metadata.

### 4.2 Section mapping

| Section | OCC title | Workbench content source | Primary modules |
| ------- | --------- | ------------------------ | --------------- |
| **I** | Introduction | Model summary, validation scope, date, validator identity, guidance version | Inventory + run metadata |
| **II** | Purpose and Scope | Intended use, applicability statement, materiality tier rationale (exposure × purpose) | Materiality engine |
| **III** | Overview of Model Risk and MRM | Inherent risk assessment, exposure × purpose narrative, known limitations | Inventory + tier config |
| **IV** | Model Development and Model Use | Data lineage, feature inventory, development summary, customization notes | Dataset manifest + feature registry |
| **V** | Model Validation and Monitoring | See §4.3 three components | bias_battery, adverse_action_translator, drift_monitor |
| **VI** | Governance and Controls | Inventory entry, approval workflow status, documentation index, audit log summary | Inventory + governance events |
| **VII** | Vendor and Other Third-Party Products | Vendor assessment (if `vendor_flag=true`); monitoring without source code | VendorModelAdapter metadata |

### 4.3 Three validation components → §V subsections

OCC 2026-13 names three validation components (primary ✅ S-38). Map to §V subsections:

| OCC component | §V subsection | Workbench source |
| ------------- | ------------- | ---------------- |
| **Conceptual Soundness** | §V.1 | Intake gate result, theory basis, feature definitions, SHAP global summary (sanity), translation methodology overview |
| **Outcomes Analysis** | §V.2 | R-03 bias battery (three layers), jurisdiction frame statement, proxy-risk report |
| **Ongoing Model Monitoring** | §V.3 | R-05 drift summary, escalation history, tier-gated cadence, recommended actions |

### 4.4 Appendices (hash-bound to audit log)

| Appendix | Content | Hash binding |
| -------- | ------- | ------------ |
| **A** | Translation methodology artifact (R-04) | `translation_methodology_v{N}.json` SHA-256 → `report.generated` event |
| **B** | Bias battery detailed tables (R-03) | `bias_battery_summary.json` SHA-256 |
| **C** | Drift monitoring snapshot (R-05) | `drift_report.json` SHA-256 |
| **D** | Fidelity validation report (R-04 Stage 3) | `fidelity_validation_report.json` SHA-256 |
| **E** | Audit log chain verification summary | Last `chain_hash`, event count, verification status |

### 4.5 Report output format

| Format | v1 | Rationale |
| ------ | -- | --------- |
| **Markdown** | ✅ Primary | Git-diffable, portfolio-friendly, Jinja2-native |
| **PDF** | ✅ Optional export | Examiner packet; WeasyPrint from same HTML intermediate |
| **JSON** | ✅ Machine-readable | API consumers, audit binding |
| **DOCX** | ❌ Defer v2 | Low priority for portfolio demo |

---

## 5. System architecture (high-level)

### 5.1 Component diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Workbench CLI / Python SDK                    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Intake Gate   │     │ Materiality     │     │ Model Inventory │
│ + Ingest      │────▶│ Engine          │────▶│ (SQLite)        │
└───────┬───────┘     └────────┬────────┘     └─────────────────┘
        │                      │
        ▼                      ▼
┌───────────────────────────────────────────────────────────────────┐
│                    Validation Orchestrator                         │
│  ┌─────────────┐ ┌──────────────────────┐ ┌──────────────────┐  │
│  │bias_battery │ │adverse_action_transl.│ │ drift_monitor    │  │
│  │  (R-03)     │ │       (R-04)         │ │    (R-05)        │  │
│  └─────────────┘ └──────────────────────┘ └──────────────────┘  │
└───────────────────────────────┬───────────────────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Audit Log     │     │ Report Generator │     │ Challenger Slot │
│ (hash chain)  │     │ (OCC I–VII)      │     │ (R-10 defer)    │
└───────────────┘     └─────────────────┘     └─────────────────┘
        │
        ▼ (v2 hook)
┌───────────────┐
│ model-ledger  │
│ export adapter│
└───────────────┘
```

### 5.2 Modular split (R-01 pattern)

| Layer | Responsibility | Competitive analog |
| ----- | -------------- | ------------------ |
| **Validation core** | Ingest → battery → report → audit | ValidMind validation workflows |
| **Monitoring adapter** | Scheduled drift runs, reference population management | Fiddler post-deployment (optional plug-in) |
| **Inventory + governance** | Model registry, tiering, approvals | ModelOp / Monitaur system of record (subset) |

v1 ships validation core + monitoring as **in-process modules**; monitoring adapter interface allows future extraction.

### 5.3 Lifecycle-to-evidence mapping (Databricks pattern ⚠ S-48)

| Lifecycle stage | Artifact produced | Storage |
| --------------- | ----------------- | ------- |
| Data sourcing | Dataset manifest + quality metrics | `datasets/` + audit event |
| Feature engineering | Feature inventory snapshot | Report §IV + audit |
| Development | Model artifact + hyperparameters | Inventory entry |
| Independent validation | OCC seven-section report + appendices | `reports/` + audit |
| Deployment | Promotion record (demo: approval event) | Governance event |
| Monitoring | Drift reports + escalation log | Report §V.3 + audit |

### 5.4 Model inventory schema

```sql
CREATE TABLE model_inventory (
    model_id            TEXT PRIMARY KEY,
    version             TEXT NOT NULL,
    name                TEXT NOT NULL,
    owner               TEXT NOT NULL,
    intended_use        TEXT NOT NULL,
    exposure_metric     REAL NOT NULL,        -- e.g. portfolio_pct
    exposure_unit       TEXT NOT NULL,        -- portfolio_pct | decision_count | notional_usd
    purpose_category    TEXT NOT NULL,        -- credit_decisioning | internal_risk | experimental
    materiality_tier    TEXT NOT NULL,        -- T1 | T2 | T3
    vendor_flag         BOOLEAN DEFAULT FALSE,
    vendor_name         TEXT,
    methodology_type    TEXT NOT NULL,
    theory_basis        TEXT NOT NULL,
    guidance_version    TEXT DEFAULT 'OCC-2026-13',
    status              TEXT NOT NULL,        -- draft | validated | monitoring | retired
    created_at          TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    challenger_model_id TEXT,                 -- slot for R-10
    UNIQUE(model_id, version)
);
```

### 5.5 Materiality tiering engine

**Formula (OCC 2026-13 ✅ S-38):** `materiality = f(exposure, purpose)`

```python
def compute_tier(exposure: float, purpose: PurposeCategory) -> Tier:
    # Configurable thresholds; defaults from R-05
    if purpose == PurposeCategory.REGULATORY_REPORTING:
        return T3
    if exposure >= 0.10 or purpose == PurposeCategory.CREDIT_DECISIONING:
        return T3
    if exposure >= 0.01:
        return T2
    return T1
```

### 5.6 Materiality re-tiering (feeds R-10)

When `exposure` crosses a configured threshold:

1. Emit `materiality.retier` audit event (old_tier → new_tier, trigger value).
2. Update `model_inventory.materiality_tier`.
3. Adjust monitoring cadence per R-05 tier table.
4. If upgrade to T3: flag "re-validation recommended" (not auto-block in v1).
5. Surface in report §II (tier rationale) and §VI (governance change log).

**No automatic validation re-run in v1** — governance notification only; R-10 defines UX.

### 5.7 Challenger-model comparison hook

Architect slot without implementation:

```python
class ChallengerComparison(Protocol):
    def compare(self, champion: Model, challenger: Model, dataset: Dataset) -> ComparisonReport: ...
```

- Inventory field: `challenger_model_id`
- Report §V.2 optional subsection: "Champion-Challenger Outcomes" (empty stub in v1)
- R-10 defines demo scenario

### 5.8 Extended validation_run contract (unified I/O)

Extends R-03 §7.1:

```yaml
validation_run:
  model: sklearn-compatible | VendorModelAdapter
  dataset: labeled CSV/Parquet
  decision_column: approval_binary | score_continuous
  protected_attributes:
    - name: sex
      source: direct | bisg_proxy | hmda
      reference_group: male
  regulatory_frame:
    federal_ecoa: proxy_discrimination
    fha_overlay: false
    state_overlay: none
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
    report_format: [markdown, pdf]
    artifact_dir: ./artifacts/{run_id}/
```

---

## 6. Implications for Workbench

1. **Implement narrow ingest first** — joblib + CSV for German Credit; VendorModelAdapter as second path for §VII narrative.
2. **Build greenfield hash-chained audit log in SQLite** — Tier 1–2 for v1; document Tier 3 schema extension; cite FINOS **AIR-DET-021** by control ID in README and report §VI.
3. **Report generator is a first-class module** — seven Jinja2 section templates, not a generic PDF dump; appendices hash-bound to audit log.
4. **Compose OSS, don't fork** — Fairlearn/Aequitas/SHAP/scipy inside modules; audit and report are Workbench-native.
5. **Optional model-ledger export** — v2 hook for inventory event sync; do not depend on model-ledger for tamper evidence (no end-to-end chain yet).
6. **TrajectoryNormalizer protocol** — satisfies choice B extensibility without gen-AI scope creep.
7. **Materiality engine runs at ingest and on exposure update** — re-tiering is event-driven, not batch-only.
8. **Challenger slot in schema and report** — defer logic to R-10.

---

## 7. Sources

| ID | Source | Tier | Status | Used for |
| -- | ------ | ---- | ------ | -------- |
| S-38 | OCC Bulletin 2026-13 PDF | 1 | ✅ | Model definition, seven sections, §VII vendor |
| S-45 | FINOS AIR-DET-021 mi-21 primary | 1 | ✅ | Tier 0–3, tamper-evidence, Art. 12 mapping |
| S-46 | block/model-ledger guarantees.md | 2 | ✅ | Content-addressed vs chained hash gap |
| S-47 | Monitaur platform + whitepaper | 3 | ✅ | Crypto-signed decision log pattern |
| S-48 | Databricks MRM 2026 banker guide | 2 | ⚠ | Lifecycle-to-evidence mapping |
| S-49 | Microsoft Research AgentRx | 2 | ✅ | Trajectory normalization pattern |
| S-03 | ValidMind Python SDK pattern | 3 | ✅ | Ingest + notebook norm |
| S-13 | block/model-ledger GitHub | 3 | ✅ | Inventory OSS evaluation |
| S-09 | Monitaur case studies | 3 | ✅ | Decision logging at scale |

---

## 8. Open questions (deferred)

1. **Tier 3 signing key management** — HSM vs software Ed25519 for portfolio demo; defer to build phase.
2. **model-ledger bidirectional sync** — export-only vs full inventory replacement; R-10/R-build decision.
3. **Streaming drift adapter** — batch v1; Kafka/EventBridge interface sketch for v2.
4. **Multi-model ensemble attribution** — R-04 open question; aggregate SHAP across ensemble members.
5. ~~Primary-source spot-check of the unverified "2026-03" circular claim~~ — ✅ Resolved: no such circular exists (R-12/R-14); differentiator #3 re-anchored to Reg B §1002.9 + historical Circular 2022-03/2023-03 (withdrawn May 12, 2025).
