# PROJECT-DEVELOPMENT-PHASE-TRACKING - Idea 227

## Phase 0 - Research & Architecture
**Goal:** Codify doc structure, storyboarding, archive directory, rights basics.
**Deliverables:** CLAUDE.md, PROJECT-detail.md, SECOND-KNOWLEDGE-BRAIN.md, docs/archive-directory.md.
**Success:** Frameworks anchored.

- [x] Finalize CLAUDE.md harness overview and active task list
- [x] Finalize PROJECT-detail.md architecture and quality gates
- [x] Expand SECOND-KNOWLEDGE-BRAIN.md with license-type taxonomy
- [x] Add canonical public-archive source directory (`docs/archive-directory.md`)
- [x] Reference archive directory and taxonomy from all relevant docs

## Phase 1 - Core Sub-Skills
**Goal:** Build requirements-gatherer, storyboard-builder, archival-finder sub-skills.
**Deliverables:** 3 production-grade sub-skills.
**Success:** Sample doc storyboard + assets can be produced.

- [x] Rewrite `skills/sub-requirements-gatherer.md` with JSON output, rights-posture mapping, and quality gate
- [x] Rewrite `skills/sub-storyboard-builder.md` with shot-type taxonomy, A/B-roll definitions, JSON output, and quality gate
- [x] Rewrite `skills/sub-archival-finder.md` with archive query strategy, license classification, fallback rules, and gap detection

## Phase 2 - Main Harness + Gates
**Goal:** Wire stages, framework-selector, scoring-engine; enforce rights gate.
**Deliverables:** `skills/main.md` + 2 sub-skills.
**Success:** End-to-end board.

- [x] Rewrite `skills/main.md` as full orchestrator with stage-by-stage context passing, output format, and hard rights gate
- [x] Rewrite `skills/sub-evaluation-framework-selector.md` with Nichols modes, structure models, justification, and shared-cluster notes
- [x] Rewrite `skills/sub-scoring-engine.md` with 0-100 rubric, rights-risk flags, and shared-cluster notes
- [x] Add `tools/rights_classifier.py` for canonical license classification
- [x] Add `tools/scoring_engine.py` implementing the rubric in code

## Phase 3 - Knowledge Pipeline
**Goal:** Real `knowledge_updater.py` that crawls sources and appends deduped entries.
**Deliverables:** Production tool.
**Success:** Dedup append works.

- [x] Implement `tools/archive_client.py` with LoC, Internet Archive, Wikimedia machine queries
- [x] Replace dummy `fetch_entries()` in `tools/knowledge_updater.py` with real archive + web-search providers, CLI, and dry-run support
- [x] Add `tools/__init__.py` so tools form a proper package
- [x] Wire `rights_classifier` into knowledge pipeline
- [x] Add `pyproject.toml` with dependencies, scripts, and pytest config

## Phase 4 - Testing
**Goal:** 5+ scenarios incl. rights-unclear and coverage gap.
**Deliverables:** Executable tests.
**Success:** Green.

- [x] Create `tests/conftest.py` for import paths
- [x] Create `tests/test_rights_classifier.py` covering PD, CC-BY, unknown, fair use, posture checks
- [x] Create `tests/test_knowledge_updater.py` covering hash, dedup, append, dry-run
- [x] Create `tests/test_archive_client.py` covering title/link extraction and archive JSON parsing
- [x] Create `tests/test_scoring_engine.py` covering coherence, coverage, rights clarity
- [x] Create `tests/test_scenarios.py` mapping the six scenario tests
- [x] Create `tests/test_skills.py` validating skill front matter and required sections
- [x] Run full test suite and confirm green

## Phase 5 - Integration
**Goal:** Share scoring-engine/framework-selector with design cluster (104, 184, 185).
**Deliverables:** Cross-links.
**Success:** Clusters can consume shared sub-skills.

- [x] Create `docs/cross-cluster-integration.md` with shared sub-skill contracts and cluster matrix
- [x] Update `skills/sub-evaluation-framework-selector.md` to document shared usage
- [x] Update `skills/sub-scoring-engine.md` to document shared usage and `extra_dimensions` extension point
- [x] Add README.md and CONTRIBUTING.md for open-source onboarding
- [x] Add `.gitignore` for Python artifacts
- [x] Add `LICENSE` (MIT) for open-source distribution
