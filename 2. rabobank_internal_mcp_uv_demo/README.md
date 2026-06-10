# Internal MCP Server Demo with uv, FastAPI and FastMCP

A minimal, realistic training project for a 1-hour MCP session with developers.

The project demonstrates how **GitHub Copilot in Visual Studio Code** can use an **internal MCP server** to safely access approved internal APIs, documentation and review prompts.

> All data is fictional. No real Rabobank data is included.

---

## What this demo contains

```text
rabobank_internal_mcp_uv_demo/
├─ app/
│  ├─ data.py              # Fake internal banking data
│  ├─ internal_api.py      # Internal FastAPI API
│  ├─ mcp_server.py        # MCP server wrapping the internal API
│  ├─ run_api.py           # uv script entrypoint for the API
│  └─ __init__.py
├─ .vscode/
│  ├─ mcp.json             # VS Code MCP config using uv
│  └─ tasks.json           # Optional VS Code tasks
├─ scripts/
│  ├─ demo-calls.ps1       # PowerShell API test calls
│  └─ demo-calls.sh        # Bash API test calls
├─ .env.example
├─ .python-version
├─ pyproject.toml
└─ README.md
```

---

## Learning goal

Developers learn that an MCP server can act as a controlled AI-facing layer over internal systems.

```text
GitHub Copilot in VS Code
          │
          ▼
      MCP Client
          │
          ▼
 Internal MCP Server
          │
 ┌────────┼────────┬─────────────┐
 ▼        ▼        ▼             ▼
Internal  API      Policies      Architecture
API       Catalog  / Standards   Checks
```

---

## Prerequisite: uv

Check if uv is available:

```bash
uv --version
```

Install uv on Windows:

```powershell
winget install astral-sh.uv
```

Alternative Windows install:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

macOS/Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Setup

From the project folder:

```bash
uv sync
```

This creates the virtual environment and installs dependencies from `pyproject.toml`.

---

## Training Pages

This repository also contains HTML training material:

- `index.html` - self-study guide for MCP and Rabobank Design System context
- `mcp-extension-lab.html` - hands-on developer lab for extending this MCP server
- `mcp-extension-trainer-answer-key.html` - trainer guide with expected solution and demo flow

---

## Step 1 — Run the internal API

Terminal 1:

```bash
uv run bank-api
```

Open the FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

Test the health endpoint:

```bash
curl http://127.0.0.1:8000/health
```

Most endpoints require the demo API key:

```bash
curl -H "x-api-key: training-demo-key" http://127.0.0.1:8000/customers/CUST-1001
```

PowerShell alternative:

```powershell
$Headers = @{ "x-api-key" = "training-demo-key" }
Invoke-RestMethod -Uri "http://127.0.0.1:8000/customers/CUST-1001" -Headers $Headers
```

---

## Step 2 — Run the MCP server

Normally VS Code starts the MCP server using `.vscode/mcp.json`.

For a manual smoke test, open Terminal 2:

```bash
uv run bank-mcp
```

The MCP server uses stdio transport, so it may look like it is waiting. That is expected.

---

## Step 3 — Connect in Visual Studio Code

The example config is in:

```text
.vscode/mcp.json
```

It starts the MCP server with:

```bash
uv run bank-mcp
```

Important: keep the internal API running in Terminal 1.

---

## MCP tools

### `get_customer_profile(customer_id)`

Example IDs:

- `CUST-1001`
- `CUST-2002`

Example prompt:

```text
Use the internal MCP server to retrieve customer CUST-1001 and summarize the active products.
```

### `get_product_info(product_id)`

Example IDs:

- `MORTGAGE-FLEX`
- `PAYMENT-PLUS`
- `BUSINESS-ACCOUNT`

Example prompt:

```text
Use the internal MCP server to explain product MORTGAGE-FLEX for a developer who needs to call the product API.
```

### `get_api_endpoint_info(api_name)`

Example API names:

- `customer-onboarding`
- `product-catalog`

Example prompt:

```text
Use the internal MCP server to inspect the customer-onboarding API and tell me which endpoint creates a new onboarding case.
```

### `run_architecture_check(service_name)`

Example prompt:

```text
Run an architecture check for CustomerOnboardingService and summarize the findings as action items.
```

---

## MCP resources

### `policy://api-security`

Example prompt:

```text
Use the policy://api-security resource and summarize the security requirements for internal APIs.
```

### `architecture://event-driven-standards`

Example prompt:

```text
Use the architecture://event-driven-standards resource and explain what every event must contain.
```

---

## MCP prompt

### `api_security_review_prompt(api_name, endpoint)`

Example prompt:

```text
Use the api_security_review_prompt for the customer-onboarding API and endpoint /onboarding/cases.
```

---

## Trainer flow for 1 hour

### 0–10 min — Explain MCP

MCP is a standard way to let AI clients use tools, resources and prompts from approved systems.

### 10–20 min — Show the internal API

Open:

```text
http://127.0.0.1:8000/docs
```

Show that it represents internal systems:

- Customer API
- Product API
- API catalog
- Policies
- Architecture check

### 20–35 min — Show the MCP server

Open `app/mcp_server.py` and explain:

- Tools perform actions or retrieve specific data
- Resources expose readable knowledge
- Prompts standardize repeatable tasks

### 35–50 min — Use GitHub Copilot in VS Code

Run the demo prompts from this README.

### 50–60 min — Extension exercise

Ask participants to add one new tool:

```python
@mcp.tool
def list_customer_products(customer_id: str) -> list[str]:
    customer = internal_get(f"/customers/{customer_id}")
    return customer["active_products"]
```

Then ask Copilot:

```text
Use the internal MCP server to list the active products for customer CUST-1001.
```

---

## Security discussion points

This demo intentionally uses fake data. In a real organization, discuss:

- Internal allowlist for MCP servers
- Authentication and authorization
- Least privilege
- Audit logging
- Correlation IDs
- Output filtering
- No direct production database access
- API gateway usage
- Data classification
- Separate dev/test/prod environments

---

## Troubleshooting

### `uv` is not recognized

Restart the terminal after installing uv.

### API endpoint returns 401

Add the demo API key header:

```text
x-api-key: training-demo-key
```

### MCP server seems stuck

That is normal for stdio MCP servers. It waits for the MCP client.

### Port 8000 already in use

Change the port in `app/run_api.py` or stop the other process.
