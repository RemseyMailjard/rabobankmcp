"""Internal MCP server wrapping the fake internal banking API.

Run with:
    uv run bank-mcp
"""

from __future__ import annotations

import os
from typing import Any

import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

INTERNAL_API_BASE_URL = os.getenv("INTERNAL_API_BASE_URL", "http://127.0.0.1:8000")
DEMO_API_KEY = os.getenv("DEMO_API_KEY", "training-demo-key")

mcp = FastMCP("Internal Banking MCP Demo")


def _headers() -> dict[str, str]:
    return {
        "x-api-key": DEMO_API_KEY,
        "x-correlation-id": "mcp-training-demo",
    }


def internal_get(path: str) -> dict[str, Any]:
    with httpx.Client(base_url=INTERNAL_API_BASE_URL, timeout=10.0, headers=_headers()) as client:
        response = client.get(path)
        response.raise_for_status()
        return response.json()


def internal_post(path: str, payload: dict[str, Any]) -> dict[str, Any]:
    with httpx.Client(base_url=INTERNAL_API_BASE_URL, timeout=10.0, headers=_headers()) as client:
        response = client.post(path, json=payload)
        response.raise_for_status()
        return response.json()


@mcp.tool
def get_customer_profile(customer_id: str) -> dict[str, Any]:
    """Retrieve a fake internal customer profile by customer ID.

    Example customer IDs: CUST-1001, CUST-2002.
    """
    return internal_get(f"/customers/{customer_id}")


@mcp.tool
def get_product_info(product_id: str) -> dict[str, Any]:
    """Retrieve fake internal product information by product ID.

    Example product IDs: MORTGAGE-FLEX, PAYMENT-PLUS, BUSINESS-ACCOUNT.
    """
    return internal_get(f"/products/{product_id}")


@mcp.tool
def get_api_endpoint_info(api_name: str) -> dict[str, Any]:
    """Retrieve API catalog information for an internal API.

    Example API names: customer-onboarding, product-catalog.
    """
    return internal_get(f"/apis/{api_name}")


@mcp.tool
def run_architecture_check(service_name: str) -> dict[str, Any]:
    """Run a fake internal architecture check for a service."""
    return internal_post("/architecture/check", {"service_name": service_name})


@mcp.resource("policy://api-security")
def api_security_policy() -> str:
    """Internal API security policy for demo purposes."""
    result = internal_get("/policies/api-security")
    return result["content"]


@mcp.resource("architecture://event-driven-standards")
def event_driven_standards() -> str:
    """Internal event-driven architecture standards for demo purposes."""
    result = internal_get("/policies/event-driven-standards")
    return result["content"]


@mcp.prompt
def api_security_review_prompt(api_name: str, endpoint: str) -> str:
    """Reusable review prompt for checking an API endpoint against internal standards."""
    return f"""
You are reviewing an internal banking API.

API name: {api_name}
Endpoint: {endpoint}

Use the policy://api-security resource.
Check whether this endpoint follows the internal API security policy.
Return:
1. What looks compliant
2. What is missing
3. Questions for the API owner
4. Recommended next steps
""".strip()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
