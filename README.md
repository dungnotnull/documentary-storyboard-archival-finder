<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/tests-38%2F38-brightgreen.svg" alt="Tests 38/38">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/cluster-design--creative--media-purple.svg" alt="Cluster">
</p>

<h1 align="center">Documentary Storyboard &amp; Archival Footage Finder</h1>
<p align="center"><em>Idea 227 — A production-grade Claude skill harness that turns a documentary idea into a rights-cleared, production-ready storyboard.</em></p>

---

## Table of Contents

1. [Why this exists](#why-this-exists)
2. [What you get](#what-you-get)
3. [Harness architecture](#harness-architecture)
4. [Quick start](#quick-start)
5. [Repository layout](#repository-layout)
6. [Rights &amp; licensing model](#rights--licensing-model)
7. [Public archive directory](#public-archive-directory)
8. [Knowledge pipeline](#knowledge-pipeline)
9. [Testing](#testing)
10. [Cross-cluster sharing](#cross-cluster-sharing)
11. [Roadmap &amp; contributing](#roadmap--contributing)
12. [License](#license)

---

## Why this exists

Independent documentarians, educators, and YouTube creators spend **hours** on two painful problems:

1. **Structuring the story** - turning a topic into a coherent narrative arc with a shot list.
2. **Finding usable archival footage** - hunting through public archives, then figuring out whether each clip can legally be used.

Using material without clear rights exposes a project to takedowns, demonetization, and legal risk. This harness solves both problems end-to-end by combining documentary narrative theory with a rights-first archival research workflow.

### Target users

| User | Need | How this helps |
|---|---|---|
| **Indie documentarian** | "Storyboard a 10-min Apollo program doc + find public-domain footage." | Returns a mode, structure, shot list, and sourced clips. |
| **Educator** | "B-roll for a history lesson, all reusable." | Prioritizes CC0 / CC-BY / public-domain assets. |
| **YouTuber** | "Structure my explainer + archival images." | Builds shot list with exact image sources. |
| **Producer** | "Rights status of these clips?" | Flags unclear/rights-managed/fair-use material. |
| **Editor** | "Shot list mapped to assets." | Produces a production board with beat-by-beat asset mapping. |

---

## What you get

A complete **Documentary Storyboard &amp; Archival Plan** with six sections:

1. **Brief** - topic, thesis/angle, length, platform, audience, rights posture
2. **Mode &amp; Structure** - Nichols documentary mode + narrative structure model
3. **Storyboard / Shot List** - scene-by-scene shots with type, A/B-roll, required visuals, sourcing plan
4. **Archival Assets** - per-beat asset table: source, exact URL, license, attribution, rights clarity, access date
5. **Scorecard** - narrative coherence, footage coverage, rights clarity (0-100 each)
6. **Coverage Gaps &amp; Clearance Plan** - original B-roll needs, legal-review triggers, timeline

---

## Harness architecture

```
Stage 1 Intake      → sub-requirements-gatherer         → brief + rights posture
Stage 2 Framework   → sub-evaluation-framework-selector → mode + structure
Stage 3 Storyboard  → sub-storyboard-builder            → scenes / shots / required visuals
Stage 4 Archival     → sub-archival-finder               → assets + rights screen
Stage 5 Scoring      → sub-scoring-engine                → coherence / coverage / rights clarity
Stage 6 Roadmap      → production + clearance plan
```

The harness is intentionally **rights-first**: every candidate asset must carry a license and a rights-clarity label before it can be presented as usable. Unclear material is flagged **"do not use without clearance."** Fair use is never asserted; it is always flagged for legal review.

---

## Quick start

### As a Claude agent

Load `skills/main.md` and follow the stage-by-stage harness flow. The orchestrator will call the sub-skills in order and enforce the quality gates.

### As a developer

```bash
# Clone
git clone https://github.com/dungnotnull/documentary-storyboard-archival-finder.git
cd documentary-storyboard-archival-finder

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run the full test suite
pytest tests/ -v

# Update the knowledge brain (dry-run first)
python tools/knowledge_updater.py --dry-run
```

### Minimal programmatic example

```python
from tools.archive_client import search_all
from tools.rights_classifier import classify, allowed_for_posture
from tools.scoring_engine import Shot, score_coverage

# Find candidate archival assets for "Apollo 11"
entries = search_all("Apollo 11", max_results=5)
for e in entries:
    print(e["source"], e["url"], classify(e.get("license", "")).license.value)

# Score coverage of a shot list
shots = [
    Shot("1.1", "Apollo 11 launch pad", has_asset=True),
    Shot("1.2", "Astronaut on ladder", has_asset=False, has_original_plan=True),
]
score, gaps = score_coverage(shots)
print(f"Coverage: {score}%")
```

---

## Repository layout

```
documentary-storyboard-archival-finder/
├── skills/
│   ├── main.md                              # Orchestrator
│   ├── sub-requirements-gatherer.md         # Brief capture
│   ├── sub-evaluation-framework-selector.md # Mode + structure
│   ├── sub-storyboard-builder.md            # Shot list
│   ├── sub-archival-finder.md               # Asset search + rights
│   └── sub-scoring-engine.md                # 0-100 scorecard
├── tools/
│   ├── archive_client.py                    # LoC / Internet Archive / Wikimedia queries
│   ├── rights_classifier.py                 # Canonical license taxonomy
│   ├── scoring_engine.py                    # Deterministic scoring
│   └── knowledge_updater.py                 # Brain crawler + CLI
├── tests/
│   ├── test_archive_client.py
│   ├── test_rights_classifier.py
│   ├── test_knowledge_updater.py
│   ├── test_scoring_engine.py
│   ├── test_scenarios.py                    # The 6 user scenarios
│   └── test_skills.py                       # Skill markdown validation
├── docs/
│   ├── archive-directory.md                 # Authoritative public archive catalog
│   ├── cross-cluster-integration.md         # 104 / 184 / 185 sharing contracts
│   └── CONTRIBUTING.md
├── SECOND-KNOWLEDGE-BRAIN.md                # Living knowledge base
├── PROJECT-detail.md                        # Project specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md    # Phase tracker (100% done)
├── pyproject.toml                           # Package metadata + pytest config
├── README.md                                # This file
└── LICENSE                                  # MIT
```

---

## Rights &amp; licensing model

The harness classifies every asset through a **canonical license taxonomy**:

| License | Use | Attribution | Commercial | Rights clarity |
|---|---|---|---|---|
| Public Domain (PD) | Yes | No | Yes | Clear |
| CC0 | Yes | Appreciated | Yes | Clear |
| CC BY | Yes | Required | Yes | Attribution-required |
| CC BY-SA | Yes | Required | Yes, share-alike | Attribution-required |
| CC BY-NC | Yes | Required | No | Attribution-required |
| Royalty-Free | Per provider terms | Per provider | Usually | Clear with review |
| Rights-Managed | Requires negotiation | Per license | Per license | **Unclear** |
| Editorial-Only | News/documentary context | Per license | No | **Unclear** |
| Fair Use | Fact-specific legal defense | N/A | N/A | **Unclear** — legal review required |
| Unknown | **Do not use without clearance** | — | — | **Unclear** |

If an archive is unreachable, the harness falls back to the cached `docs/archive-directory.md` and marks rights clarity as **Unclear** until live verification is possible.

---

## Public archive directory

The harness queries authoritative sources first:

- **Library of Congress** — U.S. history, culture, early cinema (`loc.gov/film-and-videos`)
- **Internet Archive / Prelinger** — ephemeral, educational, industrial films (`archive.org/details/prelinger`)
- **U.S. National Archives (NARA)** — federal records, NASA, military (`catalog.archives.gov`)
- **Europeana** — European cultural heritage (`europeana.eu`)
- **Wikimedia Commons** — CC0/CC-BY images, video, audio (`commons.wikimedia.org`)
- **Pexels / Pixabay** — CC0-style stock (`pexels.com`, `pixabay.com`)

See [`docs/archive-directory.md`](docs/archive-directory.md) for source-specific search strategies, machine-query templates, and license-verification checklists.

---

## Knowledge pipeline

`tools/knowledge_updater.py` keeps `SECOND-KNOWLEDGE-BRAIN.md` current by:

1. Querying the archive sources above across documentary-related keywords.
2. Falling back to DuckDuckGo HTML search when APIs are unavailable.
3. Deduplicating entries by URL hash.
4. Appending dated entries with `<!--h:hash-->` markers.
5. Classifying licenses via `tools/rights_classifier.py`.

```bash
python tools/knowledge_updater.py --dry-run   # preview
python tools/knowledge_updater.py             # append to brain
```

---

## Testing

The suite covers all six documented scenarios plus unit tests for every tool:

```bash
pytest tests/ -v
```

Current result: **38 passed**.

| Test file | Coverage |
|---|---|
| `test_archive_client.py` | Title/link extraction, LoC/IA/Wikimedia JSON parsing, dedup, offline handling |
| `test_rights_classifier.py` | PD, CC-BY, unknown, fair use, posture checks |
| `test_knowledge_updater.py` | Hashing, dedup, append, dry-run, fetch dedup |
| `test_scoring_engine.py` | Coherence, coverage, partial coverage, rights clarity |
| `test_scenarios.py` | Apollo PD, rights unclear, fair use, coverage gap, attribution, archive offline |
| `test_skills.py` | Skill front matter + required sections + rights gate |

---

## Cross-cluster sharing

Two sub-skills are intentionally shared with other design-creative-media clusters:

- **`sub-evaluation-framework-selector.md`** — used by clusters **104, 184, 185** for creative framework selection.
- **`sub-scoring-engine.md`** — used by clusters **104, 184, 185** for standardized scoring.

Both expose stable JSON schemas and allow downstream clusters to inject extra dimensions. See [`docs/cross-cluster-integration.md`](docs/cross-cluster-integration.md) for contracts and maintainer notes.

---

## Roadmap &amp; contributing

This project is considered **feature-complete for Phase 0–5**. Future maintainers may:

- Add more archive source handlers (e.g., Europeana API, Getty open content).
- Integrate a web-search API key path for higher-volume queries.
- Add a CLI entry point that runs the full harness end-to-end.
- Add GitHub Actions CI to run `pytest` on every PR.

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for conventions.

---

## License

MIT. See [`LICENSE`](LICENSE).

Built with care for documentary makers who need both **creative clarity** and **legal safety**.
