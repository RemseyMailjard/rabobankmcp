# Rabobank Demo MCP Server

This project exposes a minimal FastMCP server with a banking demo tool and dynamic tool discovery.

## Available discovery methods

The server includes two discovery tool names for compatibility:

- discoverTools
- listTools

Both return the same dynamic capability catalog built from the live MCP tool registry.

## Discovery response shape

Each discovered tool contains:

- name
- description
- inputSchema (JSON Schema style)
- examples (LLM-oriented prompt ideas)
- tags (category hints)

Top-level metadata includes:

- server
- discoverySchemaVersion
- generatedAt
- toolCount

Optional discovery inputs:

- tag: filter tools by category
- include_auth: include authentication requirement metadata
- compact: return a shortened item shape for quick summaries

## User prompts to try

- What can I do with this MCP server?
- Which tools are available?
- Show available capabilities
- Give examples of supported prompts

## Run locally

Start the server:

```powershell
uv run fastmcp run main.py:mcp --transport http --port 8000
```

Then connect from an MCP-capable client and call discoverTools or listTools.
