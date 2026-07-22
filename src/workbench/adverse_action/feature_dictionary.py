"""Business-language feature dictionary for German Credit adverse-action reasons.

Codes follow the UCI Statlog (German Credit) attribute documentation. Descriptions
are written to be specific and consumer-understandable per Reg B Sec 1002.9 and
the Circular 2023-03 insufficiency examples (never a generic checklist bucket).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

FEATURE_BUSINESS_NAMES: dict[str, str] = {
    "checking_status": "checking account status",
    "credit_history": "credit history",
    "purpose": "loan purpose",
    "savings_status": "savings account balance",
    "employment": "length of present employment",
    "other_parties": "other debtors or guarantors",
    "property_magnitude": "property ownership",
    "other_payment_plans": "other installment plans",
    "housing": "housing status",
    "job": "job/occupation category",
    "own_telephone": "registered telephone",
    "foreign_worker": "foreign-worker status",
    "duration": "requested loan duration",
    "credit_amount": "requested credit amount",
    "installment_commitment": "installment rate (% of disposable income)",
    "residence_since": "years at present residence",
    "age": "applicant age",
    "existing_credits": "number of existing credits at this bank",
    "num_dependents": "number of dependents",
}

CATEGORICAL_LEVEL_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "checking_status": {
        "A11": "checking account balance below 0 DM",
        "A12": "checking account balance between 0 and 200 DM",
        "A13": "checking account balance at or above 200 DM (or salary assignment >= 1 year)",
        "A14": "no checking account on file",
    },
    "credit_history": {
        "A30": "no credits taken, or all credits paid back duly",
        "A31": "all credits at this bank paid back duly",
        "A32": "existing credits paid back duly to date",
        "A33": "past delay in paying off existing credit(s)",
        "A34": "critical account, or credits existing at other institutions",
    },
    "purpose": {
        "A40": "loan purpose: new car",
        "A41": "loan purpose: used car",
        "A42": "loan purpose: furniture/equipment",
        "A43": "loan purpose: radio/television",
        "A44": "loan purpose: domestic appliances",
        "A45": "loan purpose: repairs",
        "A46": "loan purpose: education",
        "A47": "loan purpose: vacation",
        "A48": "loan purpose: retraining",
        "A49": "loan purpose: business",
        "A410": "loan purpose: other",
    },
    "savings_status": {
        "A61": "savings account balance below 100 DM",
        "A62": "savings account balance between 100 and 500 DM",
        "A63": "savings account balance between 500 and 1,000 DM",
        "A64": "savings account balance at or above 1,000 DM",
        "A65": "no savings account, or savings account status unknown",
    },
    "employment": {
        "A71": "currently unemployed",
        "A72": "present employment length under 1 year",
        "A73": "present employment length between 1 and 4 years",
        "A74": "present employment length between 4 and 7 years",
        "A75": "present employment length at or above 7 years",
    },
    "other_parties": {
        "A101": "no other debtors or guarantors on the application",
        "A102": "application includes a co-applicant",
        "A103": "application includes a guarantor",
    },
    "property_magnitude": {
        "A121": "real estate listed as property",
        "A122": "building-society savings agreement or life insurance listed as property",
        "A123": "car or other non-real-estate property listed",
        "A124": "no property on file, or property status unknown",
    },
    "other_payment_plans": {
        "A141": "other installment plan(s) held at a bank",
        "A142": "other installment plan(s) held at a store/retailer",
        "A143": "no other installment plans",
    },
    "housing": {
        "A151": "rents current residence",
        "A152": "owns current residence",
        "A153": "lives in residence provided free of charge",
    },
    "job": {
        "A171": "unemployed or unskilled, non-resident",
        "A172": "unskilled, resident",
        "A173": "skilled employee or official",
        "A174": "management, self-employed, or highly qualified/officer role",
    },
    "own_telephone": {
        "A191": "no telephone registered under applicant's name",
        "A192": "telephone registered under applicant's name",
    },
    "foreign_worker": {
        "A201": "foreign-worker status: yes",
        "A202": "foreign-worker status: no",
    },
}

NUMERIC_DESCRIPTION_TEMPLATES: dict[str, str] = {
    "duration": "requested loan duration of {value:.0f} months",
    "credit_amount": "requested credit amount of {value:,.0f} DM",
    "installment_commitment": "installment rate of {value:.0f}% of disposable income",
    "residence_since": "{value:.0f} years at present residence",
    "age": "applicant age of {value:.0f} years",
    "existing_credits": "{value:.0f} existing credit(s) at this bank",
    "num_dependents": "{value:.0f} dependent(s)",
}


@dataclass(slots=True)
class MappingRuleEntry:
    feature: str
    business_definition: str
    factor_description_template: str
    specificity_test: str


def describe_factor(feature: str, applicant_row: Any) -> str:
    """Render a specific, consumer-understandable factor description.

    Uses the applicant's actual recorded value so the reason names the scored
    factor (Reg B Sec 1002.9), never a generic checklist bucket.
    """
    if feature in CATEGORICAL_LEVEL_DESCRIPTIONS:
        code = str(applicant_row[feature])
        levels = CATEGORICAL_LEVEL_DESCRIPTIONS[feature]
        if code in levels:
            return levels[code]
        return f"{FEATURE_BUSINESS_NAMES.get(feature, feature)}: {code}"
    template = NUMERIC_DESCRIPTION_TEMPLATES.get(feature)
    value = applicant_row[feature]
    if template is not None:
        return template.format(value=float(value))
    return f"{FEATURE_BUSINESS_NAMES.get(feature, feature)}: {value}"


def is_mapped_specifically(feature: str, applicant_row: Any) -> bool:
    """True if the applicant's value maps to a codebook-specific description.

    Backs the automated sample-audit proxy: a factor description is treated as
    satisfying the specificity test (Circular 2023-03 insufficiency examples)
    only when it comes from a known category level or numeric template, not
    the generic `"<name>: <raw code>"` fallback.
    """
    if feature in CATEGORICAL_LEVEL_DESCRIPTIONS:
        return str(applicant_row[feature]) in CATEGORICAL_LEVEL_DESCRIPTIONS[feature]
    return feature in NUMERIC_DESCRIPTION_TEMPLATES


def mapping_rule_catalog() -> list[MappingRuleEntry]:
    """Static, versioned mapping-rule inventory for the methodology artifact.

    One entry per raw (pre-encoding) model feature — the level of disclosure
    used in adverse-action reasons — documenting the description logic applied
    at translation time. All entries pass the specificity test by construction:
    every level/value maps to a scored-factor-specific phrase, never a
    generic checklist code (Circular 2023-03 insufficiency examples).
    """
    entries: list[MappingRuleEntry] = []
    for feature, business_definition in FEATURE_BUSINESS_NAMES.items():
        if feature in CATEGORICAL_LEVEL_DESCRIPTIONS:
            sample_levels = ", ".join(sorted(CATEGORICAL_LEVEL_DESCRIPTIONS[feature].values()))
            template = f"One of: {sample_levels}."
        else:
            template = NUMERIC_DESCRIPTION_TEMPLATES[feature]
        entries.append(
            MappingRuleEntry(
                feature=feature,
                business_definition=business_definition,
                factor_description_template=template,
                specificity_test="pass",
            ),
        )
    return entries


MAPPING_RULES: list[str] = [
    "Never map to a checklist code unless the code accurately describes the scored variable "
    "(Circular 2023-03 insufficiency examples).",
    "Disclose the actual data source and value considered (e.g., checking-account balance "
    "band, employment-length band) rather than a broad category.",
    "For one-hot encoded categorical features, aggregate SHAP contributions to the parent "
    "raw feature before generating the consumer-facing reason; disclose the applicant's "
    "actual recorded level, not the encoded column name.",
    "Non-intuitive ML relationships are permitted per Reg B Official Interpretation "
    "(12 CFR 1002, comment 9(b)(2)-4); the factor need not explain the full "
    "creditworthiness relationship, only identify the scored factor.",
]

KNOWN_LIMITATIONS: list[str] = [
    "Attribution is computed on the UCI German Credit demo population; it does not "
    "represent US lending populations or a production adverse-action pipeline.",
    "Applicant age is a model input in this demo fixture. In US ECOA lending, age is a "
    "protected basis (15 U.S.C. Sec 1691(a)(1); Reg B Sec 1002.6(b)(2)); a production "
    "deployment would require age-specific adverse-action handling not implemented here.",
    "Perturbation-fidelity and rank-stability tests are automated proxies over the frozen "
    "validation fixture; they do not replace a human fair-lending reviewer's sign-off.",
    "Sample-audit is an automated specificity-proxy check, not the human review of "
    "adverse decisions described in Circular 2022-03 practice; human review sign-off is "
    "deferred to a governance workflow outside this demo.",
]
