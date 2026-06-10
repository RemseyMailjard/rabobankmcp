from __future__ import annotations

from collections import Counter
import math
import re
from typing import Any

from fastmcp import FastMCP

mcp = FastMCP("Vector DB MCP Demo")


DOCUMENTS: list[dict[str, Any]] = [
    {
        "id": "doc-001",
        "title": "VPN setup guide",
        "category": "network",
        "tags": ["vpn", "remote", "network", "globalprotect"],
        "content": "Install the VPN client, sign in with your work account, and reconnect if the tunnel drops.",
    },
    {
        "id": "doc-002",
        "title": "Resetting a password",
        "category": "account",
        "tags": ["password", "reset", "account", "login"],
        "content": "Use the self-service portal to reset your password or contact support if multi-factor enrollment is blocked.",
    },
    {
        "id": "doc-003",
        "title": "Printer troubleshooting",
        "category": "hardware",
        "tags": ["printer", "paper", "hardware", "office"],
        "content": "Check the printer queue, verify network connectivity, and reinstall the printer driver if jobs keep failing.",
    },
    {
        "id": "doc-004",
        "title": "Software license request",
        "category": "software",
        "tags": ["software", "license", "request", "access"],
        "content": "Submit a request with the application name, business reason, and manager approval before installation.",
    },
    {
        "id": "doc-005",
        "title": "External monitor flicker fix",
        "category": "hardware",
        "tags": ["monitor", "flicker", "display", "cable"],
        "content": "Test a new HDMI cable, update the graphics driver, and reduce refresh rate if the monitor flickers intermittently.",
    },
]

VECTOR_INDEX: dict[str, dict[str, float]] = {}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def build_vector(document: dict[str, Any]) -> dict[str, float]:
    tokens = tokenize(" ".join([document["title"], document["category"], " ".join(document["tags"]), document["content"]]))
    counts = Counter(tokens)
    length = math.sqrt(sum(value * value for value in counts.values())) or 1.0
    return {token: count / length for token, count in counts.items()}


def rebuild_index() -> None:
    VECTOR_INDEX.clear()
    for document in DOCUMENTS:
        VECTOR_INDEX[document["id"]] = build_vector(document)


def similarity(left: dict[str, float], right: dict[str, float]) -> float:
    shared_tokens = set(left) & set(right)
    return sum(left[token] * right[token] for token in shared_tokens)


def document_preview(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": document["id"],
        "title": document["title"],
        "category": document["category"],
        "tags": document["tags"],
    }


rebuild_index()


@mcp.tool()
def list_documents() -> list[dict[str, Any]]:
    """List the documents available in the demo vector store."""
    return [document_preview(document) for document in DOCUMENTS]


@mcp.tool()
def get_document(document_id: str) -> dict[str, Any]:
    """Return the full contents of one document in the demo vector store."""
    for document in DOCUMENTS:
        if document["id"] == document_id:
            return document
    return {
        "error": f"Unknown document '{document_id}'.",
        "available_documents": [document["id"] for document in DOCUMENTS],
    }


@mcp.tool()
def search_documents(query: str, top_k: int = 3) -> dict[str, Any]:
    """Search the demo vector store using semantic similarity.

    Use this when you want the closest matching internal documents for a question, keyword, or short request.
    """
    if top_k < 1:
        return {"error": "top_k must be at least 1."}

    query_vector = build_vector({
        "id": "query",
        "title": query,
        "category": "query",
        "tags": tokenize(query),
        "content": query,
    })

    results: list[dict[str, Any]] = []
    for document in DOCUMENTS:
        score = similarity(query_vector, VECTOR_INDEX[document["id"]])
        if score > 0:
            results.append(
                {
                    "id": document["id"],
                    "title": document["title"],
                    "category": document["category"],
                    "score": round(score, 4),
                    "snippet": document["content"],
                }
            )

    results.sort(key=lambda item: item["score"], reverse=True)
    return {
        "query": query,
        "top_k": top_k,
        "results": results[:top_k],
    }


@mcp.tool()
def add_document(title: str, content: str, category: str = "general", tags: list[str] | None = None) -> dict[str, Any]:
    """Add a document to the demo vector store and rebuild the index.

    Use this to simulate ingestion into a vector database.
    """
    tags = tags or []
    document_id = f"doc-{len(DOCUMENTS) + 1:03d}"
    new_document = {
        "id": document_id,
        "title": title,
        "category": category,
        "tags": tags,
        "content": content,
    }
    DOCUMENTS.append(new_document)
    VECTOR_INDEX[document_id] = build_vector(new_document)
    return {
        "message": "Document added to the demo vector store.",
        "document": document_preview(new_document),
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()