"""Scoring engine for documentary storyboard + archival plans.

Implements the scoring rubric from skills/sub-scoring-engine.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Shot:
    shot_id: str
    required_visual: str
    has_asset: bool = False
    has_original_plan: bool = False


@dataclass
class Asset:
    license_text: str | None
    rights_clarity: str = "Unclear"


@dataclass
class Scorecard:
    coherence: int = 0
    coherence_rationale: str = ""
    coverage: int = 0
    coverage_rationale: str = ""
    rights_clarity: int = 0
    rights_clarity_rationale: str = ""
    rights_risks: list[str] = field(default_factory=list)
    coverage_gaps: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "scores": {
                "coherence": {"score": self.coherence, "rationale": self.coherence_rationale},
                "coverage": {"score": self.coverage, "rationale": self.coverage_rationale},
                "rights_clarity": {
                    "score": self.rights_clarity,
                    "rationale": self.rights_clarity_rationale,
                },
            },
            "rights_risks": self.rights_risks,
            "coverage_gaps": self.coverage_gaps,
        }


def score_coverage(shots: list[Shot]) -> tuple[int, list[str]]:
    if not shots:
        return 0, ["No shots defined."]
    covered = sum(1 for s in shots if s.has_asset)
    partial = sum(0.5 for s in shots if not s.has_asset and s.has_original_plan)
    score = min(100, int(round(100 * (covered + partial) / len(shots))))
    gaps = [
        f"Shot {s.shot_id} ({s.required_visual}) lacks an asset and original plan"
        for s in shots
        if not s.has_asset and not s.has_original_plan
    ]
    return score, gaps


def score_rights_clarity(assets: list[Asset]) -> tuple[int, list[str]]:
    if not assets:
        return 0, ["No assets to evaluate."]
    usable = sum(1 for a in assets if a.rights_clarity in ("Clear", "Attribution-required"))
    score = int(round(100 * usable / len(assets)))
    risks = [
        f"Asset with license '{a.license_text}' is unclear - do not use without clearance."
        for a in assets
        if a.rights_clarity not in ("Clear", "Attribution-required")
    ]
    return score, risks


def score_coherence(mode: str, structure: str, thesis: str | None) -> tuple[int, str]:
    if not thesis or not mode or not structure:
        return 0, "Missing thesis, mode, or structure."
    viable_structures = (
        "three-act",
        "thesis-driven",
        "quest/journey",
        "story-circle",
    )
    if mode.lower() in ("expository", "participatory", "observational") and structure.lower() in viable_structures:
        return 90, f"Strong match between {mode} mode and {structure} structure."
    return 70, f"Mode {mode} and structure {structure} are viable but verify pacing."
