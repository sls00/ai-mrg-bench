# R-07 — Tech Stack Validation

**Ticket:** R-07  
**Session:** 3  
**Status:** Complete  
**Research date:** 2026-07-20  
**Depends on:** R-01 (competitive norms), R-06 (architecture constraints)

---

## 1. Executive summary

**Verdict:** The **Python-centric hypothesis is confirmed** for v1. Competitive landscape (ValidMind, NIMBUS, Fairlearn ecosystem — R-01 ✅) and architecture decisions (R-06) converge on a single stack optimized for **batch analytical validation + append-only audit logging**, not high-throughput transactional serving.

| Layer | v1 choice | Status |
| ----- | --------- | ------ |
| Core validation engine | **Python 3.11+** | ✅ Confirmed |
| Bias/fair-lending | **Fairlearn + Aequitas** | ✅ Confirmed (R-03) |
| Interpretability | **SHAP** | ✅ Confirmed (R-04) |
| Drift | **scipy + custom PSI** | ✅ Recommended (evidently rejected) |
| BISG proxy | **surgeo** (demo) + CFPB Stata reference | ✅ Recommended |
| Database | **SQLite** (inventory + audit) | ✅ Recommended |
| Analytical reads | **DuckDB** (optional) | ⚠ Optional helper |
| Report generation | **Jinja2 → Markdown + WeasyPrint PDF** | ✅ Recommended |
| API surface | **CLI + Python SDK** (FastAPI optional) | ✅ Recommended |
| Notebooks | **Jupyter** integration | ✅ Recommended |
| Deployment | **Local + Docker** | ✅ Confirmed |
| MCP extensibility | **Interface hook v1; server v2** | ✅ Confirmed |

---

## 2. Layer-by-layer evaluation

### 2.1 Core validation engine — Python

| Criterion | Assessment |
| --------- | ---------- |
| OSS ecosystem | Fairlearn, Aequitas, SHAP, scipy, sklearn — all Python-native ✅ |
| Competitive norm | ValidMind Python SDK + Jupyter ✅ S-03; Solytics NIMBUS Jupyter integration ✅ S-05 |
| Workload fit | Batch validation runs; no sub-100ms inference SLA |
| Alternatives considered | R-only (SAS/R bridges — enterprise incumbent pattern, not portfolio scale); Julia (thin ecosystem for fair-lending) |

**Decision:** Python 3.11+ as sole implementation language for v1.

### 2.2 Bias/fair-lending — Fairlearn + Aequitas

Already decided in R-03. Architecture binds via `bias_battery` module calling:
- Fairlearn `MetricFrame` for AIR, selection rate, error metrics
- Aequitas `Audit` for disparity tables and report structure

**No change.**

### 2.3 Interpretability — SHAP

Already decided in R-04. TreeSHAP → KernelSHAP routing.

**No change.**

### 2.4 Drift — scipy + custom PSI vs evidently

| Dimension | scipy + custom PSI | evidently |
| --------- | ------------------ | --------- |
| Dependency weight | Light (already required for KS) | Heavy (~100+ metrics, LLM evals, monitoring service) ⚠ S-51 |
| PSI implementation | ~30 lines numpy; full control over Lewis binning (R-05) | Built-in PSI preset; default threshold 0.1 (differs from R-05 Lewis bands) ⚠ |
| Differentiation | Tier escalation + OCC §V integration (R-05) | Metric breadth; monitoring dashboards |
| Audit binding | Direct integration with hash-chained log | Extra abstraction layer |
| Portfolio demo | Sufficient for German Credit + Home Credit | Overkill for batch-only v1 |

**Decision:** **scipy.stats.ks_2samp** for KS; **custom numpy PSI** function with R-05 decile binning rules. Reject evidently for v1.

**Rationale:** R-05 explicitly differentiated on tier escalation policy, not PSI calculation. Evidently adds dependency surface and monitoring-platform coupling without advancing the OCC seven-section or FINOS mi-21 differentiation thesis.

**v2 consideration:** Evidently as optional monitoring adapter backend if streaming/batch dashboard becomes a product feature.

### 2.5 BISG proxy — surgeo vs CFPB Stata port

| Option | Pros | Cons |
| ------ | ---- | ---- |
| **CFPB Stata scripts** ✅ S-19 | Regulatory ground truth; 2020 Census DHC update (Apr 2024) | Requires Stata license; subprocess orchestration; not Python-native |
| **surgeo** ✅ S-50 | Python/pandas-native; BISG + BIFSG; Jupyter-friendly | Last PyPI release 2021 ⚠; may lag 2020 Census DHC; not CFPB-maintained |
| **Greenfield port** | Full control | High effort; must validate against CFPB reference outputs |

