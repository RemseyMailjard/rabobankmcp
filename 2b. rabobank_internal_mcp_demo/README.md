# Rabobank Internal MCP Demo

A minimal but realistic training project for a 1-hour MCP session.

It contains:

1. **Internal FastAPI API** – simulates approved internal Rabobank services.
2. **MCP server** – exposes selected internal capabilities as MCP tools, resources and prompts.
3. **GitHub Copilot in VS Code config example** – shows how an internal MCP server could be added locally.

> Demo goal: show developers how GitHub Copilot can use an internal MCP server without connecting to public MCP servers.

---

## Scenario

A developer wants to explore internal banking APIs and standards without manually searching documentation.

The MCP server exposes:

### Tools

- `get_customer_profile(customer_id)`
- `get_product_info(product_id)`
- `get_api_endpoint_info(api_name)`
- `run_architecture_check(service_name)`

### Resources

- `policy://api-security`
- `architecture://event-driven-standards`

### Prompt

- `api_security_review_prompt(api_name, endpoint)`

---

## Project structure

```text
rabobank_internal_mcp_demo/
├─ app/
│  ├─ internal_api.py      # Fake internal FastAPI API
│  ├─ mcp_server.py        # MCP server that wraps the internal API
│  └─ data.py              # Demo data
├─ .vscode/
│  └─ mcp.json             # Example VS Code MCP config
├─ requirements.txt
└─ README.md
```

---

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows PowerShell/CMD
# source .venv/bin/activate    # macOS/Linux
pip install -r requirements.txt
```

---

## Step 1: Run the internal API

```bash
uvicorn app.internal_api:app --reload --port 8000
```

Test it:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/customers/CUST-1001
curl http://127.0.0.1:8000/products/MORTGAGE-FLEX
curl http://127.0.0.1:8000/apis/customer-onboarding
```

FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

---

## Step 2: Run the MCP server

Open a second terminal:

```bash
python app/mcp_server.py
```

This starts the MCP server using stdio transport, which is useful for local IDE demos.

---

## Step 3: Example prompts for GitHub Copilot in VS Code

Use these prompts once the MCP server is connected in VS Code:

```text
Use the internal MCP server to retrieve customer CUST-1001 and summarize the active products.
```

```text
Use the internal MCP server to explain product MORTGAGE-FLEX for a developer who needs to call the product API.
```

```text
Use the internal MCP server to inspect the customer-onboarding API and tell me which endpoint creates a new onboarding case.
```

```text
Use the API security policy resource and review the customer-onboarding /onboarding/cases endpoint.
```

```text
Run an architecture check for CustomerOnboardingService and summarize the risks.
```

---

## VS Code MCP configuration example

See `.vscode/mcp.json`.

You may need to adjust the Python path depending on your environment.

---

## Trainer storyline

1. Show the internal API in FastAPI docs.
2. Explain that this represents approved internal systems.
3. Show that the MCP server exposes only selected capabilities.
4. Explain tools, resources and prompts.
5. Run Copilot prompts.
6. Discuss how this could map to real internal APIs, policies and architecture standards.

---

## Security talking points

This demo intentionally keeps data fake.

In a real enterprise implementation, add:

- Authentication and authorization
- Least privilege access
- Audit logging
- Input validation
- Output filtering
- No direct access to production databases
- Approved API gateway usage
- Environment separation: dev, test, prod
- Allowlist process for MCP servers
