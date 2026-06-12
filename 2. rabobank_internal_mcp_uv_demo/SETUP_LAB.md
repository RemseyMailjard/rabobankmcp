# Internal MCP Server Demo and Setup Lab with uv, FastAPI and FastMCP

This combined guide explains the internal MCP demo, shows how to run it with `uv`, and continues into a lab for extending the server with new tools, resources, and prompts.

## Contents

- Project overview
- Learning goal
- Scenario
- Project structure
- Available MCP tools
- Available MCP resources
- Available MCP prompt
- Prerequisite: uv
- Step 1. Install dependencies
- Step 2. Start the internal API
- Step 3. Start the MCP server
- Step 4. Connect in Visual Studio Code
- Step 5. Use example prompts
- Expected result
- Extend the MCP server
- Trainer flow for 1 hour
- Security discussion points
- Troubleshooting
- Quick checklist

## Project overview

This demo is a minimal but realistic training project for a 1-hour MCP session with developers.

It demonstrates how GitHub Copilot in Visual Studio Code can use an internal MCP server to safely access approved internal APIs, documentation, and review prompts.

All data is fictional. No real Rabobank data is included.

## Learning goal

Developers learn that an MCP server can act as a controlled AI-facing layer over internal systems.

```text
GitHub Copilot in VS Code
          |
          v
      MCP Client
          |
          v
 Internal MCP Server
          |
 +--------+--------+-------------+
 |        |        |             |
 v        v        v             v
Internal  API      Policies      Architecture
API       Catalog  / Standards   Checks
```

## Scenario

A developer wants to explore internal banking APIs and standards without manually searching documentation.

The MCP server exposes selected tools, resources, and prompts for that scenario.

## Project structure

```text
rabobank_internal_mcp_uv_demo/
|- app/
|  |- data.py
|  |- internal_api.py
|  |- mcp_server.py
|  |- run_api.py
|  \- __init__.py
|- .vscode/
|  |- mcp.json
|  \- tasks.json
|- scripts/
|  |- demo-calls.ps1
|  \- demo-calls.sh
|- .env.example
|- .python-version
|- pyproject.toml
|- uv.lock
\- SETUP_LAB.md
```

## Available MCP tools

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

## Available MCP resources

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

## Available MCP prompt

### `api_security_review_prompt(api_name, endpoint)`

Example prompt:

```text
Use the api_security_review_prompt for the customer-onboarding API and endpoint /onboarding/cases.
```

## Prerequisite: uv

Check if `uv` is available:

```bash
uv --version
```

Install `uv` on Windows:

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

## Step 1. Install dependencies

From the project folder, run:

```bash
uv sync
```

This creates the virtual environment and installs the project dependencies from `pyproject.toml`.

## Step 2. Start the internal API

Open a terminal in the project folder and run:

```bash
uv run bank-api
```

Leave that terminal running. The API should be available at:

```text
http://127.0.0.1:8000
```

You can verify it in a browser with:

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

## Step 3. Start the MCP server

Normally VS Code starts the MCP server using `.vscode/mcp.json`.

For a manual smoke test, open a second terminal in the same project folder and run:

```bash
uv run bank-mcp
```

The MCP server uses stdio transport, so it may look idle. That is expected.

## Step 4. Connect in Visual Studio Code

The example config is in:

```text
.vscode/mcp.json
```

It starts the MCP server with:

```bash
uv run bank-mcp
```

Important: keep the internal API running in the first terminal.

## Step 5. Use example prompts

In GitHub Copilot Chat or any MCP-enabled client connected to this demo, try:

```text
Use the internal MCP server to retrieve customer CUST-1001 and summarize the active products.
```

Product-focused prompt:

```text
Use the internal MCP server to explain product MORTGAGE-FLEX for a developer who needs to call the product API.
```

API-focused prompt:

```text
Use the internal MCP server to inspect the customer-onboarding API and tell me which endpoint creates a new onboarding case.
```

Resource-focused prompt:

```text
Use the policy://api-security resource and review the customer-onboarding /onboarding/cases endpoint.
```

Architecture prompt:

```text
Run an architecture check for CustomerOnboardingService and summarize the risks.
```

## Expected result

If everything is working, the MCP server should respond with data from the demo API and summarize it in plain language.

## Extend the MCP server