**Decision:**
- **v1 demo:** `surgeo` for Home Credit BISG proxy pipeline (surname + ZIP/ZCTA).
- **Validation benchmark:** Document expected divergence from CFPB Stata reference; run spot-check on known surname/geocode pairs.
- **v2:** Evaluate maintained fork or partial port of CFPB `proxy-methodology` census tables (2020 DHC) into Python if surgeo accuracy gap is material.

**Open caveat (document in bias module):** CFPB uses ArcGIS geocoding; alternative geocoders yield different BISG probabilities ✅ S-19 report.

### 2.6 Database — SQLite vs Postgres vs DuckDB

| Store | Role | v1 | Rationale |
| ----- | ---- | -- | --------- |
| **SQLite** | Inventory + append-only audit log | ✅ Primary | Zero-config portfolio demo; WAL mode supports concurrent read; sufficient for <1M audit events |
| **Postgres** | Production multi-user | 📋 v2 path | Row-level security, concurrent writers, enterprise deploy |
| **DuckDB** | Analytical queries on validation datasets | ⚠ Optional | Fast Parquet/CSV scans for large Home Credit runs; not authoritative store |

**Append-only + hash-chain fit (R-06):** SQLite with application-enforced immutability (no UPDATE/DELETE on `audit_log`; triggers optional). Postgres migration is schema-compatible — same DDL, connection string swap.

**Reject DuckDB as primary store:** No native advantage for append-only transactional audit pattern; better as read accelerator.

### 2.7 Report generation — Jinja2 vs Quarto vs WeasyPrint

| Option | Assessment |
| ------ | ---------- |
| **Jinja2 → Markdown** | ✅ Primary — git-diffable, simple, maps 1:1 to OCC seven section templates |
| **WeasyPrint** (HTML → PDF) | ✅ Optional PDF export — pure Python, no LaTeX/R dependency |
| **Quarto** | ❌ Rejected v1 — adds R/Quarto toolchain; overkill for templated regulatory report |
| **ReportLab** | ❌ Rejected — programmatic PDF layout harder to maintain than HTML templates |
| **Pandoc** | ⚠ Optional v2 — Markdown → DOCX for examiner workflows |

**Decision:** Jinja2 templates in `templates/occ_2026_13/` → render Markdown → optional WeasyPrint PDF via shared HTML intermediate.

### 2.8 API surface — CLI + SDK vs FastAPI

| Surface | v1 scope | Rationale |
| ------- | -------- | --------- |
| **CLI** (`workbench validate`, `workbench audit verify-chain`, `workbench report`) | ✅ Required | Portfolio demo, CI integration, auditor reproducibility |
| **Python SDK** (`from workbench import ValidationRun`) | ✅ Required | ValidMind pattern; notebook integration |
| **FastAPI REST** | ⚠ Thin optional | Demo dashboard hook; 3 endpoints: `/validate`, `/reports/{id}`, `/audit/verify` |
| **gRPC** | ❌ Defer | No portfolio need |

**Decision:** CLI + SDK are primary; FastAPI as optional `workbench serve` extra (`pip install workbench[api]`).

### 2.9 Notebooks — Jupyter integration

ValidMind norm ✅ S-03: ship example notebooks:
- `notebooks/01_german_credit_validation.ipynb`
- `notebooks/02_home_credit_bias_proxy.ipynb`
- `notebooks/03_drift_escalation_demo.ipynb`

SDK designed for notebook-first exploration, CLI for reproducible runs.

### 2.10 Deployment

| Target | v1 |
| ------ | -- |
| Local venv | ✅ Primary dev |
| Docker Compose | ✅ Single-container demo (SQLite volume mount) |
| SaaS / K8s | ❌ Defer v2 |

### 2.11 MCP extensibility

| Scope | Decision |
| ----- | -------- |
| v1 | `MCPExportAdapter` protocol stub; document 4 tools mirroring model-ledger pattern (`record`, `investigate`, `query`, `changelog`) |
| v2 | Implement MCP server exposing audit log + inventory read tools |
| Rationale | model-ledger MCP is inventory-focused ✅ S-13; Workbench MCP would expose **validation evidence** — complementary, not duplicate |

---

## 3. Confirmed v1 dependency manifest

