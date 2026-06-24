# CLAUDE.md - Documentary Storyboard & Archival Footage Finder (Idea 227)

**Skill name:** `documentary-storyboard-archival-finder`
**Tagline:** Builds documentary storyboards/shot lists and locates rights-cleared archival footage from public archives to match the narrative.
**Cluster:** `design-creative-media`
**Source idea:** 227
**Current phase:** All phases implemented

## Problem This Skill Solves
Short-documentary makers spend enormous time structuring their story and sourcing archival footage with clear rights. This skill develops a documentary structure and storyboard/shot list, then searches public/national digital archives for matching archival footage and images, screening each for licensing/rights - outputting a storyboard mapped to sourced, rights-noted assets.

## Harness Flow Summary
1. **Intake** - `sub-requirements-gatherer` - topic, length, angle, target audience, story beats.
2. **Framework selection** - `sub-evaluation-framework-selector` - documentary structure model.
3. **Storyboard build** - `sub-storyboard-builder` - narrative arc -> scenes/shots/shot list.
4. **Archival finder + rights** - `sub-archival-finder` - search archives, screen rights/license.
5. **Scoring** - `sub-scoring-engine` - narrative coherence + footage-coverage + rights-clarity.
6. **Roadmap** - production/clearance plan.

## Sub-skills
- `sub-requirements-gatherer.md`
- `sub-evaluation-framework-selector.md`
- `sub-storyboard-builder.md`
- `sub-archival-finder.md`
- `sub-scoring-engine.md`

## Tools Required
WebSearch, WebFetch (public archives), Read, Write, Bash.

## Knowledge Sources
Documentary narrative theory (three-act, story circle); storyboarding/shot-list practice; public-domain & Creative Commons archives (Library of Congress, Internet Archive, national archives, Wikimedia, Pexels/Pixabay); copyright/fair-use basics.

## Supporting Tools
- `tools/knowledge_updater.py` - crawls documentary-craft + archive sources.
- `tools/archive_client.py` - machine queries for LoC, Internet Archive, Wikimedia Commons.
- `tools/rights_classifier.py` - canonical license classification and rights-clarity labels.
- `tools/scoring_engine.py` - deterministic scoring calculations.

## Active Development Tasks
- [x] Scaffold deliverables
- [x] Add public-archive source directory (`docs/archive-directory.md`)
- [x] Track license-type taxonomy (`SECOND-KNOWLEDGE-BRAIN.md`)
- [x] Implement production-grade Python tools and test suite

## Reference Docs
- `PROJECT-detail.md`
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md`
- `SECOND-KNOWLEDGE-BRAIN.md`
- `docs/archive-directory.md`
- `docs/cross-cluster-integration.md`
