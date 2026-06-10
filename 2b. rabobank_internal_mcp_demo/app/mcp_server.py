import os
import httpx
from fastmcp import FastMCP

INTERNAL_API_BASE_URL = os.getenv("INTERNAL_API_BASE_URL", "http://127.0.0.1:8000")

mcp = FastMCP("Rabobank Internal MCP Demo")

async def internal_get(path: str):
    """Small helper for calling the internal FastAPI API."""
    async with httpx.AsyncClient(base_url=INTERNAL_API_BASE_URL, timeout=10.0) as client:
        response = await client.get(path)
        response.raise_for_status()
        return response.json()

@mcp.tool
def get_customer_profile(customer_id: str) -> dict:
    """Retrieve a fake internal customer profile by customer ID."""
    return httpx.get(f"{INTERNAL_API_BASE_URL}/customers/{customer_id}", timeout=10.0).json()

@mcp.tool
def get_product_info(product_id: str) -> dict:
    """Retrieve fake internal product information by product ID."""
    return httpx.get(f"{INTERNAL_API_BASE_URL}/products/{product_id}", timeout=10.0).json()

@mcp.tool
def get_api_endpoint_info(api_name: str) -> dict:
    """Retrieve internal API catalog information for a named API."""
    return httpx.get(f"{INTERNAL_API_BASE_URL}/apis/{api_name}", timeout=10.0).json()

@mcp.tool
def run_architecture_check(service_name: str) -> dict:
    """Run a fake internal architecture review check for a service."""
    return httpx.get(f"{INTERNAL_API_BASE_URL}/architecture/check/{service_name}", timeout=10.0).json()

@mcp.resource("policy://api-security")
def api_security_policy() -> str:
    """Internal API security policy for demo purposes."""
    result = httpx.get(f"{INTERNAL_API_BASE_URL}/policies/api-security", timeout=10.0).json()
    return result["content"]

@mcp.resource("architecture://event-driven-standards")
def event_driven_standards() -> str:
    """Internal event-driven architecture standards for demo purposes."""
    result = httpx.get(f"{INTERNAL_API_BASE_URL}/policies/event-driven-standards", timeout=10.0).json()
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

if __name__ == "__main__":
    mcp.run()
