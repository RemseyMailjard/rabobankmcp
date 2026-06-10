# MCP Server Examples Overview

This workspace contains a small progression of MCP training examples. The folders are arranged from the simplest starter to more complete internal demo projects.

## Folder Guide

### `1. first-mcp-server/`

The smallest starting point. It shows a single MCP tool in one file and is useful for understanding the basic FastMCP shape before adding any real API calls.

### `2b. rabobank_internal_mcp_demo/`

The older Rabobank-style demo. It uses plain `requirements.txt`, direct `httpx` calls, and a simple `app/` package containing the fake internal API, data, and MCP server.

### `2. rabobank_internal_mcp_uv_demo/`

The newer and cleaner version of the Rabobank demo. It uses `pyproject.toml`, `uv` scripts, dotenv support, and separates startup for the API and MCP server.

### `3. docusign-signature-api/`

A separate dummy REST API example for a DocuSign-style signature workflow.

### `5. helpdesk-api/`

The dummy IT helpdesk API used by the assignment in `PROJECT-ASSIGNMENT.md`.

### `6. design-styling-mcp-server/`

A demo MCP server that returns ready-to-use UI components as HTML, CSS, and JavaScript snippets.

## How The Structure Evolved

The examples move from a minimal MCP proof of concept to a plain Python internal demo, then to a more maintainable `uv`-based training project.

In practice, the pattern is:

1. Start with a tiny FastMCP example.
2. Move to a fake internal API plus MCP wrapper.
3. Package the demo properly with `uv` and clearer entrypoints.

That makes the later folders easier to use as training material and easier to extend into a real MCP server project.
