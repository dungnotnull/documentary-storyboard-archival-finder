"""Tests for the canonical rights classifier."""
from __future__ import annotations

from rights_classifier import (
    LicenseCategory,
    RightsClarity,
    allowed_for_posture,
    classify,
)


def test_public_domain_clear():
    c = classify("public domain")
    assert c.license == LicenseCategory.PD
    assert c.clarity == RightsClarity.CLEAR


def test_cc_by_attribution_required():
    c = classify("CC BY 4.0")
    assert c.license == LicenseCategory.CC_BY
    assert c.clarity == RightsClarity.ATTRIBUTION_REQUIRED
    assert c.attribution_required is True


def test_unknown_is_unclear():
    c = classify("")
    assert c.license == LicenseCategory.UNKNOWN
    assert c.clarity == RightsClarity.UNCLEAR


def test_rights_managed_unclear():
    c = classify("Rights-Managed")
    assert c.clarity == RightsClarity.UNCLEAR


def test_fair_use_unclear():
    c = classify("fair use")
    assert c.license == LicenseCategory.FAIR_USE
    assert c.clarity == RightsClarity.UNCLEAR
    assert "legal review" in c.note.lower()


def test_allowed_for_public_domain_posture():
    c = classify("CC0")
    assert allowed_for_posture(c, "public-domain-cc-only") is True


def test_rights_managed_not_allowed_for_pd_posture():
    c = classify("Royalty-Free")
    assert allowed_for_posture(c, "public-domain-cc-only") is False
    assert allowed_for_posture(c, "licensed-budget") is True
