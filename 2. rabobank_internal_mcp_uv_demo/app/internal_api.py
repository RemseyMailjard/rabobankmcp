"""Fake internal FastAPI service.

This simulates approved internal APIs that an MCP server can wrap.
"""

from fastapi import FastAPI, Header, HTTPException
from app.data import API_CATALOG, CUSTOMERS, POLICIES, PRODUCTS

DEMO_API_KEY = "training-demo-key"

app = FastAPI(
    title="Internal Banking API Demo",
    description="Fake internal API for MCP server training. Contains no real Rabobank data.",
    version="0.1.0",
)


def require_demo_api_key(x_api_key: str | None) -> None:
    """Tiny demo auth check to make the internal API feel realistic."""
    if x_api_key != DEMO_API_KEY:
        raise HTTPException(status_code=401, detail="Missing or invalid demo API key")


@app.get("/health")
def health():
    return {"status": "ok", "service": "internal-banking-api-demo"}


@app.get("/customers/{customer_id}")
def get_customer(customer_id: str, x_api_key: str | None = Header(default=None)):
    require_demo_api_key(x_api_key)
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.get("/products/{product_id}")
def get_product(product_id: str, x_api_key: str | None = Header(default=None)):
    require_demo_api_key(x_api_key)
    product = PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.get("/apis/{api_name}")
def get_api(api_name: str, x_api_key: str | None = Header(default=None)):
    require_demo_api_key(x_api_key)
    api = API_CATALOG.get(api_name)
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    return api


@app.get("/policies/{policy_name}")
def get_policy(policy_name: str, x_api_key: str | None = Header(default=None)):
    require_demo_api_key(x_api_key)
    policy = POLICIES.get(policy_name)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {"policy_name": policy_name, "content": policy}


@app.post("/architecture/check")
def architecture_check(payload: dict, x_api_key: str | None = Header(default=None)):
    require_demo_api_key(x_api_key)
    service_name = payload.get("service_name", "UnknownService")
    return {
        "service_name": service_name,
        "result": "Review required",
        "findings": [
            "Confirm OAuth2 client credentials or workload identity.",
            "Add a correlation ID to all inbound and outbound calls.",
            "Check whether important state changes are emitted as domain events.",
            "Verify that no production data is exposed to developer tooling.",
        ],
        "recommendation": "Schedule architecture review before production release.",
    }
