# Minimal MCP Server Demo and Lab with uv, FastMCP and VS Code

This combined guide starts with the minimal setup for a working MCP server and continues into a hands-on lab where you extend that server with participant-friendly banking tools.

## Contents

- 1. Install uv on Windows or macOS
- 2. Create a new MCP project
- 3. Add FastMCP
- 4. Create the minimal MCP server
- 5. Run the MCP server over HTTP
- 6. Important: do not test /mcp as a normal webpage
- 7. Connect the MCP server to VS Code
- 8. Start the MCP server in VS Code
- 9. Use the MCP tool in GitHub Copilot Chat
- 10. What to explain during the demo
- Part 1 Summary
- Goal
- Scenario
- Learning Objectives
- Business Scenario
- Task 1. Create a new MCP project
- Task 2. Install FastMCP
- Task 3. Create your first MCP server
- Task 4. Create the account balance tool
- Task 5. Create the customer lookup tool
- Task 6. Create the branch information tool
- Task 7. Run the MCP server
- Task 8. Connect GitHub Copilot
- Task 9. Test the MCP tools
- Challenge Exercise
- Reflection Questions
- Expected Outcome
- Key Takeaway

## 1. Install uv on Windows or macOS

On Windows, open PowerShell and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart your terminal and verify the installation:

```powershell
uv --version
```

Optional: install Python through uv:

```powershell
uv python install 3.12
```

On macOS, you can install uv with Homebrew or the official install script.

Homebrew:

```bash
brew install uv
```

Official install script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal and verify the installation:

```bash
uv --version
```

Optional: install Python through uv:

```bash
uv python install 3.12
```

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

## 3. Add FastMCP

Install FastMCP into the project:

```powershell
uv add fastmcp
```

For this minimal demo, `fastapi` and `requests` are not needed.

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

## 6. Important: do not test /mcp as a normal webpage

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

This is expected. The `/mcp` endpoint is not a normal website or REST API endpoint. It is meant to be used by an MCP-compatible client.

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

## 8. Start the MCP server in VS Code

Make sure your HTTP MCP server is still running in the terminal.

Then open `.vscode/mcp.json`.

In VS Code, use the available MCP controls to start or detect the server.

After the server is detected, GitHub Copilot Chat can use the MCP tool.

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

## 10. What to explain during the demo

You can explain it like this:

```text
This is a minimal internal MCP server.
It exposes one approved tool to an AI client.
The AI assistant cannot directly access internal systems.
It can only call the tools that the MCP server exposes.
In this example, the approved tool is get_account_balance.
```

## Part 1 Summary

The main command flow is:

- Project setup: `uv init first-mcp-server`
- Dependency install: `uv add fastmcp`
- Run server: `uv run fastmcp run main.py:mcp --transport http --port 8000`
- VS Code config: `.vscode/mcp.json`

Key learning point: an MCP server is not the AI assistant itself. It exposes approved tools that an AI client can call.

## Goal

Understand how an MCP server works and how AI assistants can securely interact with internal business systems through MCP tools.

## Scenario

Imagine you are a developer at a bank. Many internal systems contain useful information, but AI assistants cannot access them directly.

An MCP server acts as a controlled bridge between the AI assistant and internal systems. In this lab, you create your first MCP server and expose a few internal banking operations as MCP tools.

By the end of this exercise, GitHub Copilot should be able to discover and call your tools through the MCP protocol.

## Learning Objectives

After completing this lab, you should be able to:

- Explain the purpose of an MCP server and the relationship between MCP clients and MCP servers.
- Create MCP tools using FastMCP.
- Run an MCP server locally and connect it to GitHub Copilot.
- Test MCP tools through natural language prompts.

## Business Scenario

A fictional banking system contains customer, account, and branch information. Your MCP server should expose these operations:

- `get_account_balance`: Retrieve the balance of an account.
- `get_customer_name`: Retrieve a customer name.
- `get_branch_information`: Retrieve information about a branch office.
- For this lab, the data can be hardcoded. Later labs can connect to APIs and databases.

## Task 1. Create a New MCP Project

Create a new project using uv:

```powershell
uv init first-mcp-server
cd first-mcp-server
```

## Task 2. Install FastMCP

Add the required package:

```powershell
uv add fastmcp
```

## Task 3. Create Your First MCP Server

Create the MCP server skeleton in `main.py`:

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

## Task 4. Create the Account Balance Tool

Implement a tool that returns a balance for a given account number.

```python
ACCOUNTS = {
    "12345": {"customer_id": "1001", "balance": 1250.00, "currency": "EUR"},
    "67890": {"customer_id": "1002", "balance": 2480.75, "currency": "EUR"},
}


@mcp.tool()
def get_account_balance(account_number: str) -> str:
    account = ACCOUNTS.get(account_number)

    if account is None:
        return f"No account found for {account_number}."

    return (
        f"Account {account_number} has a balance of "
        f"{account['currency']} {account['balance']:.2f}"
    )
```

