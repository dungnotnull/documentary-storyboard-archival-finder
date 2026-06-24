"""Rights classifier for archival assets.

Classifies license strings and rights fields into a canonical taxonomy,
determines attribution requirement, and returns a rights-clarity label.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LicenseCategory(str, Enum):
    PD = "PD"
    CC0 = "CC0"
    CC_BY = "CC-BY"
    CC_BY_SA = "CC-BY-SA"
    CC_BY_ND = "CC-BY-ND"
    CC_BY_NC = "CC-BY-NC"
    CC_BY_NC_SA = "CC-BY-NC-SA"
    CC_BY_NC_ND = "CC-BY-NC-ND"
    ROYALTY_FREE = "Royalty-Free"
    RIGHTS_MANAGED = "Rights-Managed"
    EDITORIAL_ONLY = "Editorial-Only"
    FAIR_USE = "Fair-Use"
    UNKNOWN = "Unknown"


class RightsClarity(str, Enum):
    CLEAR = "Clear"
    ATTRIBUTION_REQUIRED = "Attribution-required"
    UNCLEAR = "Unclear"


@dataclass(frozen=True)
class Classification:
    license: LicenseCategory
    attribution_required: bool
    share_alike_required: bool
    commercial_allowed: bool
    clarity: RightsClarity
    note: str


_LICENSE_PATTERNS: list[tuple[LicenseCategory, list[str]]] = [
    (LicenseCategory.CC0, ["cc0", "creative commons zero", "public domain dedication"]),
    (LicenseCategory.CC_BY, ["cc-by", "cc by", "creative commons attribution"]),
    (LicenseCategory.CC_BY_SA, ["cc-by-sa", "cc by-sa", "cc by sa", "creative commons attribution sharealike", "sharealike"]),
    (LicenseCategory.CC_BY_ND, ["cc-by-nd", "cc by-nd", "cc by nd", "no derivatives"]),
    (LicenseCategory.CC_BY_NC, ["cc-by-nc", "cc by-nc", "cc by nc", "non-commercial", "noncommercial"]),
    (LicenseCategory.CC_BY_NC_SA, ["cc-by-nc-sa", "cc by-nc-sa"]),
    (LicenseCategory.CC_BY_NC_ND, ["cc-by-nc-nd", "cc by-nc-nd"]),
    (LicenseCategory.PD, ["public domain", "pd", "no known restrictions", "no copyright"]),
    (LicenseCategory.ROYALTY_FREE, ["royalty-free", "royalty free"]),
    (LicenseCategory.RIGHTS_MANAGED, ["rights-managed", "rights managed"]),
    (LicenseCategory.EDITORIAL_ONLY, ["editorial only", "editorial use only", "editorial-only"]),
    (LicenseCategory.FAIR_USE, ["fair use", "fairuse"]),
]


def classify(license_text: str | None) -> Classification:
    """Classify a raw license string.

    Returns conservative defaults for empty or ambiguous input.
    """
    if not license_text:
        return Classification(
            license=LicenseCategory.UNKNOWN,
            attribution_required=False,
            share_alike_required=False,
            commercial_allowed=False,
            clarity=RightsClarity.UNCLEAR,
            note="No license information provided; do not use without clearance.",
        )
    text = license_text.lower()
    for category, patterns in _LICENSE_PATTERNS:
        if any(pattern in text for pattern in patterns):
            return _classification_for(category)
    return Classification(
        license=LicenseCategory.UNKNOWN,
        attribution_required=False,
        share_alike_required=False,
        commercial_allowed=False,
        clarity=RightsClarity.UNCLEAR,
        note=f"License text '{license_text[:80]}' could not be classified; do not use without clearance.",
    )


def _classification_for(category: LicenseCategory) -> Classification:
    notes: dict[LicenseCategory, str] = {
        LicenseCategory.PD: "Public domain; verify jurisdiction and source before use.",
        LicenseCategory.CC0: "CC0; free to use without attribution, but provenance should still be recorded.",
        LicenseCategory.CC_BY: "CC-BY; attribution required.",
        LicenseCategory.CC_BY_SA: "CC-BY-SA; attribution and share-alike required.",
        LicenseCategory.CC_BY_ND: "CC-BY-ND; attribution required; no derivative works.",
        LicenseCategory.CC_BY_NC: "CC-BY-NC; attribution required; non-commercial only.",
        LicenseCategory.CC_BY_NC_SA: "CC-BY-NC-SA; attribution, non-commercial, share-alike required.",
        LicenseCategory.CC_BY_NC_ND: "CC-BY-NC-ND; attribution, non-commercial, no derivatives.",
        LicenseCategory.ROYALTY_FREE: "Royalty-free license; read provider terms for any remaining restrictions.",
        LicenseCategory.RIGHTS_MANAGED: "Rights-managed; requires license negotiation before use.",
        LicenseCategory.EDITORIAL_ONLY: "Editorial-only; not for commercial promotion or product use.",
        LicenseCategory.FAIR_USE: "Fair use is a fact-specific legal defense, not a license; legal review required.",
    }
    note = notes.get(category, "License recognized; review provider terms.")
    attr = category in {
        LicenseCategory.CC_BY,
        LicenseCategory.CC_BY_SA,
        LicenseCategory.CC_BY_ND,
        LicenseCategory.CC_BY_NC,
        LicenseCategory.CC_BY_NC_SA,
        LicenseCategory.CC_BY_NC_ND,
    }
    sa = category in {LicenseCategory.CC_BY_SA, LicenseCategory.CC_BY_NC_SA}
    commercial = category not in {
        LicenseCategory.CC_BY_NC,
        LicenseCategory.CC_BY_NC_SA,
        LicenseCategory.CC_BY_NC_ND,
        LicenseCategory.EDITORIAL_ONLY,
    }
    if category == LicenseCategory.UNKNOWN:
        clarity = RightsClarity.UNCLEAR
    elif attr:
        clarity = RightsClarity.ATTRIBUTION_REQUIRED
    else:
        clarity = RightsClarity.CLEAR
    if category in {LicenseCategory.RIGHTS_MANAGED, LicenseCategory.EDITORIAL_ONLY, LicenseCategory.FAIR_USE}:
        clarity = RightsClarity.UNCLEAR
        note += " Do not use without clearance."
    return Classification(
        license=category,
        attribution_required=attr,
        share_alike_required=sa,
        commercial_allowed=commercial,
        clarity=clarity,
        note=note,
    )


def allowed_for_posture(classification: Classification, posture: str) -> bool:
    """Check whether a classification is allowed under a rights posture.

    posture values:
      - public-domain-cc-only: only PD, CC0, and CC variants
      - licensed-budget: PD/CC + RF/RM/Editorial allowed but flagged
      - unknown: conservative default (same as public-domain-cc-only)
    """
    posture = (posture or "unknown").lower().strip()
    if posture == "licensed-budget":
        return classification.license != LicenseCategory.UNKNOWN
    return classification.license in {
        LicenseCategory.PD,
        LicenseCategory.CC0,
        LicenseCategory.CC_BY,
        LicenseCategory.CC_BY_SA,
        LicenseCategory.CC_BY_ND,
        LicenseCategory.CC_BY_NC,
        LicenseCategory.CC_BY_NC_SA,
        LicenseCategory.CC_BY_NC_ND,
    }