Developers can add new functionality by editing `app/mcp_server.py` and restarting the server with `uv run bank-mcp`.

Use the same patterns already in the demo:

- `@mcp.tool` for actions that return structured data
- `@mcp.resource` for read-only content that Copilot can inspect
- `@mcp.prompt` for reusable prompt templates

### 1. Add a new tool

Use a tool when Copilot needs to fetch or change data.

```python
@mcp.tool
def get_account_balance(account_id: str) -> dict[str, Any]:
    """Return a demo account balance by account ID."""
    return internal_get(f"/accounts/{account_id}")
```

Guidance:

- Keep the function name clear and action-focused
- Add a docstring with example inputs
- Return JSON-serializable data
- Prefer calling the internal API through `internal_get()` or `internal_post()` rather than embedding HTTP logic in every tool

### 2. Add a calculation tool

Use a calculation tool when the server should compute something for the assistant instead of leaving the math in the prompt.

```python
@mcp.tool
def calculate_monthly_payment(principal: float, annual_rate: float, months: int) -> dict[str, float]:
    """Calculate a simple monthly payment estimate for a loan."""
    monthly_rate = annual_rate / 12 / 100
    payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** (-months))
    return {
        "principal": principal,
        "annual_rate": annual_rate,
        "months": months,
        "estimated_monthly_payment": round(payment, 2),
    }
```

Guidance:

- Use calculations for repeatable business logic, not for prompt-only explanations
- Return both the inputs and the computed result when that helps Copilot reason about the output
- Keep the logic deterministic so the same inputs produce the same output

### 3. Add a resource

Use a resource for policy text, reference content, or other read-only material that Copilot may want to inspect during a task.

```python
@mcp.resource("policy://customer-data-handling")
def customer_data_handling_policy() -> str:
    """Return a short customer data handling policy for the demo."""
    result = internal_get("/policies/customer-data-handling")
    return result["content"]
```

Guidance:

- Use a stable URI-like name
- Return a string for text content or structured data only when that is the intended contract
- Keep resources read-only

### 4. Add a reusable prompt

Use a prompt when you want a standard review template or workflow that Copilot can invoke repeatedly.

```python
@mcp.prompt
def customer_onboarding_review_prompt(customer_id: str) -> str:
    """Reusable prompt for checking a customer onboarding case."""
    return f"""
You are reviewing customer onboarding for customer ID: {customer_id}

Use the available MCP tools and resources to:
1. Summarize the current onboarding state
2. Identify missing data or risks
3. Suggest the next operational step
""".strip()
```

Guidance:

- Keep prompts reusable and parameter-driven
- Describe the expected output clearly
- Reference the relevant resources or tools in the prompt body

### 5. Test the new functionality

After adding a tool, resource, calculation, or prompt:

1. Save the changes in `app/mcp_server.py`
2. Restart the MCP server with `uv run bank-mcp`
3. Call the new tool or prompt from Copilot Chat
4. Update the lab with a short example if the new capability should be discoverable

Example developer prompt for validation:

```text
Use the new calculation tool to estimate a monthly payment for a loan with principal 250000, annual rate 4.5, and 360 months.
```

## Trainer flow for 1 hour

### 0-10 min. Explain MCP

MCP is a standard way to let AI clients use tools, resources, and prompts from approved systems.

### 10-20 min. Show the internal API

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

### 20-35 min. Show the MCP server

Open `app/mcp_server.py` and explain:

- Tools perform actions or retrieve specific data
- Resources expose readable knowledge
- Prompts standardize repeatable tasks

### 35-50 min. Use GitHub Copilot in VS Code

Run the demo prompts from this guide.

### 50-60 min. Extension exercise

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

## Troubleshooting

### `uv` is not recognized

Restart the terminal after installing `uv`.

### API endpoint returns 401

Add the demo API key header:

```text
x-api-key: training-demo-key
```

### MCP server seems stuck

That is normal for stdio MCP servers. It waits for the MCP client.

### Port 8000 already in use

Change the port in `app/run_api.py` or stop the other process.

## Quick checklist

- `uv --version` works
- `uv sync` completes successfully
- `uv run bank-api` is running in one terminal
- `uv run bank-mcp` is running in a second terminal
- A Copilot prompt can call the MCP server and return demo data
