$Headers = @{ "x-api-key" = "training-demo-key" }

Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
Invoke-RestMethod -Uri "http://127.0.0.1:8000/customers/CUST-1001" -Headers $Headers
Invoke-RestMethod -Uri "http://127.0.0.1:8000/products/MORTGAGE-FLEX" -Headers $Headers
Invoke-RestMethod -Uri "http://127.0.0.1:8000/apis/customer-onboarding" -Headers $Headers
