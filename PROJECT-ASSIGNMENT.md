# Project: Build an MCP Server

## Overview

For this project, you will build an MCP server that acts as a **client to a real REST API**. 

You have two options:

- **Option A (Default):** Build an MCP server for the provided IT Helpdesk API (described below).
- **Option B (Custom):** Build an MCP server that wraps an API of your choosing — any public API or service you find useful.

If you go with Option B, the requirements below still apply (minimum number of tools, error handling, etc.) — just substitute your own API.

---

## Option A: IT Helpdesk MCP Server

### The API

A dummy IT Helpdesk REST API is provided in `helpdesk-api/`. It simulates a company helpdesk with employees, support tickets, and a knowledge base.

#### Starting the API

```bash
cd helpdesk-api
uv sync
uv run uvicorn server:app --reload --port 8000
```

Once running, open **http://localhost:8000/docs** for interactive API documentation.

#### API Endpoints

| Method | Endpoint                | Description                                    |
|--------|-------------------------|------------------------------------------------|
| GET    | `/employees`            | List employees (optional `?department=` filter) |
| GET    | `/employees/{id}`       | Get employee details                           |
| GET    | `/tickets`              | List tickets (filters: `status`, `priority`, `employee_id`, `category`) |
| GET    | `/tickets/{id}`         | Get ticket details                             |
| POST   | `/tickets`              | Create a new ticket                            |
| PUT    | `/tickets/{id}`         | Update ticket status/priority or add a comment |
| GET    | `/kb/articles`          | Search knowledge base (`?search=`, `?category=`) |
| GET    | `/kb/articles/{id}`     | Get full article content                       |

---

### Requirements

Your MCP server must include:

1. **At least 3 tools** that map to API endpoints. For example:
   - `list_tickets` — list/filter support tickets
   - `get_ticket` — get details on a specific ticket
   - `create_ticket` — create a new support ticket
   - `search_kb` — search the knowledge base for relevant articles
   - `get_employee` — look up an employee's info
   - (feel free to add more)

2. **Error handling** — your tools should handle cases like:
   - Employee or ticket not found (404)
   - Invalid input (bad status, missing fields)

3. **Meaningful docstrings** — each tool should have a clear docstring so the LLM knows when and how to use it.

---

### Getting Started

1. **Start the Helpdesk API** (keep it running in a terminal):
   ```bash
   cd helpdesk-api
   uv sync
   uv run uvicorn server:app --reload --port 8000
   ```

2. **Create your MCP server project** (in a new terminal):
   ```bash
   cd PROJECTS/MCP-SERVER
   uv init my-helpdesk-mcp
   cd my-helpdesk-mcp
   uv add "mcp[cli]" httpx
   ```

3. **Write your server** in `main.py`. Use `httpx` to call the Helpdesk API. Here is a starter snippet:

   ```python
   from mcp.server.fastmcp import FastMCP
   import httpx

   API_BASE = "http://localhost:8000"
   mcp = FastMCP("HelpdeskAssistant")

   @mcp.tool()
   def list_tickets(status: str = None, priority: str = None) -> str:
       """List support tickets, optionally filtered by status or priority."""
       params = {}
       if status:
           params["status"] = status
       if priority:
           params["priority"] = priority
       response = httpx.get(f"{API_BASE}/tickets", params=params)
       response.raise_for_status()
       data = response.json()
       if not data["tickets"]:
           return "No tickets found matching your filters."
       lines = []
       for t in data["tickets"]:
           lines.append(f"[{t['id']}] {t['title']} — {t['status']} ({t['priority']})")
       return "\n".join(lines)

   # TODO: Add more tools ...

   if __name__ == "__main__":
       mcp.run()
   ```

4. **Connect your server to Copilot** by adding it to your VS Code MCP configuration (`.vscode/mcp.json`):
   ```json
   {
     "servers": {
       "helpdesk": {
         "type": "stdio",
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "/ABSOLUTE/PATH/TO/my-helpdesk-mcp",
           "mcp",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```
   Replace `/ABSOLUTE/PATH/TO/my-helpdesk-mcp` with the actual path to your project.

5. **Open Copilot Chat in Agent mode** and test your tools.

---

## Deliverables

1. Your `main.py` containing the MCP server code.
2. A brief demo (live or recorded) showing Copilot using at least 3 of your tools in a realistic conversation. For example:
   - *"Are there any open high-priority tickets?"*
   - *"Create a ticket for Carol Chen — her monitor is flickering."*
   - *"Is there a knowledge base article about VPN issues?"*

---

## Rubric

| Criteria                  | Points |
|---------------------------|--------|
| 3+ working tools          | 40     |
| Error handling             | 20     |
| Clear docstrings           | 15     |
| Demo with Copilot          | 25     |
| **Total**                 | **100** |

---

## Option B: Custom MCP Server

If you want to build something different, go for it. Some ideas:

- **Weather API** — wrap OpenWeatherMap so Claude can check forecasts
- **GitHub API** — let Claude search repos, list issues, read READMEs
- **Recipe API** — search recipes, get ingredients, filter by dietary restrictions
- **News API** — search headlines, get article summaries
- **Spotify API** — search tracks, get playlist info, see what's playing
- **Your own project's API** — if you have a side project with an API, wrap it

The same rubric applies: 3+ tools, error handling, docstrings, and a demo.
