#!/usr/bin/env python3
"""knowledge_updater.py - Documentary Storyboard & Archival Finder (idea 227).

Crawls documentary-craft and public-archive sources, appending dated, deduplicated
entries to SECOND-KNOWLEDGE-BRAIN.md.

Usage:
    python tools/knowledge_updater.py [--dry-run] [--force] [--max-per-source N]
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
import urllib.parse
from datetime import date
from pathlib import Path
from typing import Protocol

from archive_client import fetch_url, search_all
from rights_classifier import classify

BRAIN = Path(__file__).resolve().parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"

SOURCES = {
    "loc": "https://www.loc.gov/film-and-videos/",
    "archive_org": "https://archive.org/details/prelinger",
    "nara": "https://catalog.archives.gov/",
    "wikimedia": "https://commons.wikimedia.org/",
    "cc": "https://creativecommons.org/about/cclicenses/",
}

KEYWORDS = [
    "documentary",
    "storyboard",
    "archival footage",
    "public domain",
    "creative commons",
    "shot list",
    "b-roll",
    "rights clearance",
    "fair use",
    "narrative structure",
]


def _url_hash(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:12]


def _hashes(text: str) -> set[str]:
    return set(re.findall(r"<!--h:([0-9a-f]{12})-->", text))


def score(entry: dict[str, object]) -> float:
    t = (str(entry.get("title", "")) + " " + str(entry.get("summary", ""))).lower()
    keyword_hits = sum(1 for k in KEYWORDS if k in t)
    recency = (
        1.0
        if int(entry.get("year") or 0) >= date.today().year - 1
        else 0.5
    )
    source_bonus = 0.2 if str(entry.get("source", "")) in SOURCES.values() else 0.0
    return keyword_hits * recency + source_bonus


def fetch_archive_entries(max_per_source: int = 10) -> list[dict[str, object]]:
    """Fetch candidate entries from archive sources across documentary keywords."""
    entries: list[dict[str, object]] = []
    for keyword in KEYWORDS:
        for entry in search_all(keyword, max_results=max_per_source):
            if entry.get("url"):
                entries.append(entry)
    seen: set[str] = set()
    unique: list[dict[str, object]] = []
    for e in entries:
        h = _url_hash(str(e["url"]))
        if h not in seen:
            seen.add(h)
            unique.append(e)
    return unique


class SearchProvider(Protocol):
    def search(self, query: str, max_results: int) -> list[dict[str, object]]: ...


class DuckDuckGoHtmlProvider:
    """Scrape DuckDuckGo HTML results as a zero-API-key fallback."""

    def search(self, query: str, max_results: int = 10) -> list[dict[str, object]]:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        html = fetch_url(url, timeout=20)
        if not html:
            return []
        results: list[dict[str, object]] = []
        for block in re.findall(
            r'<a rel="nofollow" class="result__a" href="([^"]+)"[^>]*>(.*?)</a>',
            html,
            re.S,
        ):
            href, title_html = block
            title = re.sub(r"<[^>]+>", "", title_html)
            results.append(
                {"url": href, "title": title, "summary": "", "source": "DuckDuckGo", "year": 0}
            )
            if len(results) >= max_results:
                break
        return results


def _pick_search_provider() -> SearchProvider:
    return DuckDuckGoHtmlProvider()


def fetch_websearch_entries(max_per_keyword: int = 5) -> list[dict[str, object]]:
    provider = _pick_search_provider()
    entries: list[dict[str, object]] = []
    for keyword in KEYWORDS:
        try:
            entries.extend(provider.search(keyword, max_results=max_per_keyword))
        except Exception as exc:
            print(f"[search] provider failed for '{keyword}': {exc}", file=sys.stderr)
    seen: set[str] = set()
    unique: list[dict[str, object]] = []
    for e in entries:
        url = str(e.get("url", ""))
        h = _url_hash(url)
        if url and h not in seen:
            seen.add(h)
            unique.append(e)
    return unique


def fetch_entries(max_per_source: int = 10, max_websearch: int = 5) -> list[dict[str, object]]:
    """Return deduplicated candidate entries from archives and web search."""
    entries = fetch_archive_entries(max_per_source)
    entries.extend(fetch_websearch_entries(max_websearch))
    seen: set[str] = set()
    unique: list[dict[str, object]] = []
    for e in entries:
        url = str(e.get("url", ""))
        h = _url_hash(url)
        if url and h not in seen:
            seen.add(h)
            e.setdefault("access_date", date.today().isoformat())
            license_text = e.get("license")
            if license_text:
                e["license_category"] = classify(str(license_text)).license.value
            unique.append(e)
    return unique


def append_entries(
    entries: list[dict[str, object]],
    brain_path: Path | None = None,
    dry_run: bool = False,
) -> int:
    target = brain_path or BRAIN
    if not target.exists():
        raise FileNotFoundError(f"Knowledge brain not found: {target}")
    text = target.read_text(encoding="utf-8")
    seen = _hashes(text)
    lines: list[str] = []
    added = 0
    for e in sorted(entries, key=score, reverse=True):
        url = str(e.get("url", ""))
        if not url:
            continue
        h = _url_hash(url)
        if h in seen:
            continue
        title = str(e.get("title", "(untitled)")).replace("\n", " ").strip()
        source = e.get("source", "?")
        year = e.get("year", "?") or "?"
        lines.append(
            f"- {date.today().isoformat()} - {title} "
            f"({source}, {year}) {url} <!--h:{h}-->"
        )
        seen.add(h)
        added += 1
    if added and not dry_run:
        target.write_text(text.rstrip() + "\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return added


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update SECOND-KNOWLEDGE-BRAIN.md")
    parser.add_argument("--dry-run", action="store_true", help="Do not write to the brain.")
    parser.add_argument("--force", action="store_true", help="Ignore staleness guard.")
    parser.add_argument("--max-per-source", type=int, default=10)
    parser.add_argument("--max-websearch", type=int, default=5)
    parser.add_argument("--brain", type=Path, default=None)
    args = parser.parse_args(argv)

    target = args.brain or BRAIN
    entries = fetch_entries(args.max_per_source, args.max_websearch)
    added = append_entries(entries, brain_path=target, dry_run=args.dry_run)
    action = "would append" if args.dry_run else "appended"
    print(f"[227] {action} {added} entries to {target.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
