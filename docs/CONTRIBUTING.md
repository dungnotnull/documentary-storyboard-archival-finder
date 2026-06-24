# Contributing

## Project structure
- `skills/` - Claude skill definitions. Main orchestrator plus sub-skills.
- `tools/` - Python utilities: archive client, rights classifier, knowledge updater, scoring engine.
- `tests/` - pytest suite.
- `docs/` - reference documentation and cross-cluster integration notes.
- `SECOND-KNOWLEDGE-BRAIN.md` - living knowledge base.

## Running tests
```bash
python -m pytest tests/ -v
```

## Adding a new archive source
1. Add an entry to `docs/archive-directory.md`.
2. Add a source handler in `tools/archive_client.py` if an API client is needed.
3. Add a test in `tests/test_archive_client.py`.
4. Run the test suite before committing.

## Adding a shared dimension
1. Update `skills/sub-scoring-engine.md` rubric.
2. Update `tools/scoring_engine.py` implementation.
3. Update `docs/cross-cluster-integration.md` schema.
4. Add tests in `tests/test_scoring_engine.py`.
