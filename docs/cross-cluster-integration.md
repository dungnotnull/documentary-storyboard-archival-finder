# Cross-Cluster Integration - Design-Creative-Media

Idea 227 shares two sub-skills with other clusters in the design-creative-media family to avoid duplication and keep evaluation consistent.

## Shared sub-skills

### sub-evaluation-framework-selector
- Shared with clusters 104, 184, 185.
- Purpose: selects the creative evaluation framework (documentary mode, narrative structure, design criteria).
- Shared behavior: always returns a named framework, a one-line justification, and a quality gate.
- Cluster-specific override: each cluster may extend the list of allowed frameworks in its own main harness; the sub-skill core must remain framework-agnostic except for the documentary mode taxonomy documented here.

### sub-scoring-engine
- Shared with clusters 104, 184, 185.
- Purpose: scores a creative artifact on standardized dimensions.
- Shared dimensions: coherence, coverage, rights clarity.
- Cluster-specific dimensions: clusters may add their own dimensions (e.g., visual style, technical feasibility) downstream; the engine must allow extra dimensions via the `extra_dimensions` input.

## Integration contracts

### sub-evaluation-framework-selector output schema
```json
{
  "mode": "<documentary mode or design mode>",
  "structure": "<structure model>",
  "justification": "<1-3 sentences>",
  "quality_gate": "<specific pass condition>"
}
```

### sub-scoring-engine input/output schema
Input:
```json
{
  "dimensions": ["coherence", "coverage", "rights_clarity"],
  "storyboard": { "...": "..." },
  "assets": [ "..." ],
  "extra_dimensions": { "visual_style": { "weight": 0.2 } }
}
```
Output:
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

## Consuming clusters

| Cluster | Shared sub-skill | How it is used |
|---|---|---|
| 104 | framework-selector, scoring-engine | Creative concept evaluation / pitch scoring |
| 184 | framework-selector, scoring-engine | Media asset / visual project scoring |
| 185 | framework-selector, scoring-engine | Narrative / storytelling scoring |

## Maintainer notes
- Do not rename these sub-skill files without updating references in clusters 104, 184, 185.
- When adding a new shared dimension to sub-scoring-engine, bump the minor version in the front matter and notify cluster maintainers.
- Keep rights-clarity logic in sync with the `tools/rights_classifier.py` module so that all clusters classify licenses consistently.
