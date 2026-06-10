#!/usr/bin/env bash
set -euo pipefail

curl http://127.0.0.1:8000/health
curl -H "x-api-key: training-demo-key" http://127.0.0.1:8000/customers/CUST-1001
curl -H "x-api-key: training-demo-key" http://127.0.0.1:8000/products/MORTGAGE-FLEX
curl -H "x-api-key: training-demo-key" http://127.0.0.1:8000/apis/customer-onboarding
