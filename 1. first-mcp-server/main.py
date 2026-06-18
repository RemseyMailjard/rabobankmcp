import os

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from pathlib import Path

load_dotenv()

mcp = FastMCP("Rabobank Demo MCP Server")

EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
EXCHANGE_RATE_API_BASE = "https://v6.exchangerate-api.com/v6"


ACCOUNTS = {
    "12345": {"customer_id": "1001", "balance": 1250.00, "currency": "EUR"},
    "67890": {"customer_id": "1002", "balance": 2480.75, "currency": "EUR"},
}

CUSTOMERS = {
    "1001": "John Smith",
    "1002": "Aisha Khan",
}

BRANCHES = {
    "BR001": {
        "location": "Utrecht",
        "opening_hours": "09:00 - 17:00",
        "services": ["Daily banking", "Mortgage advice", "Business support"],
    }
}


@mcp.tool()
def get_account_balance(account_number: str) -> str:
    """Get the balance of an internal account by account number."""
    account = ACCOUNTS.get(account_number)

    if account is None:
        return f"No account found for {account_number}."

    return (
        f"Account {account_number} has a balance of "
        f"{account['currency']} {account['balance']:.2f}"
    )


@mcp.tool()
def get_customer_name(customer_id: str) -> str:
    """Get the customer name by customer ID."""
    customer_name = CUSTOMERS.get(customer_id)

    if customer_name is None:
        return f"No customer found for {customer_id}."

    return f"Customer {customer_id} is {customer_name}"


@mcp.tool()
def get_branch_information(branch_code: str) -> str:
    """Get branch details by branch code."""
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


@mcp.tool()
def get_exchange_rate(currency: str) -> str:
    """Get the live exchange rate from the given currency to EUR using ExchangeRate-API."""
    base_currency = currency.upper()

    rates, error = _fetch_conversion_rates(base_currency)
    if error is not None:
        return error

    rate = rates.get("EUR")
    if rate is None:
        return f"No EUR exchange rate available for {base_currency}."

    return f"1 {base_currency} = {rate} EUR"



# Bonus exercise: integrate a public exchange-rate API as an MCP tool.
# This demonstrates calling a live, unauthenticated API (exchangerate.host)
# and returning the result as a tool response. Add this after the demo
# exchange rate method to show how to integrate external services.

def _fetch_conversion_rates(base_currency: str) -> tuple[dict[str, float] | None, str | None]:
    """Fetch live conversion rates for a base currency from ExchangeRate-API.

    Returns a tuple of (rates, error_message). Exactly one element is non-None.
    """
    if not EXCHANGE_RATE_API_KEY:
        return None, (
            "API key is missing. Set EXCHANGE_RATE_API_KEY as an environment variable."
        )

    url = f"{EXCHANGE_RATE_API_BASE}/{EXCHANGE_RATE_API_KEY}/latest/{base_currency}"

    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
    except httpx.HTTPError as exc:
        return None, f"Failed to reach exchange rate service: {exc}"

    data = response.json()

    if data.get("result") == "error":
        return None, f"API error: {data.get('error-type', 'unknown-error')}"

    rates = data.get("conversion_rates")
    if not rates:
        return None, "Unexpected response: no conversion rates returned."

    return rates, None


@mcp.tool()
def get_live_exchange_rate(from_currency: str, to_currency: str = "EUR") -> str:
    """Get the live exchange rate between two currencies using ExchangeRate-API.

    Args:
        from_currency: ISO 4217 base currency code, for example USD or GBP.
        to_currency: ISO 4217 target currency code, defaults to EUR.
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    rates, error = _fetch_conversion_rates(from_currency)
    if error is not None:
        return error

    rate = rates.get(to_currency)
    if rate is None:
        return f"Unsupported target currency: {to_currency}"

    return f"1 {from_currency} = {rate} {to_currency}"


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another using live exchange rates.

    Args:
        amount: The amount of money to convert.
        from_currency: ISO 4217 currency code to convert from, for example EUR or USD.
        to_currency: ISO 4217 currency code to convert to, for example USD or GBP.
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    rates, error = _fetch_conversion_rates(from_currency)
    if error is not None:
        return error

    rate = rates.get(to_currency)
    if rate is None:
        return f"Unsupported target currency: {to_currency}"

    converted_amount = amount * rate
    return (
        f"{amount:.2f} {from_currency} is approximately "
        f"{converted_amount:.2f} {to_currency}. "
        f"Exchange rate: 1 {from_currency} = {rate} {to_currency}"
    )

from pathlib import Path

@mcp.resource(
    "resources://exchange-rate-resource",
    name="Exchange Rate Resource",
    description="Markdown documentation with examples, currency codes, use cases, and common errors for the exchange rate MCP server."
)
def get_exchange_rate_resources() -> str:
    """Return the Markdown resource file for the exchange rate MCP server."""
    return Path("resources/exchange-rate-resource.md").read_text(encoding="utf-8")

@mcp.prompt(
    name="explain_exchange_rate_server",
    description="Explains what this MCP server does by using the exchange rate resource."
)
def explain_exchange_rate_server() -> str:
    """Create a prompt that explains the exchange rate MCP server."""
    return """
Read the resource `resources://exchange-rate-resource`.

Then explain in simple words:
1. What this MCP server does.
2. Which currency-related tools it offers.
3. One example question a user could ask.

Keep the explanation short and beginner-friendly.
"""



if __name__ == "__main__":
    mcp.run()