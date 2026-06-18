# Demo Scenarios

Ready-made test prompts for the Rabobank Demo MCP Server. Use these in GitHub Copilot
Chat (Agent mode) once the server is running and connected via `.vscode/mcp.json`.

## Demo Data

| Type | Values |
| --- | --- |
| Accounts | `12345` (EUR 1250.00), `67890` (EUR 2480.75) |
| Customers | `1001` (John Smith), `1002` (Aisha Khan) |
| Branch | `BR001` (Utrecht) |

Currency tools (`get_exchange_rate`, `get_live_exchange_rate`, `convert_currency`) use
live rates from ExchangeRate-API and require `EXCHANGE_RATE_API_KEY` in your `.env`.

## 1. Account Balance (`get_account_balance`)

```text
What is the balance of account 12345?
How much money is in account 67890?
Check the balance for account 99999.
```

Expected: balances for the first two; a "No account found" message for `99999`.

## 2. Customer Lookup (`get_customer_name`)

```text
What is the name of customer 1001?
Who is customer 1002?
Look up customer 5555.
```

Expected: `John Smith`, `Aisha Khan`, and a "No customer found" message for `5555`.

## 3. Branch Information (`get_branch_information`)

```text
Show information about branch BR001.
What are the opening hours of branch BR001?
Tell me about branch BR999.
```

Expected: Utrecht branch details (location, hours, services); a "No branch found"
message for `BR999`.

## 4. Exchange Rate to EUR (`get_exchange_rate`)

```text
What is the USD to EUR exchange rate?
How much is 1 GBP in EUR?
What is the current exchange rate for JPY to EUR?
```

Expected: a live rate like `1 USD = 0.86 EUR`.

## 5. Exchange Rate Between Two Currencies (`get_live_exchange_rate`)

```text
What is the live exchange rate from GBP to USD?
Show me the rate from EUR to JPY.
What is 1 USD worth in CHF?
```

Expected: a live rate like `1 GBP = 1.27 USD`.

## 6. Currency Conversion (`convert_currency`)

```text
Convert 100 USD to EUR.
How much is 250 GBP in JPY?
Convert 1000 EUR to USD.
```

Expected: a converted amount plus the exchange rate used.

## 7. Multi-Tool / Combined Prompts

These encourage the assistant to chain multiple tools in one conversation:

```text
What is the balance of account 12345, and how much is that in USD?
Who owns account 12345, and what is their branch BR001's opening hours?
Convert the balance of account 67890 to GBP.
```

Expected: the assistant calls several tools and combines the results.

## 8. Guardrail / Negative Prompts

Use these to show the assistant can only do what the tools allow:

```text
Transfer 500 EUR from account 12345 to account 67890.
Delete customer 1002.
Show me all accounts in the database.
```

Expected: the assistant cannot perform these — there is no tool for transfers,
deletions, or bulk listing. This demonstrates that only approved tools are exposed.
