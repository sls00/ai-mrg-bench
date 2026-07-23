"""State-overlay profiles for P3 jurisdictional-frame demos (CA ADMT / CO SB 26-189)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Static lookup mirroring ESCALATION_ACTIONS in workbench.drift — not a YAML profile block.
OVERLAY_PROFILES: dict[str, dict[str, Any]] = {
    "CA": {
        "state_authority": (
            "California CCPA/CPRA ADMT (CPPA, Cal. Code Regs tit. 11)"
        ),
        "artifact_name": "admt_risk_assessment_summary.json",
        "significant_decision": (
            "Financial or lending services (ADMT significant decision)"
        ),
        "battery_label": (
            "Layer A/B/C as risk-assessment evidence for discrimination harms "
            "(not a mandated four-fifths/AIR legal test under CCPA ADMT)"
        ),
        "non_claims": (
            "Does not constitute CPPA certification or a California Attorney General "
            "compliance determination."
        ),
        "subsection_lines": [
            (
                "ADMT risk assessment cross-reference: see "
                "`admt_risk_assessment_summary.json` (Cal. Code Regs tit. 11 §7152 "
                "negative-impact categories — document-only template)."
            ),
            (
                "Pre-use notice checklist stub: document-only; consumer-facing notice "
                "text is out of scope for this validation-only demo."
            ),
        ],
        "federal_role": "Federal ECOA proxy-discrimination frame (OCC 2026-13 reporting)",
        "state_role": "CCPA/CPRA ADMT risk-assessment framing overlay",
    },
    "CO": {
        "state_authority": "Colorado SB 26-189 (effective 2027-01-01)",
        "artifact_name": "co_disclosure_checklist.json",
        "significant_decision": (
            "Consequential decision — financial or lending services"
        ),
        "battery_label": (
            "Layer A as optional existing-law outcomes support evidence; "
            "no statutory disparate-impact battery under SB 26-189"
        ),
        "non_claims": (
            "Does not satisfy Colorado Attorney General rules (pending January 2027) "
            "or constitute a CO AG compliance determination."
        ),
        "subsection_lines": [
            (
                "Post-adverse outcome plain-language description checklist: "
                "within 30 days (document stub)."
            ),
            "Human review on request: governance workflow stub (document-only).",
            "Record retention flag: 3 years.",
        ],
        "federal_role": "Federal ECOA proxy-discrimination frame (OCC 2026-13 reporting)",
        "state_role": "Colorado SB 26-189 disclosure / human-review overlay",
    },
}


@dataclass(slots=True)
class OverlayResult:
    """Overlay artifact + report/audit enrichment for an active state_overlay."""

    state_overlay: str
    state_authority: str
    artifact_name: str
    artifact_payload: dict[str, Any]
    regulatory_frames: list[dict[str, str]]
    overlay_non_claims: str
    overlay_subsection_lines: list[str]
    battery_label: str
    significant_decision: str


def resolve_state_overlay(
    *,
    state_overlay: str,
    run_id: str,
    bias_layers: dict[str, Any],
    layer_a_label: str,
    protected_attribute: str,
) -> OverlayResult | None:
    """Return overlay packaging when ``state_overlay`` is CA or CO; else ``None``.

    Unknown non-``none`` values raise ``ValueError`` so misconfigured demos fail loudly.
    """
    key = state_overlay.strip().upper() if state_overlay else "NONE"
    if key in {"", "NONE"}:
        return None
    if key not in OVERLAY_PROFILES:
        supported = ", ".join(sorted(OVERLAY_PROFILES))
        raise ValueError(
            f"Unsupported state_overlay={state_overlay!r}; "
            f"supported overlays: {supported}, or 'none'",
        )

    profile = OVERLAY_PROFILES[key]
    if key == "CA":
        artifact_payload = _build_admt_risk_assessment(
            run_id=run_id,
            state_authority=profile["state_authority"],
            bias_layers=bias_layers,
            layer_a_label=layer_a_label,
            protected_attribute=protected_attribute,
            non_claims=profile["non_claims"],
        )
    else:
        artifact_payload = _build_co_disclosure_checklist(
            run_id=run_id,
            state_authority=profile["state_authority"],
            non_claims=profile["non_claims"],
        )

    regulatory_frames = [
        {
            "frame": "Federal",
            "authority": "ECOA / Reg B (proxy_discrimination) + OCC 2026-13",
            "role": profile["federal_role"],
        },
        {
            "frame": key,
            "authority": profile["state_authority"],
            "role": profile["state_role"],
        },
    ]
    return OverlayResult(
        state_overlay=key,
        state_authority=profile["state_authority"],
        artifact_name=profile["artifact_name"],
        artifact_payload=artifact_payload,
        regulatory_frames=regulatory_frames,
        overlay_non_claims=profile["non_claims"],
        overlay_subsection_lines=list(profile["subsection_lines"]),
        battery_label=profile["battery_label"],
        significant_decision=profile["significant_decision"],
    )


def _build_admt_risk_assessment(
    *,
    run_id: str,
    state_authority: str,
    bias_layers: dict[str, Any],
    layer_a_label: str,
    protected_attribute: str,
    non_claims: str,
) -> dict[str, Any]:
    """Machine-readable ADMT risk-assessment summary for §7152 category evidence.

    Field list is self-designed: CPPA has not published a fixed export schema.
    Metrics are labeled as risk-assessment evidence, never as disparate-impact compliance.
    """
    layer_a = bias_layers["A"]
    layer_b = bias_layers["B"]
    layer_c = bias_layers["C"]
    return {
        "schema_version": "1.0",
        "artifact_kind": "admt_risk_assessment_summary",
        "run_id": run_id,
        "authority": state_authority,
        "significant_decision_category": "financial_or_lending_services",
        "admt_purpose": (
            "Credit decisioning support model under review; ADMT used to materially "
            "influence provision or denial of financial or lending services."
        ),
        "negative_impact_categories_considered": [
            "discrimination_on_protected_characteristics",
            "economic_harm_from_adverse_credit_decision",
            "reduced_access_to_financial_services",
        ],
        "discrimination_harms_evidence": {
            "protected_attribute": protected_attribute,
            "layer_a_label": layer_a_label,
            "layer_a": {
                "air": layer_a["air"],
                "selection_rate_gap": layer_a["selection_rate_gap"],
                "smd_score": layer_a["smd_score"],
            },
            "layer_b": {
                "fpr_parity_ratio": layer_b["fpr_parity_ratio"],
                "fnr_parity_ratio": layer_b["fnr_parity_ratio"],
            },
            "layer_c": {
                "auxiliary_classifier_auc": layer_c["auxiliary_classifier_auc"],
                "top_proxy_correlations": layer_c["top_proxy_correlations"],
            },
            "messaging": (
                "Statistical outputs are risk-assessment evidence for discrimination "
                "harms under CCPA ADMT §7152 — not a determination of disparate-impact "
                "compliance or ECOA liability."
            ),
        },
        "safeguards_documented": [
            {
                "safeguard": "hash_chained_audit_log",
                "status": "present",
                "notes": "FINOS mi-5 / mi-21 evidence chain for this validation run.",
            },
            {
                "safeguard": "protected_attribute_excluded_from_model_features",
                "status": "present",
                "notes": "sex reserved for validation; excluded from feature_names_in_.",
            },
            {
                "safeguard": "human_appeal_workflow",
                "status": "document_only_stub",
                "notes": "Consumer appeal / human overturn path not operated in this demo.",
            },
        ],
        "admt_bias_expert_consultation": "document_only_stub",
        "pre_use_notice": "document_only_stub",
        "non_claims": non_claims,
    }


def _build_co_disclosure_checklist(
    *,
    run_id: str,
    state_authority: str,
    non_claims: str,
) -> dict[str, Any]:
    """CO SB 26-189 disclosure checklist — no ADMT JSON and no DIA claim."""
    return {
        "schema_version": "1.0",
        "artifact_kind": "co_disclosure_checklist",
        "run_id": run_id,
        "authority": state_authority,
        "consequential_domain": "financial_or_lending",
        "disparate_impact_battery": False,
        "checklist": [
            {
                "item": "point_of_interaction_notice",
                "status": "document_stub",
                "notes": "Out of scope for validation-only demo.",
            },
            {
                "item": "post_adverse_outcome_notice",
                "status": "document_stub",
                "window_days": 30,
                "notes": (
                    "Plain-language description within 30 days; cross-check adverse-action "
                    "translator output when that module is enabled."
                ),
            },
            {
                "item": "human_review_on_request",
                "status": "document_stub",
                "notes": "Meaningful human review workflow stub only.",
            },
            {
                "item": "record_retention",
                "status": "flagged",
                "retention_years": 3,
                "notes": "3-year record retention flag for ADMT consequential decisions.",
            },
        ],
        "non_claims": non_claims,
    }
