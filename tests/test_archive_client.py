"""Tests for archive_client helpers and source parsers."""
from __future__ import annotations

import json
from unittest.mock import patch

import archive_client as ac


def test_extract_title():
    html = "<html><head><title>Apollo 11</title></head><body></body></html>"
    assert ac.extract_title(html) == "Apollo 11"


def test_extract_links():
    html = '<a href="/item/1">One</a><a href="https://x.com/2">Two</a>'
    links = ac.extract_links(html, "https://example.com")
    urls = {link["url"] for link in links}
    assert "https://example.com/item/1" in urls
    assert "https://x.com/2" in urls


def test_guess_year():
    assert ac._guess_year({"year": "1969"}) == 1969
    assert ac._guess_year({"date": "July 20, 1969"}) == 1969
    assert ac._guess_year({"title": "nothing"}) == 0


def test_loc_search_parses_json(monkeypatch):
    fake = {
        "results": [
            {"url": "https://loc.gov/item/1", "title": "Apollo", "description": "Moon"}
        ]
    }

    def mock_fetch(url):
        return json.dumps(fake)

    monkeypatch.setattr(ac, "fetch_url", mock_fetch)
    results = ac.loc_search("apollo", max_results=5)
    assert len(results) == 1
    assert results[0]["source"] == "Library of Congress"


def test_internet_archive_search_parses_json(monkeypatch):
    fake = {
        "response": {
            "docs": [{"identifier": "apollo11", "title": "Apollo 11", "year": "1969"}]
        }
    }

    def mock_fetch(url):
        return json.dumps(fake)

    monkeypatch.setattr(ac, "fetch_url", mock_fetch)
    results = ac.internet_archive_search("apollo")
    assert len(results) == 1
    assert results[0]["url"] == "https://archive.org/details/apollo11"


def test_wikimedia_search_parses_json(monkeypatch):
    fake = {"query": {"search": [{"title": "Apollo 11 launch.jpg"}]}}

    def mock_fetch(url):
        return json.dumps(fake)

    monkeypatch.setattr(ac, "fetch_url", mock_fetch)
    results = ac.wikimedia_search("apollo 11")
    assert len(results) == 1
    assert "Apollo_11_launch.jpg" in results[0]["url"]


def test_search_all_dedup_and_sets_access_date(monkeypatch):
    def fake_loc(q, n):
        return [{"url": "https://x/1", "title": "X", "source": "LoC", "year": 2024}]

    def fake_ia(q, collection="prelinger", max_results=10):
        return [{"url": "https://x/1", "title": "X", "source": "IA", "year": 2024}]

    def fake_wiki(q, n):
        return []

    monkeypatch.setattr(ac, "loc_search", fake_loc)
    monkeypatch.setattr(ac, "internet_archive_search", fake_ia)
    monkeypatch.setattr(ac, "wikimedia_search", fake_wiki)
    results = ac.search_all("apollo")
    assert len(results) == 1
    assert results[0]["access_date"]


def test_fetch_url_returns_none_on_error(monkeypatch):
    def raise_error(*args, **kwargs):
        raise Exception("network down")

    monkeypatch.setattr(ac, "requests", None)
    monkeypatch.setattr(ac.urllib.request, "urlopen", raise_error)
    assert ac.fetch_url("https://example.com") is None
