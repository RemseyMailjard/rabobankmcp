# Exchange Rate MCP Server Resources

## Purpose

This MCP server helps users convert money from one currency to another by using live exchange rates.

It can be used by:

* Finance teams
* Customer service teams
* Banking employees
* Developers learning MCP
* Trainers demonstrating how AI can call external APIs

The goal of this server is to show how an AI assistant can use an MCP tool to retrieve real-time exchange rate data.

---

## Available Tool

### convert_currency

Converts an amount from one currency to another.

The tool needs three pieces of information:

| Input         | Description                    | Example |
| ------------- | ------------------------------ | ------- |
| amount        | The amount of money to convert | `100`   |
| from_currency | The currency you convert from  | `EUR`   |
| to_currency   | The currency you convert to    | `USD`   |

Example:

```text
Convert 100 EUR to USD
```

---

## Currency Codes

This server uses ISO 4217 three-letter currency codes.

Common examples:

| Code | Currency             |
| ---- | -------------------- |
| EUR  | Euro                 |
| USD  | United States Dollar |
| GBP  | British Pound        |
| JPY  | Japanese Yen         |
| CAD  | Canadian Dollar      |
| AUD  | Australian Dollar    |
| CHF  | Swiss Franc          |
| CNY  | Chinese Yuan         |
| SEK  | Swedish Krona        |
| NOK  | Norwegian Krone      |

---

## Example Use Case

A customer from the United States pays an invoice in USD.

The finance department in the Netherlands wants to know the value in EUR.

The assistant can call the `convert_currency` tool and return a simple explanation.

Example answer:

```text
500 USD is approximately 462.30 EUR, based on the latest available exchange rate.
```

---

## Good Prompt Examples

Good prompts include an amount, a source currency, and a target currency.

Examples:

```text
Convert 100 EUR to USD.
```

```text
How much is 250 GBP in EUR?
```

```text
I received 1500 USD from a customer. What is this worth in EUR?
```

```text
Convert 5000 JPY to USD and explain the result in simple business language.
```

---

## Bad Prompt Examples

These prompts are unclear because important information is missing.

```text
Convert money.
```

Problem: the amount and currencies are missing.

```text
Convert 100 to dollars.
```

Problem: the source currency is missing.

```text
What is this worth?
```

Problem: the amount and currency are missing.

---

## Common API Errors

| Error             | Meaning                                     |
| ----------------- | ------------------------------------------- |
| unsupported-code  | The currency code is not supported          |
| invalid-key       | The API key is missing or incorrect         |
| malformed-request | The API request was not formatted correctly |

---

## Important Notes

Exchange rates can change during the day.

The result should be treated as an estimate unless the organization uses an official internal finance rate.

For accounting, invoicing, or legal reporting, always verify the rate with the official finance system.

---

## Demo Scenario

### Scenario: Customer Payment Conversion

A customer pays an invoice in USD, but the company administration works in EUR.

The assistant should:

1. Understand the amount and currencies.
2. Call the `convert_currency` tool.
3. Explain the result clearly.
4. Mention that the result is based on the latest available exchange rate.

Example user question:

```text
A customer paid 1200 USD. What is that approximately in EUR?
```

Expected assistant behavior:

```text
The assistant calls the convert_currency tool with:
amount = 1200
from_currency = USD
to_currency = EUR
```

Then the assistant explains the result in normal business language.
