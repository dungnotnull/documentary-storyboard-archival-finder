# PROJECT-detail.md - Documentary Storyboard & Archival Footage Finder

## Executive Summary
A harness for documentary filmmakers that (1) structures a story and produces a storyboard/shot list grounded in narrative theory, and (2) locates matching archival footage/images from public and Creative Commons archives, screening each asset for licensing/rights. Output maps each storyboard beat to candidate, rights-noted assets plus a clearance plan.

## Problem Statement
Short-doc makers, especially indie/educational, struggle to structure their narrative and to find usable footage without rights headaches. Using improperly licensed material risks takedowns and legal exposure.

## Target Users & Use Cases
- **Indie documentarian** - "Storyboard a 10-min doc on the Apollo program + find public-domain footage." - storyboard + sourced clips.
- **Educator** - "B-roll for a history lesson, all reusable." - CC/public-domain assets.
- **YouTuber** - "Structure my explainer + archival images." - shot list + image sources.
- **Producer** - "Rights status of these clips?" - license screen.
- **Editor** - "Shot list mapped to assets." - production-ready board.

## Harness Architecture
```
/documentary-storyboard-archival-finder
  Stage 1 Intake     - sub-requirements-gatherer        - topic/length/angle
  Stage 2 Framework  - sub-evaluation-framework-selector - structure model
  Stage 3 Storyboard - sub-storyboard-builder           - scenes/shots/shot list
  Stage 4 Archival   - sub-archival-finder              - assets + rights screen
  Stage 5 Scoring    - sub-scoring-engine               - coherence/coverage/rights
  Stage 6 Roadmap    - production + clearance plan
```

## Full Sub-Skill Catalog
| Sub-skill | Purpose | Inputs | Outputs | Tools | Quality gate |
|---|---|---|---|---|---|
| requirements-gatherer | Brief | user | topic/length | Read | Topic + length + angle |
| framework-selector | Structure | brief | model | WebSearch | Structure chosen |
| storyboard-builder | Board | brief | scenes/shots | - | Arc + shot list complete |
| archival-finder | Source | shot list | assets + rights | WebFetch | License noted per asset |
| scoring-engine | Score | all | scores | - | Coverage + rights clarity |

## E2E Execution Flow
Intake -> framework -> storyboard -> archival search + rights screen -> score -> roadmap. Fallback to cached archive directory if web down. Error: asset rights unclear -> mark "rights unverified - do not use without clearance."

## SECOND-KNOWLEDGE-BRAIN Integration
`knowledge_updater.py` crawls documentary-craft + archive sources; dated append.

## Quality Gates
- Storyboard follows a named structure with a shot list.
- Each archival asset has a noted license/rights status + source.
- Unclear rights flagged "do not use without clearance."
- Fair-use suggestions are cautious and flagged as needing legal review.
- Coverage gaps (beats lacking footage) identified.

## Test Scenarios
See `tests/test-scenarios.md` (6 scenarios) and the executable suite in `tests/`.

## Key Design Decisions
1. Rights status mandatory per asset; default to caution.
2. Public-domain / CC sources prioritized over ambiguous.
3. Narrative structure precedes footage hunting.
4. Fair use flagged as legal-review-required, never asserted.
5. Coverage gaps surfaced so the maker can plan original B-roll.

## Cross-Cluster Sharing
The framework-selector and scoring-engine sub-skills are shared with design-creative-media clusters 104, 184, and 185. See `docs/cross-cluster-integration.md` for contracts and maintainer notes.
