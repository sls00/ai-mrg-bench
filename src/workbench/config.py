"""Configuration models and YAML loader for validation runs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class ProtectedAttributeConfig:
    name: str
    source: str
    reference_group: str


@dataclass(slots=True)
class RegulatoryFrameConfig:
    federal_ecoa: str
    fha_overlay: bool
    state_overlay: str


@dataclass(slots=True)
class MaterialityConfig:
    exposure: float
    exposure_unit: str
    purpose: str


@dataclass(slots=True)
class ModuleFlags:
    bias_battery: bool
    adverse_action_translator: bool
    drift_monitor: bool


@dataclass(slots=True)
class AuditConfig:
    finos_tier: int
    actor: str
    db_path: Path


@dataclass(slots=True)
class OutputConfig:
    report_format: list[str]
    artifact_dir_template: str

    def artifact_dir_for(self, run_id: str) -> Path:
        return Path(self.artifact_dir_template.format(run_id=run_id))


@dataclass(slots=True)
class ValidationRunConfig:
    run_id: str
    model_id: str
    model_version: str
    model_path: Path
    dataset_path: Path
    decision_column: str
    label_column: str
    intended_use: str
    methodology_type: str
    theory_basis: str
    guidance_version: str
    protected_attributes: list[ProtectedAttributeConfig]
    regulatory_frame: RegulatoryFrameConfig
    materiality: MaterialityConfig
    modules: ModuleFlags
    audit: AuditConfig
    outputs: OutputConfig
    reference_dataset_path: Path | None = None
    monitor_dataset_path: Path | None = None

    @classmethod
    def from_yaml(cls, path: Path) -> ValidationRunConfig:
        payload = yaml.safe_load(path.read_text())
        if "validation_run" not in payload:
            raise ValueError(f"{path} is missing top-level 'validation_run'")
        run = payload["validation_run"]

        protected = [
            ProtectedAttributeConfig(
                name=item["name"],
                source=item.get("source", "direct"),
                reference_group=item.get("reference_group", ""),
            )
            for item in run["protected_attributes"]
        ]
        base_dir = path.parent
        modules = ModuleFlags(**run["modules"])
        reference_dataset_path = (
            _resolve_existing_path(run["reference_dataset"], base_dir)
            if "reference_dataset" in run
            else None
        )
        monitor_dataset_path = (
            _resolve_existing_path(run["monitor_dataset"], base_dir)
            if "monitor_dataset" in run
            else None
        )
        drift_datasets_missing = reference_dataset_path is None or monitor_dataset_path is None
        if modules.drift_monitor and drift_datasets_missing:
            raise ValueError(
                f"{path}: modules.drift_monitor is true but reference_dataset and "
                "monitor_dataset must both be configured",
            )
        return cls(
            run_id=run["run_id"],
            model_id=run.get("model_id", "german-credit-xgb"),
            model_version=run.get("model_version", "v1.2"),
            model_path=_resolve_existing_path(run["model"], base_dir),
            dataset_path=_resolve_existing_path(run["dataset"], base_dir),
            decision_column=run["decision_column"],
            label_column=run["label_column"],
            intended_use=run.get("intended_use", "credit underwriting decision support"),
            methodology_type=run.get("methodology_type", "statistical_credit_model"),
            theory_basis=run.get("theory_basis", "statistical credit-risk modeling"),
            guidance_version=run.get("guidance_version", "OCC-2026-13"),
            protected_attributes=protected,
            regulatory_frame=RegulatoryFrameConfig(**run["regulatory_frame"]),
            materiality=MaterialityConfig(**run["materiality"]),
            modules=modules,
            audit=AuditConfig(
                finos_tier=int(run["audit"]["finos_tier"]),
                actor=run["audit"]["actor"],
                db_path=_resolve_output_path(run["audit"].get("db_path", "workbench.db"), base_dir),
            ),
            outputs=OutputConfig(
                report_format=list(run["outputs"]["report_format"]),
                artifact_dir_template=run["outputs"]["artifact_dir"],
            ),
            reference_dataset_path=reference_dataset_path,
            monitor_dataset_path=monitor_dataset_path,
        )

    def as_metadata(self) -> dict[str, Any]:
        """Compact metadata payload used in audit events."""
        return {
            "run_id": self.run_id,
            "model_id": self.model_id,
            "model_version": self.model_version,
            "guidance_version": self.guidance_version,
            "materiality_exposure": self.materiality.exposure,
            "materiality_purpose": self.materiality.purpose,
            "modules": {
                "bias_battery": self.modules.bias_battery,
                "adverse_action_translator": self.modules.adverse_action_translator,
                "drift_monitor": self.modules.drift_monitor,
            },
        }


def _resolve_existing_path(raw_path: str, base_dir: Path) -> Path:
    candidate = (base_dir / raw_path).resolve()
    if candidate.exists():
        return candidate
    return (Path.cwd() / raw_path).resolve()


def _resolve_output_path(raw_path: str, base_dir: Path) -> Path:
    del base_dir
    absolute = Path(raw_path)
    if absolute.is_absolute():
        return absolute
    return (Path.cwd() / raw_path).resolve()