Example output:

```text
Account 12345 has a balance of EUR 1250.00
```

## Task 5. Create the Customer Lookup Tool

Implement a tool that returns customer information.

```python
CUSTOMERS = {
    "1001": "John Smith",
    "1002": "Aisha Khan",
}


@mcp.tool()
def get_customer_name(customer_id: str) -> str:
    customer_name = CUSTOMERS.get(customer_id)

    if customer_name is None:
        return f"No customer found for {customer_id}."

    return f"Customer {customer_id} is {customer_name}"
```

Example output:

```text
Customer 1001 is John Smith
```

## Task 6. Create the Branch Information Tool

Implement a tool that returns branch information.

```python
BRANCHES = {
    "BR001": {
        "location": "Utrecht",
        "opening_hours": "09:00 - 17:00",
        "services": ["Daily banking", "Mortgage advice", "Business support"],
    }
}


@mcp.tool()
def get_branch_information(branch_code: str) -> str:
    branch = BRANCHES.get(branch_code)

    if branch is None:
        return f"No branch found for {branch_code}."

    services = ", ".join(branch["services"])
    return (
        f"Branch {branch_code}\n"
        f"Location: {branch['location']}\n"
        f"Opening Hours: {branch['opening_hours']}\n"
        f"Services: {services}"
    )
```

Example output:

```text
Branch BR001
Location: Utrecht
Opening Hours: 09:00 - 17:00
Services: Daily banking, Mortgage advice, Business support
```

## Task 7. Run the MCP Server

Start the server and verify that it launches successfully:

```powershell
uv run fastmcp run main.py:mcp --transport http --port 8000
```

## Task 8. Connect GitHub Copilot

Configure GitHub Copilot to use the MCP server. Create:

```text
.vscode/mcp.json
```

Add:

```json
{
  "servers": {
    "rabobank-demo": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Verify that the tools are discovered in GitHub Copilot Chat.

## Task 9. Test the MCP Tools

Try prompts like these and observe which MCP tool is invoked:

```text
What is the balance of account 12345?
What is the name of customer 1001?
Show information about branch BR001.
```

## Challenge Exercise

Add a new tool:

```python
get_exchange_rate(currency)
```

Examples:

```text
USD -> EUR
GBP -> EUR
CHF -> EUR
```

Allow GitHub Copilot to retrieve exchange rates through the MCP server.

## Reflection Questions

- Why would an organization use an MCP server instead of giving direct database access to an AI assistant?
- What advantages does MCP provide compared to hardcoding business logic inside prompts?
- What security benefits are gained by exposing only approved tools?
- Which internal systems in your organization could benefit from an MCP server?

## Expected Outcome

At the end of the lab, you should be able to ask GitHub Copilot questions such as:

```text
What is the balance of account 12345?
What is the name of customer 1001?
Show me information about branch BR001.
```

GitHub Copilot should automatically discover and call the appropriate MCP tool.

Your MCP server should now include:

- One MCP server
- Account balance tool
- Customer lookup tool
- Branch information tool
- GitHub Copilot MCP connection
- Validated prompts that call the right tool

## Key Takeaway

### Tools

Tools are functions the AI client can call to reach approved business functionality.

```text
What is the balance of account 12345?
```

### Key takeaway

An MCP server acts as a secure integration layer between AI assistants and internal systems.

By exposing carefully designed tools, organizations can give AI access to business functionality without exposing databases, APIs, or sensitive infrastructure directly.

## Lab 2. Add Simulated Internal Data

Replace `main.py` with:

```python
from fastmcp import FastMCP

mcp = FastMCP("Internal Bank MCP Server")

accounts = {
    "NL91RABO0123456789": {
        "name": "Contoso Retail BV",
        "balance": 1250.00,
        "currency": "EUR"
    },
    "NL44RABO0987654321": {
        "name": "Fabrikam Logistics",
        "balance": 9850.75,
        "currency": "EUR"
    }
}


@mcp.tool()
def get_account_balance(account_number: str) -> str:
    """Get the balance for an internal bank account."""
    account = accounts.get(account_number)

    if account is None:
        return f"No account found for {account_number}"

    return (
        f"Account: {account_number}\n"
        f"Customer: {account['name']}\n"
        f"Balance: {account['currency']} {account['balance']:.2f}"
    )


if __name__ == "__main__":
    mcp.run()
