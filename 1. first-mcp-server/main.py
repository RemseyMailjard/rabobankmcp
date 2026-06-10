from fastmcp import FastMCP

mcp = FastMCP("Rabobank Demo MCP Server")

@mcp.tool()
def get_account_balance(account_number: str) -> str:
    """Get the balance for an internal Rabobank account."""
    return f"Account {account_number} has a balance of €1,250.00"


if __name__ == "__main__":
    mcp.run()