"""Scenario-level tests based on tests/test-scenarios.md."""
from __future__ import annotations

from rights_classifier import RightsClarity, classify
from scoring_engine import Asset, Shot, score_coherence, score_coverage, score_rights_clarity


def test_scenario_1_apollo_public_domain():
    """Apollo program short doc with public-domain requirement."""
    shots = [
        Shot("1.1", "Apollo 11 launch pad wide shot", True),
        Shot("1.2", "Astronaut on ladder", True),
    ]
    assets = [Asset("Public Domain", "Clear"), Asset("Public Domain", "Clear")]
    cov_score, _ = score_coverage(shots)
    rights_score, _ = score_rights_clarity(assets)
    coh_score, _ = score_coherence("expository", "three-act", "Apollo 11 united humanity")
    assert cov_score == 100
    assert rights_score == 100
    assert coh_score >= 90


def test_scenario_2_rights_unclear():
    c = classify("All rights reserved")
    assert c.clarity == RightsClarity.UNCLEAR


def test_scenario_3_fair_use():
    c = classify("fair use")
    assert c.clarity == RightsClarity.UNCLEAR
    assert "legal review" in c.note.lower()


def test_scenario_4_coverage_gap():
    shots = [Shot("2.1", "Private family dinner", False, False)]
    score, gaps = score_coverage(shots)
    assert score == 0
    assert len(gaps) == 1


def test_scenario_5_attribution_license():
    c = classify("CC BY 4.0")
    assert c.clarity == RightsClarity.ATTRIBUTION_REQUIRED
    assert c.attribution_required is True


def test_scenario_6_archive_offline():
    c = classify(None)
    assert c.clarity == RightsClarity.UNCLEAR