```toml
# pyproject.toml [project.dependencies] — illustrative v1 manifest
python = ">=3.11"

# Core ML / validation
scikit-learn = ">=1.4"
numpy = ">=1.26"
pandas = ">=2.1"
scipy = ">=1.11"

# Bias / fairness (compose, don't fork)
fairlearn = ">=0.10"
aequitas = ">=1.0"          # pin after compatibility test

# Interpretability
shap = ">=0.45"

# BISG proxy (demo)
surgeo = ">=1.1.2"

# Model ingest
joblib = ">=1.3"

# Reports
jinja2 = ">=3.1"
markdown = ">=3.5"
weasyprint = ">=62.0"       # optional [pdf] extra

# Data
pyarrow = ">=15.0"           # Parquet support

# Storage
# sqlite3 — stdlib

# CLI
typer = ">=0.12"
rich = ">=13.0"

# Optional extras
# [api]: fastapi, uvicorn
# [notebooks]: jupyter, matplotlib, plotly
# [analytical]: duckdb
# [vendor]: httpx
```

**Dev dependencies:** pytest, hypothesis (property tests for audit chain), ruff, mypy.

---

## 4. Alternatives considered and rejected

| Alternative | Why rejected |
| ----------- | ------------ |
| **evidently** for drift | Heavy; monitoring-platform scope; R-05 differentiation is escalation not PSI |
| **Quarto** for reports | R toolchain overhead; Jinja2 sufficient for seven-section structure |
| **Postgres** v1 | Operational complexity for portfolio demo; SQLite sufficient |
| **DuckDB** as primary DB | Wrong workload fit for append-only audit |
| **CFPB Stata subprocess** v1 | License friction; surgeo adequate for demo with documented caveats |
| **ONNX Runtime** v1 | No demo requirement; joblib sufficient |
| **Monitaur SDK** | Commercial; not composable |
| **model-ledger as audit backend** | No end-to-end hash chain yet ⚠ S-46 |
| **LLM report generation** | Cannot guarantee regulatory structure fidelity |

---

## 5. Deferred to v2

| Item | Trigger |
| ---- | ------- |
| Postgres backend | Multi-user / production deploy |
| Evidently monitoring adapter | Streaming dashboard product feature |
| MCP server implementation | Agent-tier governance demo |
| CFPB BISG Python port | surgeo accuracy gap on 2020 DHC |
| ONNX ingest | Enterprise model format demand |
| Quarto/Pandoc DOCX export | Examiner format request |
| FastAPI full REST surface | SaaS hosting |
| Ed25519 signed audit segments (Tier 3) | FINOS Tier 3 compliance demo |

---

## 6. Implications for Workbench

1. **Standardize on Python 3.11+ monorepo** with `typer` CLI and importable SDK package.
2. **Pin Fairlearn + Aequitas + SHAP** after compatibility matrix test on German Credit.
3. **Implement PSI as ~30-line internal utility** (`workbench.metrics.psi`) — do not add evidently.
4. **Use surgeo for Home Credit proxy demo** with methodology footnote on CFPB reference divergence.
5. **SQLite single-file database** (`workbench.db`) for inventory + audit; document Postgres migration path.
6. **Jinja2 seven-section report templates** with Markdown output; WeasyPrint behind `[pdf]` extra.
7. **Ship Jupyter notebooks** as primary demo surface (ValidMind pattern).
8. **Dockerfile** with optional extras documented; no cloud deploy in v1.
9. **MCP protocol stub** in `workbench.adapters.mcp` — interface only.

---

## 7. Sources

| ID | Source | Tier | Status | Used for |
| -- | ------ | ---- | ------ | -------- |
| S-03 | ValidMind Python SDK / Jupyter pattern | 3 | ✅ | API + notebook norm |
| S-05 | Solytics NIMBUS Jupyter integration | 3 | ✅ | Competitive stack signal |
| S-14 | Fairlearn + Aequitas GitHub | 3 | ✅ | Composition decision |
| S-19 | CFPB proxy-methodology | 1 | ✅ | BISG reference |
| S-50 | surgeo PyPI + docs | 2 | ✅ | Python BISG implementation |
| S-51 | evidently docs (PSI preset) | 2 | ⚠ | Rejection rationale |
| S-46 | model-ledger guarantees.md | 2 | ✅ | Audit backend rejection |
| S-35 | SHAP library | 2 | ✅ | Interpretability stack |
| S-13 | block/model-ledger MCP pattern | 3 | ✅ | MCP hook design |

---

## 8. Open questions

1. **Aequitas Python 3.11+ compatibility** — verify at build time; may need fork or pinned version.
2. **WeasyPrint system dependencies** — libcairo/pango in Docker image; document in README.
3. **surgeo 2020 Census tables** — manual update vs fork if demo accuracy insufficient.
4. **FastAPI auth** — defer; v1 local-only has no auth requirement.
5. **Property test coverage target** — recommend hypothesis tests for audit chain (mirror model-ledger pattern ✅ S-46).
