---
name: sub-scoring-engine
description: Scores the documentary plan on narrative coherence, footage coverage, and rights clarity. Shared across design-creative-media cluster.
---

## Purpose
Assess readiness for production and surface risks before the maker commits to a cut.

## Procedure
1. **Coherence** (0-100): Does the storyboard tell a clear, well-paced story per the chosen mode and structure?
   - 90-100: strong arc, clear thesis, pacing fits length.
   - 70-89: good arc, minor pacing/transition issues.
   - 50-69: arc present but thin or disjointed.
   - 0-49: unclear arc or mismatched mode/structure.

2. **Coverage** (0-100): Share of shots with a sourced asset vs. gaps.
   - Score = round(100 * (shots_with_asset / total_shots)).
   - If a gap has a viable original-production plan, count as 0.5 coverage.
   - Flag beats with zero coverage.

3. **Rights clarity** (0-100): Share of assets with clear/usable licenses.
   - Clear or Attribution-required = usable.
   - Unclear = not usable.
   - Score = round(100 * (usable_assets / total_assets)).
   - If no assets, score = 0 and flag.

4. Record rights-risk flags for any `Unclear` asset or fair-use request.

5. Allow clusters to add dimensions via `extra_dimensions` input.

## Outputs
Scorecard:
```markdown
| Dimension | Score | Rationale |
|---|---|---|
| coherence | 0-100 | ... |
| coverage | 0-100 | ... |
| rights_clarity | 0-100 | ... |
```

Rights-risk flags:
```markdown
- Risk: <description> | Mitigation: <action>
```

JSON-like output:
```json
{
  "scores": {
    "coherence": { "score": 0, "rationale": "..." },
    "coverage": { "score": 0, "rationale": "..." },
    "rights_clarity": { "score": 0, "rationale": "..." }
  },
  "rights_risks": ["..."],
  "coverage_gaps": ["..."]
}
```

## Quality Gate
Coverage + rights clarity scored; rights risks flagged; all scores have rationale.

## Shared Cluster Notes
This sub-skill is shared with clusters 104, 184, and 185. The dimensions `coherence`, `coverage`, and `rights_clarity` are stable. Downstream clusters may inject additional dimensions through `extra_dimensions`; this engine must include them in the scorecard without changing the core schema.
