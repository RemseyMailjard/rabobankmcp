# Use the official uv image (Python 3.12 + uv preinstalled).
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

# Copy the server. PEP 723 inline metadata means uv resolves deps on run,
# but we warm the cache at build time so startup is fast.
COPY server.py ./

# Pre-install dependencies declared in the script's inline metadata.
RUN uv sync --script server.py

# The MCP server listens over HTTP so it can run as a long-lived service.
EXPOSE 8000

# Run over HTTP transport on all interfaces so the container stays up and
# is reachable from clients. Host/port are passed to FastMCP's HTTP transport.
CMD ["uv", "run", "fastmcp", "run", "server.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
