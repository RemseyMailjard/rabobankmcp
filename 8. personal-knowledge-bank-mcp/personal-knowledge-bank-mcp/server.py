"""Personal Knowledge Bank — MCP server.

Exposes a local folder of Markdown notes to an AI assistant through MCP,
using FastMCP. The server offers three tools (list, read, search) and one
bonus prompt. Every file access is sandboxed to the knowledge-bank folder.
"""

from pathlib import Path

from fastmcp import FastMCP

# Root of the knowledge bank — the hard sandbox boundary.
# Resolve once so every later check compares against an absolute, real path.
KB_ROOT = (Path(__file__).parent / "personal-knowledge-bank").resolve()

mcp = FastMCP("personal-knowledge-bank")


# --- internal logic (plain functions, easy to test) -----------------------

def _safe_path(relative_path: str) -> Path:
    """Resolve a requested path and ensure it stays inside KB_ROOT.

    This is the path-traversal guard: a request such as
    ``../../etc/passwd`` resolves to a path outside the knowledge bank and
    is rejected before any file is opened.
    """
    candidate = (KB_ROOT / relative_path).resolve()
    if not candidate.is_relative_to(KB_ROOT):
        raise ValueError("Access outside the knowledge bank is not allowed.")
    return candidate


def _list() -> list[str]:
    return [str(p.relative_to(KB_ROOT)) for p in sorted(KB_ROOT.rglob("*.md"))]


def _read(relative_path: str) -> str:
    path = _safe_path(relative_path)
    if path.suffix != ".md" or not path.is_file():
        raise ValueError("File not found in the knowledge bank.")
    return path.read_text(encoding="utf-8")


def _search(query: str) -> list[dict]:
    needle = query.lower()
    results: list[dict] = []
    for path in sorted(KB_ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if needle in text.lower():
            snippet = next(
                (line.strip() for line in text.splitlines() if needle in line.lower()),
                "",
            )
            results.append({"file": str(path.relative_to(KB_ROOT)), "snippet": snippet})
    return results


# --- MCP surface (the three required tools + one bonus prompt) -------------

@mcp.tool
def list_knowledge_files() -> list[str]:
    """List all Markdown files available in the knowledge bank."""
    return _list()


@mcp.tool
def read_knowledge_file(relative_path: str) -> str:
    """Read one Markdown file from the knowledge bank.

    Args:
        relative_path: Path relative to the knowledge-bank root,
            e.g. ``profile/professional-profile.md``.
    """
    return _read(relative_path)


@mcp.tool
def search_knowledge_bank(query: str) -> list[dict]:
    """Search titles, tags and content across the knowledge bank.

    Returns a list of ``{"file": ..., "snippet": ...}`` matches, where the
    snippet is the first line in the file that contains the query.
    """
    return _search(query)


@mcp.prompt
def refinement_summary() -> str:
    """Bonus: surface the saved summary prompt as a reusable MCP prompt.

    Demonstrates the third MCP building block — a Prompt — sourced directly
    from the knowledge bank so there is a single source of truth.
    """
    return _read("prompts/meeting-summary-prompt.md")


if __name__ == "__main__":
    # Default transport is stdio, which is what local assistants connect to.
    mcp.run()
