# Personal Knowledge Bank — MCP server

A small, runnable example for the MCP training. It exposes a folder of Markdown
notes (`personal-knowledge-bank/`) to an AI assistant through an MCP server
built with [FastMCP](https://gofastmcp.com), managed with
[uv](https://docs.astral.sh/uv/).

The server offers the three tools the exercise asks for, plus one bonus prompt:

| Surface | Name | What it does |
| --- | --- | --- |
| Tool | `list_knowledge_files` | Lists every Markdown file in the bank. |
| Tool | `read_knowledge_file` | Reads one file (sandboxed to the bank). |
| Tool | `search_knowledge_bank` | Searches titles, tags and content. |
| Prompt | `refinement_summary` | Surfaces the saved summary prompt. |

Every file access goes through a **path-traversal guard**: a request like
`../../etc/passwd` is rejected before any file is opened.

## Project layout

```
personal-knowledge-bank-mcp/
├── pyproject.toml            # project + dependencies (fastmcp)
├── server.py                 # the MCP server
├── test_server.py            # smoke tests for the logic
├── README.md
└── personal-knowledge-bank/  # the knowledge bank itself
    ├── index.md
    ├── profile/professional-profile.md
    ├── projects/current-project.md
    ├── learnings/mcp-notes.md
    ├── prompts/meeting-summary-prompt.md
    └── templates/project-brief-template.md
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.
  (uv manages Python and all dependencies for you — no manual `pip` needed.)

## Install

From the project folder:

```bash
uv sync
```

This creates an isolated `.venv` and installs FastMCP from `pyproject.toml`,
pinning exact versions in `uv.lock`.

## Run

```bash
uv run server.py
```

The server starts on the default **stdio** transport, which is what a local
assistant connects to. It will appear to "hang" — that is correct; it is
waiting for an MCP client. Stop it with `Ctrl+C`.

## Test the logic

```bash
uv run pytest -q
```

## Try it interactively (MCP Inspector)

FastMCP ships a dev inspector:

```bash
uv run fastmcp dev server.py
```

Then call `list_knowledge_files`, `read_knowledge_file` and
`search_knowledge_bank` from the Inspector UI.

## Connect to Claude Desktop

```bash
uv run fastmcp install claude-desktop server.py
```

Restart Claude Desktop and ask, for example:

- *Which files are available in my knowledge bank?*
- *Read my professional profile.*
- *Search my knowledge bank for MCP.*
- *Based on my knowledge bank, what are my current goals?*

## Security note

This bank deliberately contains **no** customer data, secrets, real colleague
names or internal URLs. The folder root is treated as a hard sandbox, and the
server only ever reads `.md` files inside it. Keep it that way: see Module 9 of
the course reader for the data-classification reasoning.
