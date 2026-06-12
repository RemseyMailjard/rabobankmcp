from datetime import datetime, timezone
from typing import Any

from fastmcp import FastMCP

mcp = FastMCP("Rabobank Demo MCP Server")


ACCOUNTS = {
    "12345": {"customer_id": "1001", "balance": 1250.00, "currency": "EUR"},
    "67890": {"customer_id": "1002", "balance": 2480.75, "currency": "EUR"},
}

CUSTOMERS = {
    "1001": "John Smith",
    "1002": "Aisha Khan",
}

BRANCHES = {
    "BR001": {
        "location": "Utrecht",
        "opening_hours": "09:00 - 17:00",
        "services": ["Daily banking", "Mortgage advice", "Business support"],
    },
    "BR002": {
        "location": "Eindhoven",
        "opening_hours": "09:00 - 17:00",
        "services": ["Daily banking", "Investments", "Private banking"],
    },
}


def _infer_tags(tool_name: str, description: str) -> list[str]:
    """Infer lightweight categories from tool metadata."""
    text = f"{tool_name} {description}".lower()
    tags: set[str] = set()

    keyword_to_tag = {
        "account": "account",
        "balance": "account",
        "transaction": "transactions",
        "risk": "risk",
        "customer": "customer",
        "discover": "meta",
        "list": "meta",
        "tool": "meta",
    }

    for keyword, tag in keyword_to_tag.items():
        if keyword in text:
            tags.add(tag)

    if not tags:
        tags.add("general")

    return sorted(tags)


def _example_value_for_schema(param_schema: dict[str, Any]) -> Any:
    json_type = param_schema.get("type")

    if json_type == "string":
        return "example"
    if json_type == "integer":
        return 1
    if json_type == "number":
        return 1.0
    if json_type == "boolean":
        return True
    if json_type == "array":
        return []
    if json_type == "object":
        return {}

    return "value"


def _build_examples(tool_name: str, input_schema: dict[str, Any]) -> list[str]:
    props = input_schema.get("properties", {})
    required = input_schema.get("required", [])
    ordered_params = list(required) + [p for p in props if p not in required]

    if not ordered_params:
        return [
            f"Run {tool_name} using this MCP server.",
            f"Call {tool_name} and summarize the response.",
        ]

    arg_payload = {
        name: _example_value_for_schema(props.get(name, {})) for name in ordered_params
    }

    primary = ", ".join(ordered_params)
    return [
        f"Use {tool_name} with {primary} to complete my request.",
        f"Call {tool_name} with arguments {arg_payload}.",
    ]


async def _discover_tool_catalog(
    tag: str | None = None,
    include_auth: bool = False,
    compact: bool = False,
) -> dict[str, Any]:
    discovered_tools = await mcp.list_tools()
    requested_tag = tag.lower() if tag else None
    tool_items: list[dict[str, Any]] = []

    for tool in discovered_tools:
        tool_data = tool.model_dump()
        name = tool_data.get("name", "")
        description = tool_data.get("description") or "No description provided."
        input_schema = tool_data.get("parameters") or {
            "type": "object",
            "properties": {},
            "required": [],
        }

        explicit_tags = sorted(tool_data.get("tags") or [])
        inferred_tags = _infer_tags(name, description)
        combined_tags = sorted(set(explicit_tags + inferred_tags))

        if requested_tag and requested_tag not in [t.lower() for t in combined_tags]:
            continue

        item: dict[str, Any] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
            "examples": _build_examples(name, input_schema),
            "tags": combined_tags,
        }

        if compact:
            item = {
                "name": item["name"],
                "description": item["description"],
                "examples": item["examples"],
                "tags": item["tags"],
            }

        if include_auth:
            item["auth"] = {
                "required": bool(getattr(tool, "auth", None)),
                "details": "Configured by server metadata" if getattr(tool, "auth", None) else "none",
            }

        tool_items.append(item)

    return {
        "server": mcp.name,
        "discoverySchemaVersion": "1.0.0",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "toolCount": len(tool_items),
        "tools": tool_items,
        "examplePrompts": [
            "What can I do with this MCP server?",
            "Which tools are available?",
            "Show available capabilities",
            "Give examples of supported prompts",
        ],
    }

@mcp.tool()
def get_account_balance(account_number: str) -> str:
    """Get the balance for an internal Rabobank account."""
    account = ACCOUNTS.get(account_number)

    if account is None:
        return f"No account found for {account_number}."

    return (
        f"Account {account_number} has a balance of "
        f"{account['currency']} {account['balance']:.2f}"
    )


@mcp.tool()
def get_customer_name(customer_id: str) -> str:
    """Get the customer name for an internal Rabobank customer."""
    customer_name = CUSTOMERS.get(customer_id)

    if customer_name is None:
        return f"No customer found for {customer_id}."

    return f"Customer {customer_id} is {customer_name}"


@mcp.tool()
def get_branch_information(branch_code: str) -> str:
    """Get branch information for an internal Rabobank branch."""
    branch = BRANCHES.get(branch_code)

    if branch is None:
        return f"No branch found for {branch_code}."

    services = ", ".join(branch["services"])
    return (
        f"Branch {branch_code}\n"
        f"Location: {branch['location']}\n"
        f"Opening Hours: {branch['opening_hours']}\n"
        f"Services: {services}"
    )


@mcp.tool(name="discoverTools", tags={"meta", "discovery"})
async def discover_tools(
    tag: str | None = None,
    include_auth: bool = False,
    compact: bool = False,
) -> dict[str, Any]:
    """Discover tools dynamically, including schemas, examples, and optional metadata."""
    return await _discover_tool_catalog(tag=tag, include_auth=include_auth, compact=compact)


@mcp.tool(name="listTools", tags={"meta", "discovery"})
async def list_tools(
    tag: str | None = None,
    include_auth: bool = False,
    compact: bool = False,
) -> dict[str, Any]:
    """Alias for discoverTools to support list-style capability discovery prompts."""
    return await _discover_tool_catalog(tag=tag, include_auth=include_auth, compact=compact)


if __name__ == "__main__":
    mcp.run()