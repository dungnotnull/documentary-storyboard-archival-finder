---
name: sub-evaluation-framework-selector
description: Selects the documentary mode (Nichols) and narrative structure model for the project. Shared across design-creative-media cluster.
---

## Purpose
Pick the storytelling approach that best serves the topic, length, and audience.

## Procedure
1. Choose a **documentary mode** from Bill Nichols' taxonomy:
   - **expository** - narrator/VO explains (best for short explainers, history).
   - **observational** - fly-on-the-wall, minimal intervention (events, process).
   - **participatory** - filmmaker engages subjects (interviews, travel).
   - **poetic** - mood/association over linear argument (artistic shorts).
   - **reflexive** - questions filmmaking itself (meta, experimental).
   - **performative** - personal/emotional experience.

2. Choose a **structure**:
   - **three-act** - setup, confrontation, resolution (classic narrative).
   - **quest/journey** - protagonist pursues a goal.
   - **story-circle** (Harmon) - character wants, leaves, adapts, returns changed.
   - **thesis-driven** - argument -> evidence -> conclusion.
   - **mosaic/collage** - thematic clusters, less linear.
   - **chronological** - event sequence.

3. Match mode + structure to topic, length, and audience. For example:
   - 10-min history explainer -> expository + three-act or thesis-driven.
   - character portrait -> participatory + quest/journey.
   - tone piece -> poetic + mosaic.

4. Justify the selection in 1-3 sentences.

## Outputs
Return:
```json
{
  "mode": "<expository|observational|participatory|poetic|reflexive|performative>",
  "structure": "<three-act|quest/journey|story-circle|thesis-driven|mosaic|chronological>",
  "justification": "...",
  "quality_gate": "Mode and structure model selected"
}
```

## Quality Gate
Mode and structure model selected.

## Shared Cluster Notes
This sub-skill is shared with design-creative-media clusters 104, 184, and 185. Keep the output schema stable; consuming clusters may extend allowed frameworks locally, but the core selector must always return `mode`, `structure`, `justification`, and `quality_gate`.
