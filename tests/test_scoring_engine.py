"""Tests for the deterministic scoring engine."""
from __future__ import annotations

from scoring_engine import Asset, Shot, score_coherence, score_coverage, score_rights_clarity


def test_coverage_full():
    shots = [Shot("1.1", "moon", True), Shot("1.2", "rocket", True)]
    score, gaps = score_coverage(shots)
    assert score == 100
    assert gaps == []


def test_coverage_partial_with_original_plan():
    shots = [Shot("1.1", "moon", True), Shot("1.2", "launch pad", False, True)]
    score, gaps = score_coverage(shots)
    assert score == 75
    assert gaps == []


def test_coverage_gap():
    shots = [Shot("1.1", "moon", True), Shot("1.2", "launch pad", False, False)]
    score, gaps = score_coverage(shots)
    assert score == 50
    assert "launch pad" in gaps[0]


def test_rights_clarity_all_clear():
    assets = [Asset("CC0", "Clear"), Asset("CC-BY", "Attribution-required")]
    score, risks = score_rights_clarity(assets)
    assert score == 100
    assert risks == []


def test_rights_clarity_unclear_flagged():
    assets = [Asset("CC0", "Clear"), Asset(None, "Unclear")]
    score, risks = score_rights_clarity(assets)
    assert score == 50
    assert len(risks) == 1


def test_rights_clarity_no_assets():
    score, risks = score_rights_clarity([])
    assert score == 0


def test_coherence_strong_match():
    score, rationale = score_coherence("expository", "three-act", "Apollo changed humanity")
    assert score >= 90


def test_coherence_missing_thesis():
    score, rationale = score_coherence("expository", "three-act", "")
    assert score == 0
