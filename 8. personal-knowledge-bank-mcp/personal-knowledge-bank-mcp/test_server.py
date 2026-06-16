"""Smoke tests for the knowledge-bank MCP server logic."""

import pytest

import server


def test_lists_all_markdown_files():
    files = server._list()
    assert "index.md" in files
    assert "profile/professional-profile.md" in files
    assert len(files) == 6


def test_reads_a_known_file():
    content = server._read("profile/professional-profile.md")
    assert "# Professional Profile" in content


def test_search_finds_mcp():
    hits = server._search("MCP")
    assert any(h["file"] == "learnings/mcp-notes.md" for h in hits)


def test_path_traversal_is_blocked():
    with pytest.raises(ValueError):
        server._read("../../etc/passwd")


def test_non_markdown_is_rejected():
    with pytest.raises(ValueError):
        server._read("../pyproject.toml")
