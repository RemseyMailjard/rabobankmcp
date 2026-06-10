"""Fake internal banking data for a safe MCP training demo.

No real Rabobank data is included. The names, IDs, services and policies are fictional.
"""

CUSTOMERS = {
    "CUST-1001": {
        "customer_id": "CUST-1001",
        "segment": "Retail Banking",
        "risk_profile": "Low",
        "active_products": ["PAYMENT-PLUS", "MORTGAGE-FLEX"],
        "relationship_since": "2018-04-12",
        "developer_note": "Demo record. No real personal data.",
    },
    "CUST-2002": {
        "customer_id": "CUST-2002",
        "segment": "SME Banking",
        "risk_profile": "Medium",
        "active_products": ["BUSINESS-ACCOUNT", "LOAN-SME"],
        "relationship_since": "2021-09-03",
        "developer_note": "Demo SME record. No real personal data.",
    },
}

PRODUCTS = {
    "MORTGAGE-FLEX": {
        "product_id": "MORTGAGE-FLEX",
        "name": "Flexible Mortgage",
        "domain": "Mortgages",
        "description": "Demo mortgage product with flexible repayment options.",
        "required_checks": ["income-check", "identity-verification", "risk-assessment"],
        "api_owner": "Mortgage Platform Team",
    },
    "PAYMENT-PLUS": {
        "product_id": "PAYMENT-PLUS",
        "name": "Payment Plus Account",
        "domain": "Payments",
        "description": "Demo payment account for daily banking scenarios.",
        "required_checks": ["identity-verification", "sanctions-screening"],
        "api_owner": "Payments API Team",
    },
    "BUSINESS-ACCOUNT": {
        "product_id": "BUSINESS-ACCOUNT",
        "name": "Business Current Account",
        "domain": "SME Banking",
        "description": "Demo account product for small and medium enterprises.",
        "required_checks": ["chamber-of-commerce-check", "ubo-check", "sanctions-screening"],
        "api_owner": "SME Banking Platform Team",
    },
}

API_CATALOG = {
    "customer-onboarding": {
        "api_name": "customer-onboarding",
        "owner": "Customer Platform Team",
        "classification": "Internal",
        "authentication": "OAuth2 client credentials or approved workload identity",
        "base_path": "/onboarding",
        "endpoints": [
            {"method": "POST", "path": "/onboarding/cases", "purpose": "Create onboarding case"},
            {"method": "GET", "path": "/onboarding/cases/{caseId}", "purpose": "Retrieve onboarding case status"},
            {"method": "POST", "path": "/onboarding/cases/{caseId}/documents", "purpose": "Upload required documents"},
        ],
    },
    "product-catalog": {
        "api_name": "product-catalog",
        "owner": "Product Platform Team",
        "classification": "Internal",
        "authentication": "OAuth2 client credentials or approved workload identity",
        "base_path": "/products",
        "endpoints": [
            {"method": "GET", "path": "/products/{productId}", "purpose": "Retrieve product details"},
            {"method": "GET", "path": "/products?domain={domain}", "purpose": "List products by domain"},
        ],
    },
}

POLICIES = {
    "api-security": """
API Security Policy - Demo

1. Internal APIs must use OAuth2 client credentials or approved workload identity.
2. Every request must include a correlation ID.
3. Sensitive data must only be returned when the caller has an approved business purpose.
4. Write operations must be logged for audit purposes.
5. APIs must validate input and reject unknown fields.
6. Production data must not be exposed to developer tooling.
7. API documentation must include authentication, authorization and error handling examples.
""".strip(),
    "event-driven-standards": """
Event-Driven Architecture Standards - Demo

1. Events must use domain-oriented names.
2. Events must include eventId, correlationId, source, timestamp and schemaVersion.
3. Consumers must be idempotent.
4. Event payloads must not contain unnecessary personal data.
5. Breaking schema changes require a new schema version.
""".strip(),
}
