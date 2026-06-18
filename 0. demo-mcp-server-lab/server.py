# /// script
# requires-python = ">=3.10"
# dependencies = ["fastmcp"]
# ///
"""
Rabobank MCP Workshop - Your First MCP Server with FastMCP
===========================================================

A single, coherent example that demonstrates ALL THREE MCP primitives in one
server, built around a synthetic mortgage / interest-rate advisory domain.

The point of this example is NOT the banking math - it is to make the
*control model* of each primitive tangible:

    TOOLS     -> model-controlled        the LLM decides when to call them (actions / compute)
    RESOURCES -> application-controlled   the app or user decides what context to load (read-only data)
    PROMPTS   -> user-controlled          a human deliberately triggers a reusable workflow

All data below is synthetic. No real customer or rate data is used.

------------------------------------------------------------------
Setup (uv)
------------------------------------------------------------------
The block at the top of this file is PEP 723 inline metadata: it declares the
dependencies, so uv installs them on the fly - no separate venv or install
step is needed.

    uv run server.py                 # runs over stdio (uv resolves FastMCP)

Inspect / test without a client:
    uv run fastmcp dev server.py     # opens the MCP Inspector in the browser

For a real project instead of a single file:
    uv init rabo-mcp-lab && cd rabo-mcp-lab
    uv add fastmcp
    uv run server.py

Connect from a client (Claude Desktop / VS Code) by registering this server in
the client's MCP config, e.g. command "uv" with args:
    ["run", "--with", "fastmcp", "fastmcp", "run", "/path/to/server.py"]
"""

from fastmcp import FastMCP

# The server instance. The name is what clients show in their UI.
mcp = FastMCP("rabo-mortgage-advisor")


# Synthetic "current" rate table. In a real server this would come from an
# internal rate service. We expose it below as a RESOURCE (not a tool) because
# it is read-only context the application loads - there is no action to perform.
MORTGAGE_RATES = {
    "annuity-10y-fixed": 3.65,
    "annuity-20y-fixed": 4.10,
    "annuity-30y-fixed": 4.35,
    "linear-20y-fixed": 4.05,
    "variable": 4.80,
}

# A bank-style affordability threshold: the maximum share of gross income that
# may go to housing costs. Synthetic value for the workshop.
MAX_DTI_RATIO = 0.30


# ==================================================================
# 1) TOOLS  -  model-controlled actions / computations
# ==================================================================
# The LLM reads the type hints + docstring (FastMCP turns these into a JSON
# Schema automatically) and decides on its own when a tool is useful.
# Tools MAY have side effects; these two are pure computations.

@mcp.tool
def calculate_monthly_payment(
    principal: float,
    annual_rate_pct: float,
    term_years: int,
) -> dict:
    """Calculate the monthly payment for an annuity mortgage.

    Args:
        principal: Loan amount in euros.
        annual_rate_pct: Nominal annual interest rate as a percentage, e.g. 3.65.
        term_years: Term of the loan in years.

    Returns:
        A breakdown with the monthly payment, total amount paid and total interest.
    """
    monthly_rate = annual_rate_pct / 100 / 12
    n = term_years * 12

    if monthly_rate == 0:
        monthly_payment = principal / n
    else:
        monthly_payment = principal * monthly_rate / (1 - (1 + monthly_rate) ** -n)

    total_paid = monthly_payment * n
    return {
        "monthly_payment": round(monthly_payment, 2),
        "total_paid": round(total_paid, 2),
        "total_interest": round(total_paid - principal, 2),
    }


@mcp.tool
def affordability_check(
    monthly_payment: float,
    gross_monthly_income: float,
) -> dict:
    """Check whether a monthly payment fits within a debt-to-income threshold.

    Args:
        monthly_payment: Proposed monthly housing cost in euros.
        gross_monthly_income: Gross monthly income in euros.

    Returns:
        The debt-to-income ratio and whether it stays within the bank's limit.
    """
    ratio = monthly_payment / gross_monthly_income
    return {
        "dti_ratio": round(ratio, 3),
        "max_allowed": MAX_DTI_RATIO,
        "within_limit": ratio <= MAX_DTI_RATIO,
    }

# DISCUSSION: a tool with a *real side effect* (e.g. logging an advice request
# to an internal system) would also live here. That side-effecting nature is
# exactly what separates a tool from a resource - and it is where audit logging
# and RBAC attach in an enterprise deployment.


# ==================================================================
# 2) RESOURCES  -  application-controlled, read-only data (context)
# ==================================================================
# Resources are addressed by a URI and behave like a GET: idempotent, no side
# effects. The application (or user) decides which resource to load as context;
# the model does not "invoke" them the way it invokes a tool.

@mcp.resource("rates://current")
def current_rates() -> dict:
    """The full table of current mortgage interest rates (synthetic)."""
    return MORTGAGE_RATES


# A RESOURCE TEMPLATE: the {product} segment is filled in at read time, so one
# function serves many addresses, e.g.  rates://mortgage/annuity-20y-fixed
@mcp.resource("rates://mortgage/{product}")
def rate_for_product(product: str) -> dict:
    """Look up the current interest rate for a single mortgage product."""
    rate = MORTGAGE_RATES.get(product)
    if rate is None:
        return {
            "product": product,
            "error": "unknown product",
            "available": list(MORTGAGE_RATES),
        }
    return {"product": product, "annual_rate_pct": rate}


# ==================================================================
# 3) PROMPT  -  user-controlled, reusable workflow
# ==================================================================
# A prompt is a template a human deliberately triggers (a slash-command in the
# client). This one ORCHESTRATES the primitives above: it tells the model to
# read the rate RESOURCE and then call the calculation + affordability TOOLS,
# and finish with a structured recommendation. This is the "aha" moment: tools,
# resources and prompts are not three ways to do the same thing - the prompt
# ties the other two together into one repeatable flow.

@mcp.prompt
def mortgage_advice(
    client_name: str,
    loan_amount: float,
    term_years: int,
    gross_monthly_income: float,
    product: str,
) -> str:
    """Guided mortgage-advice workflow for an advisor."""
    return (
        f"You are a mortgage advisor preparing advice for {client_name}.\n\n"
        f"Follow these steps:\n"
        f"1. Read the resource `rates://mortgage/{product}` to get the current "
        f"interest rate for the requested product.\n"
        f"2. Call `calculate_monthly_payment` with principal={loan_amount}, "
        f"the rate from step 1, and term_years={term_years}.\n"
        f"3. Call `affordability_check` with the resulting monthly payment and "
        f"gross_monthly_income={gross_monthly_income}.\n"
        f"4. Write a short, structured advice covering: the product and rate, "
        f"the monthly payment, the total interest over the term, and whether it "
        f"is affordable. If it is not within the limit, suggest one alternative.\n\n"
        f"Keep the tone factual. All figures are indicative."
    )


# ==================================================================
# Run the server (stdio transport - ideal for a first, local server).
# For a remote / shared server you would use:  mcp.run(transport="http")
# ==================================================================
if __name__ == "__main__":
    mcp.run()
