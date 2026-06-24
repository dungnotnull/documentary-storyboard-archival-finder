"""Lightweight archive API/search clients for public archives.

Implements machine-query templates from docs/archive-directory.md using the
standard library plus optional requests/beautifulsoup4 when available.
"""
from __future__ import annotations

import json
import os
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date
from html.parser import HTMLParser
from typing import Any

try:
    import requests
except ImportError:  # pure stdlib fallback is tested
    requests = None  # type: ignore[assignment]

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # type: ignore[assignment,misc]


DEFAULT_TIMEOUT = int(os.environ.get("ARCHIVE_CLIENT_TIMEOUT", "20"))


@dataclass(frozen=True)
class ArchiveEntry:
    beat: str
    shot_id: str
    description: str
    source: str
    url: str
    license_text: str | None
    attribution_string: str | None
    access_date: str
    raw: dict[str, Any]


class _TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title += data


def fetch_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> str | None:
    """Fetch a URL with a browser-like user agent and short timeout."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/json,*/*",
    }
    if requests is not None:
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except Exception:
            return None
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            charset = response.headers.get_content_charset("utf-8")
            return response.read().decode(charset, errors="replace")
    except Exception:
        return None


def extract_title(html: str) -> str:
    """Extract the page <title> as a fallback description."""
    parser = _TitleParser()
    parser.feed(html)
    return parser.title.strip()


def extract_links(html: str, base_url: str) -> list[dict[str, Any]]:
    """Extract visible hyperlink text and hrefs from HTML."""
    links: list[dict[str, Any]] = []

    if BeautifulSoup is not None:
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.find_all("a", href=True):
            url = urllib.parse.urljoin(base_url, a["href"])
            txt = " ".join(a.stripped_strings)
            links.append({"url": url, "title": txt, "summary": txt})
        return links

    class LinkParser(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self._href: str | None = None
            self._text: list[str] = []
            self._in_a = False

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            if tag.lower() == "a":
                self._in_a = True
                for name, value in attrs:
                    if name == "href" and value is not None:
                        self._href = value

        def handle_endtag(self, tag: str) -> None:
            if tag.lower() == "a":
                if self._href:
                    url = urllib.parse.urljoin(base_url, self._href)
                    links.append(
                        {
                            "url": url,
                            "title": " ".join(self._text).strip(),
                            "summary": " ".join(self._text).strip(),
                        }
                    )
                self._href = None
                self._text = []
                self._in_a = False

        def handle_data(self, data: str) -> None:
            if self._in_a:
                self._text.append(data.strip())

    parser = LinkParser()
    parser.feed(html)
    return links


def loc_search(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    url = f"https://www.loc.gov/film-and-videos/?q={urllib.parse.quote(query)}&fo=json"
    html = fetch_url(url)
    if html is None:
        return []
    try:
        data = json.loads(html)
        results = data.get("results", []) or data.get("search", {}).get("results", [])
        return [
            {
                "url": r.get("url", ""),
                "title": r.get("title", ""),
                "summary": r.get("description", "") or r.get("summary", ""),
                "source": "Library of Congress",
                "year": _guess_year(r),
            }
            for r in results[:max_results]
            if r.get("url")
        ]
    except json.JSONDecodeError:
        return []


def internet_archive_search(query: str, collection: str = "prelinger", max_results: int = 10) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(f"collection:{collection} {query}")
    url = f"https://archive.org/advancedsearch.php?q={encoded}&output=json&rows={max_results}"
    html = fetch_url(url)
    if html is None:
        return []
    try:
        data = json.loads(html)
        docs = data.get("response", {}).get("docs", [])
        return [
            {
                "url": f"https://archive.org/details/{doc.get('identifier', '')}",
                "title": doc.get("title", ""),
                "summary": doc.get("description", "") or "",
                "source": "Internet Archive",
                "year": _guess_year(doc),
            }
            for doc in docs
            if doc.get("identifier")
        ]
    except json.JSONDecodeError:
        return []


def wikimedia_search(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(query)
    url = (
        "https://commons.wikimedia.org/w/api.php?"
        f"action=query&list=search&srsearch={encoded}&srnamespace=6&format=json"
    )
    html = fetch_url(url)
    if html is None:
        return []
    try:
        data = json.loads(html)
        results = data.get("query", {}).get("search", [])
        return [
            {
                "url": f"https://commons.wikimedia.org/wiki/{r.get('title', '').replace(' ', '_')}",
                "title": r.get("title", ""),
                "summary": r.get("snippet", ""),
                "source": "Wikimedia Commons",
                "year": 0,
            }
            for r in results[:max_results]
            if r.get("title")
        ]
    except json.JSONDecodeError:
        return []


def _guess_year(record: dict[str, Any]) -> int:
    for key in ("year", "date", "created", "issued", "publicdate"):
        value = record.get(key)
        if not value:
            continue
        match = re.search(r"(19|20)\d{2}", str(value))
        if match:
            return int(match.group(0))
    return 0


def search_all(query: str, max_results: int = 10) -> list[dict[str, Any]]:
    """Run the query across all configured archive sources and merge results."""
    entries: list[dict[str, Any]] = []
    entries.extend(loc_search(query, max_results))
    entries.extend(internet_archive_search(query, max_results=max_results))
    entries.extend(wikimedia_search(query, max_results))
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for e in entries:
        url = e.get("url", "")
        if url and url not in seen:
            seen.add(url)
            e.setdefault("access_date", date.today().isoformat())
            unique.append(e)
    return unique
