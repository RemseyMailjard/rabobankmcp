# Lab: Build an Internal MCP Server Step by Step

## Goal

In this lab, you will build a minimal internal MCP server and gradually extend it with extra capabilities.

You will learn how to expose:

* Tools
* Resources
* Prompts
* Simulated internal data
* Basic validation and error handling

The example is based on a fictional internal banking scenario.

---

# Lab 0 — Project Setup

## Step 1: Create the project

```powershell
uv init internal-bank-mcp-server
cd internal-bank-mcp-server
uv add fastmcp
```

## Step 2: Create the first server

Replace `main.py` with:

```python
from fastmcp import FastMCP

mcp = FastMCP("Internal Bank MCP Server")


@mcp.tool()
def get_account_balance(account_number: str) -> str:
    """Get the balance for an internal bank account."""
    return f"Account {account_number} has a balance of €1,250.00"


if __name__ == "__main__":
    mcp.run()
```

## Step 3: Run the server

```powershell
uv run fastmcp run main.py:mcp --transport http --port 8000
```

---

# Lab 1 — Connect to VS Code

Create:

```text
.vscode/mcp.json
```

Add:

```json
{
  "servers": {
    "internal-bank-demo": {
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

In GitHub Copilot Chat, use Agent Mode and ask:

```text
Use the internal-bank-demo MCP server to get the balance for account NL91RABO0123456789.
```

---

# Lab 2 — Add Simulated Internal Data

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

---

# Lab 3 — Add a Second Tool

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

---

# Lab 4 — Add Transactions

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

---

# Lab 5 — Add Simple Risk Analysis

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

---

# Lab 6 — Add a Resource

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

---

# Lab 7 — Add a Prompt Template

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

---

# Lab 8 — Final Challenge

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

---

# Final Version Checklist

Your MCP server should now include:

* One MCP server
* Account balance tool
* Customer profile tool
* Recent transactions tool
* Risk analysis tool
* Internal policy resource
* Account review prompt
* Final challenge tool

---

# Key Learning Summary

## Tools

Tools are functions the AI client can call.

Example:

```text
Get the balance for this account.
```

## Resources

Resources are read-only data sources.

Example:

```text
Read the internal account review policy.
```

## Prompts

Prompts are reusable templates.

Example:

```text
Use the account review prompt.
```

## Enterprise lesson

An MCP server allows developers to expose internal functionality in a controlled way.

The AI assistant does not get unlimited access.
It only gets access to the tools, resources and prompts that the server provides.
