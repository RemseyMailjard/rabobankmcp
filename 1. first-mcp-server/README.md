# Rabobank Demo MCP Server Lab

This project demonstrates how to expose approved internal business functionality to an AI client through MCP.

## Goal

Understand how an MCP server works and how AI assistants can securely interact with internal systems through approved tools.

## Learning Objectives

- Explain the MCP client-server model.
- Create MCP tools with FastMCP.
- Run an MCP server locally over HTTP.
- Connect GitHub Copilot (Agent mode) to the MCP server.
- Test tool invocation through natural language prompts.

## Scenario

In this fictional banking scenario, the MCP server exposes demo operations:

- `get_account_balance` — look up a hardcoded internal account balance.
- `get_customer_name` — look up a hardcoded customer name by ID.
- `get_branch_information` — look up hardcoded branch details.
- `get_exchange_rate` — live rate from a currency to EUR (uses ExchangeRate-API).
- `get_live_exchange_rate` — live rate between any two currencies (defaults target to EUR).
- `convert_currency` — convert an amount between two currencies at the live rate.

## Prerequisites

### 1. Install `uv`

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS (Homebrew):

```bash
brew install uv
```

macOS (official script):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:

```powershell
uv --version
```

Optional Python install via `uv`:

```powershell
uv python install 3.12
```

### 2. Create a new MCP project (already done in this repo)

```powershell
uv init first-mcp-server
cd first-mcp-server
```

### 3. Add dependencies (already done in this repo)

```powershell
uv add fastmcp httpx python-dotenv
```

## Exchange Rate API Setup

The `get_exchange_rate`, `get_live_exchange_rate`, and `convert_currency` tools call
[ExchangeRate-API](https://www.exchangerate-api.com/) for live rates. They need an API key.

### 1. Get a free API key

1. Sign up at [https://app.exchangerate-api.com/](https://app.exchangerate-api.com/).
2. Confirm your email and open the dashboard.
3. Copy your API key (looks like `1234567890abcdef12345678`).

The key is used to build the request URL:

```text
https://v6.exchangerate-api.com/v6/<API_KEY>/latest/<BASE_CURRENCY>
```

### 2. Create your `.env` file

This repo includes an `.env.example`. Copy it to `.env` and insert your own key.

Windows (PowerShell):

```powershell
Copy-Item .env.example .env
```

macOS / Linux:

```bash
cp .env.example .env
```

Then edit `.env`:

```text
EXCHANGE_RATE_API_KEY=your_real_key_here
```

`main.py` loads this automatically via `python-dotenv` (`load_dotenv()`), and `.env`
is listed in `.gitignore` so your key is not committed.

> Security note: `.env.example` currently contains a real-looking key. Treat it as
> compromised — revoke/rotate it in the ExchangeRate-API dashboard and keep only a
> placeholder in `.env.example`. Never commit a real key.

### 3. Behavior without a key

If `EXCHANGE_RATE_API_KEY` is missing, the currency tools return:

```text
API key is missing. Set EXCHANGE_RATE_API_KEY as an environment variable.
```

The account, customer, and branch tools work without any key (they use hardcoded data).

## Main Command Flow

- Project setup: `uv init first-mcp-server`
- Dependency install: `uv add fastmcp`
- Run server: `uv run fastmcp run main.py:mcp --transport http --port 8000`
- VS Code config: `.vscode/mcp.json`

## Run the MCP Server

Start HTTP transport:

```powershell
uv run fastmcp run main.py:mcp --transport http --port 8000
```

The server is running when you see output like:

```text
Uvicorn running on http://127.0.0.1:8000
```

Leave this terminal open.

If port 8000 is in use, run on 8001:

```powershell
uv run fastmcp run main.py:mcp --transport http --port 8001
```

Then update `.vscode/mcp.json` to use port 8001.

## Important Endpoint Note

`/mcp` is not a normal webpage or REST endpoint. Browsing to it directly can return:

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

This is expected. MCP clients use the proper protocol headers.

## Connect to VS Code

Open this project folder in VS Code (folder open is required, not a single file).

The project includes:

- `.vscode/mcp.json`

With configuration:

```json
{
	"servers": {
		"rabobank-demo": {
			"url": "http://127.0.0.1:8000/mcp"
		}
	}
}
```

Connection steps:

1. Open `.vscode/mcp.json`.
2. Click `Start` above the server entry.
3. Open GitHub Copilot Chat.
4. Switch to `Agent mode`.
5. Click the `Select tools` icon (plus icon).
6. Confirm `rabobank-demo` appears with available tools.

## Test Prompts

Use prompts like:

```text
What is the balance of account 12345?
What is the name of customer 1001?
Show information about branch BR001.
What is the USD to EUR exchange rate?
What is the live exchange rate from GBP to USD?
Convert 100 USD to EUR.
```

Demo data available for the prompts above:

- Accounts: `12345`, `67890`
- Customers: `1001` (John Smith), `1002` (Aisha Khan)
- Branch: `BR001` (Utrecht)

## Demo Script

```text
This is a minimal internal MCP server.
It exposes approved tools to an AI client.
The AI assistant cannot directly access internal systems.
It can only call tools that the MCP server exposes.
In this example, approved tools include account, customer, branch, and exchange rate lookups.
```

## Reflection Questions

- Why use an MCP server instead of direct database access from an AI assistant?
- What advantages does MCP provide over hardcoding business logic in prompts?
- What security benefits come from exposing only approved tools?
- Which internal systems in your organization could benefit from MCP?

## Key Takeaway

An MCP server is a secure integration layer between AI assistants and internal systems. By exposing carefully designed tools, organizations can provide useful business functionality without directly exposing databases, internal APIs, or sensitive infrastructure.
