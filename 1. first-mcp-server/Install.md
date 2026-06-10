# Minimal MCP Server Demo with `uv`, FastMCP and VS Code

This guide shows how to create and run a minimal MCP server for a developer demo.

The goal is to build the smallest possible working example:

* one Python project
* one MCP server
* one MCP tool
* running locally with `uv`
* connected to VS Code / GitHub Copilot

---

## 1. Install `uv` on Windows

Open PowerShell and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal and verify the installation:

```powershell
uv --version
```

Optional: install Python through `uv`:

```powershell
uv python install 3.12
```

---

## 2. Create a new MCP project

Go to the folder where you want to create the demo project.

```powershell
cd "C:\Users\Remse\Desktop\MCP-server Rabobank\MCP-server examples"
```

Create a new project:

```powershell
uv init first-mcp-server
cd first-mcp-server
```

This creates a Python project with a `pyproject.toml` file.

---

## 3. Add FastMCP

Install FastMCP into the project:

```powershell
uv add fastmcp
```

For this minimal demo, `fastapi` and `requests` are not needed.

---

## 4. Create the minimal MCP server

Open `main.py` and replace the content with:

```python
from fastmcp import FastMCP

mcp = FastMCP("Rabobank Demo MCP Server")


@mcp.tool()
def get_account_balance(account_number: str) -> str:
    """Get the balance for an internal Rabobank account."""
    return f"Account {account_number} has a balance of €1,250.00"


if __name__ == "__main__":
    mcp.run()
```

This server exposes one MCP tool:

```text
get_account_balance
```

---

## 5. Run the MCP server over HTTP

Run the server with HTTP transport:

```powershell
uv run fastmcp run main.py:mcp --transport http --port 8000
```

You should see output similar to:

```text
Starting MCP server 'Rabobank Demo MCP Server'
with transport 'http' on http://127.0.0.1:8000/mcp
Uvicorn running on http://127.0.0.1:8000
```

Leave this terminal open.

---

## 6. Important: do not test `/mcp` as a normal webpage

If you open this URL in the browser:

```text
http://127.0.0.1:8000/mcp
```

You may see:

```json
{
  "jsonrpc": "2.0",
  "id": "server-error",
  "error": {
    "code": -32600,
    "message": "Not Acceptable: Client must accept text/event-stream"
  }
}
```

This is expected.

The `/mcp` endpoint is not a normal website or REST API endpoint. It is meant to be used by an MCP-compatible client.

---

## 7. Connect the MCP server to VS Code

In your project, create this file:

```text
.vscode/mcp.json
```

Add the following configuration:

```json
{
  "servers": {
    "rabobank-demo": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Save the file.

---

## 8. Start the MCP server in VS Code

Make sure your HTTP MCP server is still running in the terminal.

Then open:

```text
.vscode/mcp.json
```

In VS Code, use the available MCP controls to start or detect the server.

After the server is detected, GitHub Copilot Chat can use the MCP tool.

---

## 9. Use the MCP tool in GitHub Copilot Chat

Open GitHub Copilot Chat in VS Code.

Switch to:

```text
Agent mode
```

Use a prompt like:

```text
Use the rabobank-demo MCP server to get the account balance for NL91RABO0123456789.
```

Copilot should discover and call the MCP tool:

```text
get_account_balance
```

---

## 10. What to explain during the demo

You can explain it like this:

```text
This is a minimal internal MCP server. 
It exposes one approved tool to an AI client.
The AI assistant cannot directly access internal systems.
It can only call the tools that the MCP server exposes.
In this example, the approved tool is get_account_balance.
```

---

## Minimal command overview

```powershell
uv init first-mcp-server
cd first-mcp-server
uv add fastmcp
uv run fastmcp run main.py:mcp --transport http --port 8000
```

---

## Minimal project structure

```text
first-mcp-server
│
├── .vscode
│   └── mcp.json
│
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Key learning point

An MCP server is not the AI assistant itself.

It is a controlled bridge between an AI client and approved tools, data or systems.

For an enterprise environment, this means developers can expose internal capabilities in a controlled way instead of giving AI unrestricted access.
