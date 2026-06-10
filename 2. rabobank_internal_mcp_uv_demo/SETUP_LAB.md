# Setup Lab: Run the Internal MCP Demo with uv

This lab shows how to set up the demo, start the internal API, start the MCP server, and use a sample Copilot prompt against the server.

## Goal

By the end of this lab, you will have:

- Installed `uv`
- Synced the project dependencies
- Started the internal FastAPI service
- Started the MCP server with `uv`
- Used an example prompt to exercise the MCP server

## Prerequisites

- Windows, macOS, or Linux
- Python 3.11 or later
- `uv` installed and available on your `PATH`

Check `uv` first:

```bash
uv --version
```

If you do not have `uv`, install it on Windows with:

```powershell
winget install astral-sh.uv
```

## Step 1: Install dependencies

From the project folder, run:

```bash
uv sync
```

This creates the virtual environment and installs the project dependencies from `pyproject.toml`.

## Step 2: Start the internal API

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

## Step 3: Start the MCP server

Open a second terminal in the same project folder and run:

```bash
uv run bank-mcp
```

The MCP server uses stdio transport, so it may look idle. That is expected.

## Step 4: Use an example prompt

In GitHub Copilot Chat or any MCP-enabled client connected to this demo, try this prompt:

```text
Use the internal MCP server to retrieve customer CUST-1001 and summarize the active products.
```

If you want a product-focused prompt, use:

```text
Use the internal MCP server to explain product MORTGAGE-FLEX for a developer who needs to call the product API.
```

## Expected result

If everything is working, the MCP server should respond with data from the demo API and summarize it in plain language.

## Extend the MCP server

Developers can add new functionality by editing [app/mcp_server.py](app/mcp_server.py) and restarting the server with `uv run bank-mcp`.

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
4. Update the lab or README with a short example if the new capability should be discoverable

Example developer prompt for validation:

```text
Use the new calculation tool to estimate a monthly payment for a loan with principal 250000, annual rate 4.5, and 360 months.
```

## Quick checklist

- `uv --version` works
- `uv sync` completes successfully
- `uv run bank-api` is running in one terminal
- `uv run bank-mcp` is running in a second terminal
- A Copilot prompt can call the MCP server and return demo data
