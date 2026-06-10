from fastapi import FastAPI, HTTPException
from app.data import CUSTOMERS, PRODUCTS, API_CATALOG, POLICIES

app = FastAPI(
    title="Internal Banking API Demo",
    description="Fake internal API for MCP server training. Contains no real Rabobank data.",
    version="1.0.0"
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "internal-banking-api-demo"}

@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    customer = CUSTOMERS.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/apis/{api_name}")
def get_api(api_name: str):
    api = API_CATALOG.get(api_name)
    if not api:
        raise HTTPException(status_code=404, detail="API not found")
    return api

@app.get("/policies/{policy_name}")
def get_policy(policy_name: str):
    policy = POLICIES.get(policy_name)
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return {"policy_name": policy_name, "content": policy}

@app.get("/architecture/check/{service_name}")
def architecture_check(service_name: str):
    return {
        "service_name": service_name,
        "result": "Review required",
        "findings": [
            "Confirm OAuth2 client credentials or workload identity.",
            "Add correlation ID to all inbound and outbound calls.",
            "Check whether the service emits domain events for important state changes.",
            "Verify that no production data is exposed to developer tooling."
        ],
        "recommendation": "Schedule architecture review before production release."
    }
