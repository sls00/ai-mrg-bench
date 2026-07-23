"""Python SDK entry point for validation runs."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from workbench.adverse_action import run_adverse_action_translation
from workbench.audit import AuditStore, verify_audit_chain
from workbench.bias_battery import run_bias_battery
from workbench.config import ValidationRunConfig
from workbench.drift import run_drift_monitor
from workbench.ingest import load_model_and_dataset, run_intake_gate
from workbench.materiality import assign_materiality_tier
from workbench.overlay import resolve_state_overlay
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

        # Overlay artifacts must exist on disk (and be hash-bound) before
        # bias_battery.result is appended — audit log is append-only.
        artifact_dir.mkdir(parents=True, exist_ok=True)
        overlay = resolve_state_overlay(
            state_overlay=config.regulatory_frame.state_overlay,
            run_id=config.run_id,
            bias_layers=bias.payload["layers"],
            layer_a_label=str(bias.payload["layer_a_label"]),
            protected_attribute=protected.name,
        )
        if overlay is not None:
            overlay_path = artifact_dir / overlay.artifact_name
            overlay_path.write_text(
                json.dumps(overlay.artifact_payload, indent=2, sort_keys=True),
            )
            bias.payload["jurisdiction_frame"]["state_authority"] = overlay.state_authority
            bias.payload["overlay_artifacts"] = [
                {
                    "name": overlay.artifact_name,
                    "sha256": _sha256_file(overlay_path),
                },
            ]
            bias.appendix_payload["jurisdiction_frame"] = dict(
                bias.payload["jurisdiction_frame"],
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

        adverse_action_paths: dict[str, Path] | None = None
        adverse_action_section: dict[str, object] | None = None
        if config.modules.adverse_action_translator:
            adverse_action = run_adverse_action_translation(
                dataset=ingestion.dataset,
                model=ingestion.model,
                model_features=ingestion.model_features,
                decision_column=config.decision_column,
                run_id=config.run_id,
                model_id=config.model_id,
                model_version=config.model_version,
                created_utc=_utc_now(),
            )
            methodology_json_path = artifact_dir / "translation_methodology_v1.json"
            methodology_json_path.write_text(
                json.dumps(adverse_action.methodology_json, indent=2, sort_keys=True),
            )
            methodology_md_path = artifact_dir / "translation_methodology_v1.md"
            methodology_md_path.write_text(adverse_action.methodology_markdown.strip() + "\n")
            fidelity_path = artifact_dir / "fidelity_validation_report.json"
            fidelity_path.write_text(
                json.dumps(adverse_action.fidelity_json, indent=2, sort_keys=True),
            )
            adverse_action_paths = {
                "methodology_json": methodology_json_path,
                "methodology_md": methodology_md_path,
                "fidelity_json": fidelity_path,
            }

            proxy_features = {
                entry["feature"] for entry in bias.payload["layers"]["C"]["top_proxy_correlations"]
            }
            proxy_overlap = sorted(
                set(adverse_action.section_summary["top_global_features"]) & proxy_features,
            )
            adverse_action_section = {
                **adverse_action.section_summary,
                "proxy_overlap_features": proxy_overlap,
            }

            audit.append_event(
                event_id=_event_id(),
                event_type="adverse_action.methodology_published",
                timestamp_utc=_utc_now(),
                model_id=config.model_id,
                model_version=config.model_version,
                materiality_tier=materiality.tier,
                actor=config.audit.actor,
                payload={
                    "methodology_id": adverse_action.methodology_json["methodology_id"],
                    "model_id": config.model_id,
                    "model_version": config.model_version,
                    "reasoning": {
                        "summary": (
                            "Translation methodology artifact published per Reg B Sec 1002.9; "
                            "hash-bound below via artifact_refs."
                        ),
                    },
                },
                finos_control="mi-21",
                finos_tier=config.audit.finos_tier,
                artifact_refs=[
                    {
                        "name": "translation_methodology_v1.json",
                        "sha256": _sha256_file(methodology_json_path),
                    },
                    {
                        "name": "translation_methodology_v1.md",
                        "sha256": _sha256_file(methodology_md_path),
                    },
                ],
            )

            for event_payload in adverse_action.attribution_events:
                audit.append_event(
                    event_id=_event_id(),
                    event_type="adverse_action.attribution",
                    timestamp_utc=_utc_now(),
                    model_id=config.model_id,
                    model_version=config.model_version,
                    materiality_tier=materiality.tier,
                    actor=config.audit.actor,
                    payload=event_payload,
                    finos_control="mi-21",
                    finos_tier=config.audit.finos_tier,
                )

        drift_paths: dict[str, Path] | None = None
        drift_section: dict[str, object] | None = None
        if config.modules.drift_monitor:
            reference_dataset = pd.read_csv(config.reference_dataset_path)
            monitor_dataset = pd.read_csv(config.monitor_dataset_path)
            drift = run_drift_monitor(
                reference_dataset=reference_dataset,
                monitor_dataset=monitor_dataset,
                model=ingestion.model,
                model_features=ingestion.model_features,
                protected_attribute=protected.name,
                reference_group=protected.reference_group,
                run_id=config.run_id,
                materiality_tier=materiality.tier,
                reference_path=str(config.reference_dataset_path),
                monitor_path=str(config.monitor_dataset_path),
            )
            drift_report_path = artifact_dir / "drift_report.json"
            drift_report_path.write_text(
                json.dumps(drift.appendix_payload, indent=2, sort_keys=True),
            )
            drift_paths = {"drift_report": drift_report_path}
            drift_section = drift.section_context

            audit.append_event(
                event_id=_event_id(),
                event_type="drift.event",
                timestamp_utc=_utc_now(),
                model_id=config.model_id,
                model_version=config.model_version,
                materiality_tier=materiality.tier,
                actor=config.audit.actor,
                payload=drift.payload,
                finos_control="mi-4",
                finos_tier=config.audit.finos_tier,
                artifact_refs=[
                    {"name": "drift_report.json", "sha256": _sha256_file(drift_report_path)},
                ],
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
        if overlay is not None:
            run_context["jurisdiction_frame"]["state_authority"] = overlay.state_authority
            run_context["regulatory_frames"] = overlay.regulatory_frames
            run_context["overlay_non_claims"] = overlay.overlay_non_claims
            run_context["overlay_subsection_lines"] = overlay.overlay_subsection_lines
            run_context["overlay_battery_label"] = overlay.battery_label
            run_context["overlay_significant_decision"] = overlay.significant_decision
            run_context["overlay_artifact_name"] = overlay.artifact_name
        if adverse_action_section is not None:
            run_context["adverse_action"] = adverse_action_section
        if drift_section is not None:
            run_context["drift"] = drift_section
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
            appendix_a_path=(adverse_action_paths or {}).get("methodology_json"),
            appendix_d_path=(adverse_action_paths or {}).get("fidelity_json"),
            appendix_c_path=(drift_paths or {}).get("drift_report"),
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
        appendices_status = {
            "A": "N/A",
            "B": "present",
            "C": "N/A",
            "D": "N/A",
            "E": "present",
        }
        if adverse_action_paths is not None:
            appendices_status["A"] = "present"
            appendices_status["D"] = "present"
            artifact_refs.append(
                {
                    "name": "translation_methodology_v1.json",
                    "sha256": _sha256_file(adverse_action_paths["methodology_json"]),
                },
            )
            artifact_refs.append(
                {
                    "name": "fidelity_validation_report.json",
                    "sha256": _sha256_file(adverse_action_paths["fidelity_json"]),
                },
            )
        if drift_paths is not None:
            appendices_status["C"] = "present"
            artifact_refs.append(
                {
                    "name": "drift_report.json",
                    "sha256": _sha256_file(drift_paths["drift_report"]),
                },
            )
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
                "appendices": appendices_status,
                "reasoning": {
                    "summary": (
                        "Report generated with Sections I-VII and appendices "
                        + "/".join(
                            sorted(
                                letter
                                for letter, status in appendices_status.items()
                                if status == "present"
                            ),
                        )
                        + "."
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
