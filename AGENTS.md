# ai-mrg-bench

Open, model-agnostic validation workbench for traditional ML credit models — tiering, bias/proxy testing, drift, hash-chained audit, and OCC reporting — for MRM reviewers and portfolio hiring demos.

## Commands

```bash
git lfs install && git lfs pull          # frozen demo models (models/*.joblib)
uv sync --all-extras --dev               # install
uv run pytest -q                         # test  (THE verification gate; CI also uses phase markers on labeled PRs)
uv run ruff check src tests              # lint
uv run mypy src                          # typecheck
bash scripts/check_fixture_hashes.sh     # fixture-byte integrity (CI gate)
bash scripts/check_circular_banlist.sh     # messaging hygiene (CI gate)
```

Run the app:

```bash
uv run workbench validate run --config configs/synth_fin_cre_baseline.yaml --output-dir artifacts/synth_fin_cre_p5/
uv run workbench audit verify-chain
```

## Conventions

- **CLI is canonical** — notebooks are companions; CI/reproducibility go through `workbench` + YAML configs, not notebook cells.
- **Phase pytest markers** — tag tests `@pytest.mark.phase0` … `phase5`; PR labels (`phase:p0` … `phase:p5`) set the CI floor (`docs/dev.md`).
- **Config-driven runs** — one validation workflow per YAML under `configs/`; copy `configs/synth_fin_cre_baseline.yaml` for new demos.
- **Fixture manifests are law** — `manifests/*_fixture_manifest.yaml` pins byte hashes; regenerate only via `scripts/freeze_*_fixtures.py` after bootstrap scripts.
- **Strict mypy** on `src/workbench` (`mypy_path = "src"`); canonical orchestration shape: `src/workbench/sdk.py` (`ValidationRun`).

## Do not

- Assert **CFPB Circular 2026-03** as current operative authority, or present CA/CO overlays / bias metrics as compliance determinations (see README do-not-claim).
- Edit committed `data/`, `models/`, or manifests by hand — run the freeze/bootstrap scripts and commit the manifest delta.
- `import evidence_workbench` or add a reverse dependency on `evid-wb-ui` — `workbench ui` PATH-execs `evidence-workbench` only.
- Add nondeterminism to validation/audit pipelines (fixture hashes and golden reports are CI-gated).
