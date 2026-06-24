"""Tests for knowledge_updater dedup, hashing, and append logic."""
from __future__ import annotations

import hashlib
from datetime import date
from pathlib import Path

import knowledge_updater as ku


def test_url_hash():
    expected = hashlib.sha256(b"https://example.com").hexdigest()[:12]
    assert ku._url_hash("https://example.com") == expected


def test_hashes_detects_markers():
    text = "- something <!--h:abc123def45a-->\n- else <!--h:def456abc123-->"
    assert ku._hashes(text) == {"abc123def45a", "def456abc123"}


def test_score_boosts_recent():
    old = {"title": "documentary", "summary": "", "year": 1990, "source": "Blog"}
    recent = {"title": "documentary", "summary": "", "year": date.today().year, "source": "Blog"}
    assert ku.score(recent) > ku.score(old)


def test_append_entries_dedup(tmp_path):
    brain = tmp_path / "SECOND-KNOWLEDGE-BRAIN.md"
    brain.write_text("# Brain\n\n## Knowledge Update Log\n", encoding="utf-8")
    entries = [
        {"url": "https://example.com/1", "title": "First", "source": "Test", "year": 2024},
        {"url": "https://example.com/1", "title": "First dup", "source": "Test", "year": 2024},
        {"url": "https://example.com/2", "title": "Second", "source": "Test", "year": 2024},
    ]
    added = ku.append_entries(entries, brain_path=brain)
    assert added == 2
    text = brain.read_text(encoding="utf-8")
    assert text.count("<!--h:") == 2


def test_append_entries_dry_run_does_not_write(tmp_path):
    brain = tmp_path / "SECOND-KNOWLEDGE-BRAIN.md"
    original = "# Brain\n"
    brain.write_text(original, encoding="utf-8")
    entries = [{"url": "https://example.com/3", "title": "Third", "source": "Test", "year": 2024}]
    added = ku.append_entries(entries, brain_path=brain, dry_run=True)
    assert added == 1
    assert brain.read_text(encoding="utf-8") == original


def test_fetch_entries_returns_deduped_list(monkeypatch):
    def fake_fetch_archive(n):
        return [
            {"url": "https://a.com/1", "title": "A1", "source": "LoC", "year": 2024},
            {"url": "https://a.com/2", "title": "A2", "source": "LoC", "year": 2024},
        ]

    def fake_fetch_websearch(n):
        return [{"url": "https://a.com/1", "title": "A1 dup", "source": "DDG", "year": 2024}]

    monkeypatch.setattr(ku, "fetch_archive_entries", fake_fetch_archive)
    monkeypatch.setattr(ku, "fetch_websearch_entries", fake_fetch_websearch)
    entries = ku.fetch_entries()
    assert len(entries) == 2


def test_main_dry_run(tmp_path, capsys):
    brain = tmp_path / "SECOND-KNOWLEDGE-BRAIN.md"
    brain.write_text("# Brain\n\n## Knowledge Update Log\n", encoding="utf-8")

    def fake_fetch(ms, mw):
        return [{"url": "https://example.com/x", "title": "X", "source": "Test", "year": 2024}]

    monkeypatch = None  # cannot use fixture here; patch via unittest
    from unittest.mock import patch

    with patch.object(ku, "fetch_entries", fake_fetch):
        rc = ku.main(["--dry-run", "--brain", str(brain)])
    captured = capsys.readouterr()
    assert rc == 0
    assert "would append 1" in captured.out
    assert brain.read_text(encoding="utf-8").count("<!--h:") == 0