```

Test prompt:

```text
Get the account balance for NL44RABO0987654321.
```

## Lab 3. Add a Second Tool

Add this function below `get_account_balance`:

```python
@mcp.tool()
def get_customer_profile(account_number: str) -> str:
    """Get basic customer information for an account."""
    account = accounts.get(account_number)

    if account is None:
        return f"No customer profile found for {account_number}"

    return (
        f"Customer name: {account['name']}\n"
        f"Account number: {account_number}\n"
        f"Customer type: Business customer"
    )
```

Test prompt:

```text
Get the customer profile for account NL91RABO0123456789.
```

Discovery prompt:

```text
What can I do with this MCP server?
```

## Lab 4. Add Transactions

Extend the data:

```python
transactions = {
    "NL91RABO0123456789": [
        {"date": "2026-06-01", "description": "Invoice payment", "amount": 450.00},
        {"date": "2026-06-03", "description": "Office supplies", "amount": -89.95},
        {"date": "2026-06-05", "description": "Subscription fee", "amount": -29.99}
    ],
    "NL44RABO0987654321": [
        {"date": "2026-06-02", "description": "Client payment", "amount": 2500.00},
        {"date": "2026-06-04", "description": "Transport costs", "amount": -340.50}
    ]
}
```

Add this tool:

```python
@mcp.tool()
def list_recent_transactions(account_number: str) -> str:
    """List recent transactions for an internal bank account."""
    account_transactions = transactions.get(account_number)

    if account_transactions is None:
        return f"No transactions found for {account_number}"

    result = f"Recent transactions for {account_number}:\n"

    for transaction in account_transactions:
        result += (
            f"- {transaction['date']} | "
            f"{transaction['description']} | "
            f"EUR {transaction['amount']:.2f}\n"
        )

    return result
```

Test prompt:

```text
List the recent transactions for NL91RABO0123456789.
```

## Lab 5. Add Simple Risk Analysis

Add this tool:

```python
@mcp.tool()
def analyze_account_risk(account_number: str) -> str:
    """Analyze simple risk indicators for an account."""
    account = accounts.get(account_number)
    account_transactions = transactions.get(account_number, [])

    if account is None:
        return f"No account found for {account_number}"

    negative_transactions = [
        t for t in account_transactions if t["amount"] < 0
    ]

    if account["balance"] < 0:
        risk_level = "High"
        reason = "The account has a negative balance."
    elif len(negative_transactions) >= 3:
        risk_level = "Medium"
        reason = "The account has multiple outgoing transactions."
    else:
        risk_level = "Low"
        reason = "No major risk indicators were found."

    return (
        f"Risk level: {risk_level}\n"
        f"Reason: {reason}"
    )
```

Test prompt:

```text
Analyze the risk for account NL91RABO0123456789.
```

## Lab 6. Add a Resource

Resources are read-only data that the AI client can inspect.

Add this:

```python
@mcp.resource("bank://policy/account-review")
def account_review_policy() -> str:
    """Internal account review policy."""
    return """
Internal Account Review Policy

1. Always verify the account number.
2. Never expose sensitive personal data.
3. Use account balance and transaction history only for business purposes.
4. Escalate accounts with negative balances.
5. Keep auditability in mind when using AI-assisted analysis.
"""
```

Test prompt:

```text
Read the internal account review policy from the MCP server and summarize it.
```

## Lab 7. Add a Prompt Template

Prompts are reusable instructions exposed by the MCP server.

Add this:

```python
@mcp.prompt()
def account_review_prompt(account_number: str) -> str:
    """Create a structured prompt for reviewing an account."""
    return f"""
Review account {account_number}.

Use the available MCP tools to:
1. Get the account balance.
2. Get the customer profile.
3. List recent transactions.
4. Analyze account risk.

Return the result as a short business summary.
"""
```

Test prompt:

```text
Use the account review prompt for account NL91RABO0123456789.
```

## Lab 8. Final Challenge

Add a new tool yourself:

```text
detect_large_transactions
```

The tool should:

1. Accept an account number.
2. Accept a minimum amount.
3. Return all transactions above that amount.
4. Return a clear message if none are found.

Suggested function signature:

```python
@mcp.tool()
def detect_large_transactions(account_number: str, minimum_amount: float) -> str:
    """Detect transactions above a certain amount."""
    pass
```

## Lab Checklist

Your MCP server should now include:

- One MCP server
- Account balance tool
- Customer profile tool
- Recent transactions tool
- Risk analysis tool
- Internal policy resource
- Account review prompt
- Final challenge tool

## Lab Summary

### Tools

Tools are functions the AI client can call.

```text
Get the balance for this account.
```

### Resources

Resources are read-only data sources.

```text
Read the internal account review policy.
```

### Prompts

Prompts are reusable templates.

```text
Use the account review prompt.
```

### Enterprise lesson

An MCP server allows developers to expose internal functionality in a controlled way.

The AI assistant does not get unlimited access. It only gets access to the tools, resources and prompts that the server provides.
