# Vector DB MCP Server Demo

This demo MCP server simulates a vector database with a tiny in-memory index.

## What it does

The server exposes tools for working with documents by semantic similarity:

- `list_documents` to inspect the indexed documents
- `get_document` to read one full document
- `search_documents` to run semantic search over the store
- `add_document` to simulate ingestion into a vector database

## Example prompts

- "Find the best document for VPN troubleshooting"
- "Search for documents about password resets"
- "Add a new document for monitor flickering fixes"
- "List the documents in the vector store"

## Run it

From this folder:

```bash
uv sync
uv run vector-mcp
```

You can also run the file directly with:

```bash
uv run main.py
```

## Notes

This is intentionally a lightweight example. It behaves like a vector database demo, but keeps everything in memory so it is easy to understand and easy to use in training sessions.