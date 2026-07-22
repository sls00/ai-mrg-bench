"""Model and dataset ingestion with protected-class gate."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import yaml

from workbench.config import ValidationRunConfig


@dataclass(slots=True)
class IntakeResult:
    status: str
    reason: str


@dataclass(slots=True)
class IngestedArtifacts:
    model: Any
    dataset: pd.DataFrame
    model_features: list[str]


def load_registry_names(path: Path) -> set[str]:
    payload = yaml.safe_load(path.read_text())
    protected = payload.get("protected_attributes", [])
    return {str(entry["name"]) for entry in protected}


def load_model_and_dataset(
    config: ValidationRunConfig, protected_registry_path: Path
) -> IngestedArtifacts:
    model = joblib.load(config.model_path)
    dataset = pd.read_csv(config.dataset_path)
    model_features = _model_feature_names(model)
    protected_names = load_registry_names(protected_registry_path)
    enforce_protected_class_gate(model_features, protected_names)
    ensure_required_columns(dataset, config)
    return IngestedArtifacts(model=model, dataset=dataset, model_features=model_features)


def run_intake_gate(config: ValidationRunConfig) -> IntakeResult:
    blocked_methodologies = {"spreadsheet_arithmetic", "deterministic_rules"}
    if config.methodology_type in blocked_methodologies:
        reason = (
            f"Methodology '{config.methodology_type}' is excluded by "
            "OCC model-definition gate."
        )
        return IntakeResult(
            status="REJECT",
            reason=reason,
        )
    if not config.theory_basis.strip():
        return IntakeResult(status="REJECT", reason="Model metadata missing theory_basis.")
    return IntakeResult(
        status="PASS",
        reason="Model metadata passes OCC model-definition intake gate.",
    )


def _model_feature_names(model: Any) -> list[str]:
    feature_names = getattr(model, "feature_names_in_", None)
    if feature_names is None:
        raise ValueError(
            "Model is missing feature_names_in_; cannot enforce protected-class gate.",
        )
    return [str(value) for value in feature_names]


def enforce_protected_class_gate(model_features: list[str], protected_names: set[str]) -> None:
    collisions = sorted(set(model_features).intersection(protected_names))
    if collisions:
        joined = ", ".join(collisions)
        raise ValueError(
            f"Protected-class ingest gate failed: model uses prohibited inputs: {joined}",
        )


def ensure_required_columns(dataset: pd.DataFrame, config: ValidationRunConfig) -> None:
    required = {config.label_column, config.decision_column}
    required.update(attribute.name for attribute in config.protected_attributes)
    missing = sorted(required.difference(dataset.columns))
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Dataset is missing required columns: {joined}")
