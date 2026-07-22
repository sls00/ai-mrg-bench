"""Python SDK entry point for validation runs."""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from workbench.audit import AuditStore, verify_audit_chain
from workbench.bias_battery import run_bias_battery
from workbench.config import ValidationRunConfig
from workbench.ingest import load_model_and_dataset, run_intake_gate
from workbench.materiality import assign_materiality_tier
from workbench.report import generate_occ_report


@dataclass(slots=True)
class ValidationResult:
    run_id: str
    artifact_dir: Path
    report_path: Path


class ValidationRun:
    """Orchestrates one P0 validation workflow."""

    def __init__(self, config: ValidationRunConfig) -> None:
        self.config = config

    @classmethod
    def from_config(cls, config_path: Path) -> ValidationRun:
        return cls(ValidationRunConfig.from_yaml(config_path))

    def run(self) -> ValidationResult:
        config = self.config
        artifact_dir = config.outputs.artifact_dir_for(config.run_id)
        if not artifact_dir.is_absolute():
            artifact_dir = (Path.cwd() / artifact_dir).resolve()
        db_path = config.audit.db_path
        if not db_path.is_absolute():
            db_path = (Path.cwd() / db_path).resolve()
        audit = AuditStore(db_path)

        ingestion = load_model_and_dataset(
            config,
            protected_registry_path=(
                Path.cwd() / "configs" / "protected_class_registry.yaml"
            ).resolve(),
        )
        intake_result = run_intake_gate(config)
        if intake_result.status != "PASS":
            raise ValueError(intake_result.reason)

        materiality = assign_materiality_tier(
            config.materiality.exposure,
            config.materiality.purpose,
        )
        timestamp = _utc_now()
        audit.append_event(
            event_id=_event_id(),
            event_type="validation_run.start",
            timestamp_utc=timestamp,
            model_id=config.model_id,
            model_version=config.model_version,
            materiality_tier=materiality.tier,
            actor=config.audit.actor,
            payload={
                "config": config.as_metadata(),
                "dataset_sha256": _sha256_file(config.dataset_path),
                "intake_status": intake_result.status,
                "reasoning": {"intake_reason": intake_result.reason},
            },
            finos_control="mi-5",
            finos_tier=config.audit.finos_tier,
        )

        protected = config.protected_attributes[0]
        bias = run_bias_battery(
            dataset=ingestion.dataset,
            model=ingestion.model,
            model_features=ingestion.model_features,
            protected_attribute=protected.name,
            reference_group=protected.reference_group,
            decision_column=config.decision_column,
            label_column=config.label_column,
            run_id=config.run_id,
            regulatory_frame=config.regulatory_frame,
        )
        audit.append_event(
            event_id=_event_id(),
            event_type="bias_battery.result",
            timestamp_utc=_utc_now(),
            model_id=config.model_id,
            model_version=config.model_version,
            materiality_tier=materiality.tier,
            actor=config.audit.actor,
            payload=bias.payload,
            finos_control="mi-5",
            finos_tier=config.audit.finos_tier,
        )

        audit.append_event(
            event_id=_event_id(),
            event_type="validation_run.complete",
            timestamp_utc=_utc_now(),
            model_id=config.model_id,
            model_version=config.model_version,
            materiality_tier=materiality.tier,
            actor=config.audit.actor,
            payload={
                "status": "PASS",
                "intake": {"status": intake_result.status, "reason": intake_result.reason},
                "materiality": {"tier": materiality.tier, "rationale": materiality.rationale},
                "modules": {
                    "bias_battery": config.modules.bias_battery,
                    "adverse_action_translator": config.modules.adverse_action_translator,
                    "drift_monitor": config.modules.drift_monitor,
                },
                "reasoning": {
                    "summary": (
                        "Core P0 validation loop completed before report generation."
                    ),
                },
            },
            finos_control="mi-5",
            finos_tier=config.audit.finos_tier,
        )

        audit_summary = verify_audit_chain(db_path)
        run_context = {
            "run_id": config.run_id,
            "model_id": config.model_id,
            "model_version": config.model_version,
            "guidance_version": config.guidance_version,
            "actor": config.audit.actor,
            "intake_status": intake_result.status,
            "intake_reason": intake_result.reason,
            "intended_use": config.intended_use,
            "exposure": config.materiality.exposure,
            "purpose": config.materiality.purpose,
            "materiality_tier": materiality.tier,
            "methodology_type": config.methodology_type,
            "theory_basis": config.theory_basis,
            "jurisdiction_frame": {
                "federal_ecoa": config.regulatory_frame.federal_ecoa,
                "fha_overlay": config.regulatory_frame.fha_overlay,
                "state_overlay": config.regulatory_frame.state_overlay,
            },
            "layer_a": bias.payload["layers"]["A"],
            "layer_b": bias.payload["layers"]["B"],
            "layer_c": bias.payload["layers"]["C"],
            "finos_tier": config.audit.finos_tier,
            "audit_db": str(db_path),
            "audit_status": audit_summary.status,
            "audit_events": audit_summary.total_events,
            "audit_breaks": len(audit_summary.breaks),
        }
        report = generate_occ_report(
            artifact_dir=artifact_dir,
            run_context=run_context,
            bias_summary=bias.appendix_payload,
            audit_summary={
                "status": audit_summary.status,
                "events": audit_summary.total_events,
                "breaks": audit_summary.breaks,
                "event_type_counts": audit_summary.event_type_counts,
            },
        )

        artifact_refs = [
            {
                "name": "german_credit_validation_report.md",
                "sha256": _sha256_file(report.markdown_path),
            },
            {"name": "report.json", "sha256": _sha256_file(report.report_json_path)},
            {
                "name": "bias_battery_summary.json",
                "sha256": _sha256_file(report.appendix_b_path),
            },
            {
                "name": "audit_chain_verification.json",
                "sha256": _sha256_file(report.appendix_e_path),
            },
        ]
        audit.append_event(
            event_id=_event_id(),
            event_type="report.generated",
            timestamp_utc=_utc_now(),
            model_id=config.model_id,
            model_version=config.model_version,
            materiality_tier=materiality.tier,
            actor=config.audit.actor,
            payload={
                "report_path": str(report.markdown_path),
                "appendices": {
                    "A": "N/A",
                    "B": "present",
                    "C": "N/A",
                    "D": "N/A",
                    "E": "present",
                },
                "reasoning": {
                    "summary": (
                        "P0 report generated with Sections I-VI and appendices B/E."
                    ),
                },
            },
            finos_control="mi-21",
            finos_tier=config.audit.finos_tier,
            artifact_refs=artifact_refs,
        )
        final_verification = verify_audit_chain(db_path)
        if final_verification.status != "PASS":
            raise RuntimeError(f"audit verify-chain failed: {final_verification.breaks}")
        return ValidationResult(
            run_id=config.run_id,
            artifact_dir=artifact_dir,
            report_path=report.markdown_path,
        )


def _event_id() -> str:
    return str(uuid.uuid4())


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()
