"""
Dummy IT Helpdesk API
=====================
A simple REST API simulating an IT helpdesk system.
Students will build an MCP server that wraps these endpoints.

Run with:
    uv run uvicorn server:app --reload --port 8000

API docs available at: http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(
    title="IT Helpdesk API",
    description="A dummy IT helpdesk API for building an MCP server against.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# In-memory data
# ---------------------------------------------------------------------------

employees = {
    "EMP001": {
        "id": "EMP001",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "department": "Engineering",
        "role": "Senior Developer",
    },
    "EMP002": {
        "id": "EMP002",
        "name": "Bob Martinez",
        "email": "bob@example.com",
        "department": "Marketing",
        "role": "Marketing Manager",
    },
    "EMP003": {
        "id": "EMP003",
        "name": "Carol Chen",
        "email": "carol@example.com",
        "department": "Engineering",
        "role": "DevOps Engineer",
    },
    "EMP004": {
        "id": "EMP004",
        "name": "David Kim",
        "email": "david@example.com",
        "department": "Sales",
        "role": "Account Executive",
    },
    "EMP005": {
        "id": "EMP005",
        "name": "Eva Rossi",
        "email": "eva@example.com",
        "department": "HR",
        "role": "HR Specialist",
    },
}

_ticket_counter = 3  # next ticket ID

tickets = {
    "TKT-001": {
        "id": "TKT-001",
        "title": "VPN not connecting from home",
        "description": "I can't connect to the corporate VPN from my home network. I get a timeout error after about 30 seconds.",
        "status": "open",
        "priority": "high",
        "employee_id": "EMP002",
        "category": "network",
        "created_at": "2025-06-10T09:15:00",
        "comments": [
            {
                "author": "IT Support",
                "text": "Have you tried restarting your router?",
                "timestamp": "2025-06-10T10:00:00",
            }
        ],
    },
    "TKT-002": {
        "id": "TKT-002",
        "title": "Need access to Figma",
        "description": "I need a Figma license for an upcoming project. My manager (Bob Martinez) has approved it.",
        "status": "in_progress",
        "priority": "medium",
        "employee_id": "EMP001",
        "category": "software",
        "created_at": "2025-06-11T14:30:00",
        "comments": [],
    },
}

kb_articles = {
    "KB-001": {
        "id": "KB-001",
        "title": "How to connect to the VPN",
        "category": "network",
        "content": (
            "1. Download the GlobalProtect VPN client from the IT portal.\n"
            "2. Open GlobalProtect and enter the portal address: vpn.example.com\n"
            "3. Sign in with your corporate email and password.\n"
            "4. Click Connect.\n\n"
            "Troubleshooting:\n"
            "- If you get a timeout, try switching to a different network.\n"
            "- Make sure your firewall is not blocking UDP port 4501.\n"
            "- Restart your router and try again."
        ),
        "tags": ["vpn", "remote", "network", "globalprotect"],
    },
    "KB-002": {
        "id": "KB-002",
        "title": "Requesting new software licenses",
        "category": "software",
        "content": (
            "To request a new software license:\n"
            "1. Open a support ticket with category 'software'.\n"
            "2. Include the software name and business justification.\n"
            "3. Mention your manager's name for approval.\n"
            "4. IT will process the request within 2 business days."
        ),
        "tags": ["software", "license", "request"],
    },
    "KB-003": {
        "id": "KB-003",
        "title": "Setting up your new laptop",
        "category": "hardware",
        "content": (
            "When you receive your new laptop:\n"
            "1. Power it on and connect to the 'CorpSetup' Wi-Fi network.\n"
            "2. Sign in with your corporate credentials.\n"
            "3. The device will auto-enroll in MDM and install required software.\n"
            "4. This process takes about 30 minutes.\n"
            "5. After setup, restart and connect to the regular corporate Wi-Fi."
        ),
        "tags": ["laptop", "onboarding", "hardware", "setup"],
    },
    "KB-004": {
        "id": "KB-004",
        "title": "Resetting your password",
        "category": "account",
        "content": (
            "To reset your corporate password:\n"
            "1. Go to https://password.example.com\n"
            "2. Enter your corporate email address.\n"
            "3. You'll receive a reset link via your personal email on file.\n"
            "4. Follow the link and set a new password.\n"
            "Requirements: 12+ characters, one uppercase, one number, one symbol."
        ),
        "tags": ["password", "account", "security", "reset"],
    },
    "KB-005": {
        "id": "KB-005",
        "title": "Printer setup and troubleshooting",
        "category": "hardware",
        "content": (
            "Adding a network printer:\n"
            "1. Go to Settings > Printers & Scanners.\n"
            "2. Click 'Add Printer' and select the printer from the list.\n"
            "3. Office printers are named by floor (e.g., 'Floor3-HP-Color').\n\n"
            "Troubleshooting:\n"
            "- Paper jam: Open the front panel, gently remove jammed paper.\n"
            "- Offline: Check the network cable and restart the printer.\n"
            "- Poor print quality: Replace toner cartridge."
        ),
        "tags": ["printer", "hardware", "troubleshooting"],
    },
}

# ---------------------------------------------------------------------------
# Pydantic models for request bodies
# ---------------------------------------------------------------------------


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str = "medium"  # low, medium, high
    employee_id: str
    category: str = "general"  # network, software, hardware, account, general


class TicketUpdate(BaseModel):
    status: Optional[str] = None  # open, in_progress, resolved, closed
    priority: Optional[str] = None
    comment: Optional[str] = None


# ---------------------------------------------------------------------------
# Employee endpoints
# ---------------------------------------------------------------------------


@app.get("/employees")
def list_employees(department: Optional[str] = Query(None)):
    """List all employees, optionally filtered by department."""
    results = list(employees.values())
    if department:
        results = [e for e in results if e["department"].lower() == department.lower()]
    return {"employees": results}


@app.get("/employees/{employee_id}")
def get_employee(employee_id: str):
    """Get details for a specific employee."""
    emp = employees.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


# ---------------------------------------------------------------------------
# Ticket endpoints
# ---------------------------------------------------------------------------


@app.get("/tickets")
def list_tickets(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    employee_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
):
    """List tickets with optional filters."""
    results = list(tickets.values())
    if status:
        results = [t for t in results if t["status"] == status]
    if priority:
        results = [t for t in results if t["priority"] == priority]
    if employee_id:
        results = [t for t in results if t["employee_id"] == employee_id]
    if category:
        results = [t for t in results if t["category"] == category]
    return {"tickets": results}


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    """Get details for a specific ticket."""
    ticket = tickets.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@app.post("/tickets", status_code=201)
def create_ticket(body: TicketCreate):
    """Create a new support ticket."""
    global _ticket_counter
    _ticket_counter += 1
    ticket_id = f"TKT-{_ticket_counter:03d}"

    if body.employee_id not in employees:
        raise HTTPException(status_code=400, detail="Invalid employee_id")
    if body.priority not in ("low", "medium", "high"):
        raise HTTPException(
            status_code=400, detail="Priority must be low, medium, or high"
        )

    ticket = {
        "id": ticket_id,
        "title": body.title,
        "description": body.description,
        "status": "open",
        "priority": body.priority,
        "employee_id": body.employee_id,
        "category": body.category,
        "created_at": datetime.now().isoformat(),
        "comments": [],
    }
    tickets[ticket_id] = ticket
    return ticket


@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, body: TicketUpdate):
    """Update a ticket's status/priority or add a comment."""
    ticket = tickets.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if body.status:
        if body.status not in ("open", "in_progress", "resolved", "closed"):
            raise HTTPException(status_code=400, detail="Invalid status")
        ticket["status"] = body.status

    if body.priority:
        if body.priority not in ("low", "medium", "high"):
            raise HTTPException(status_code=400, detail="Invalid priority")
        ticket["priority"] = body.priority

    if body.comment:
        ticket["comments"].append(
            {
                "author": "MCP User",
                "text": body.comment,
                "timestamp": datetime.now().isoformat(),
            }
        )

    return ticket


# ---------------------------------------------------------------------------
# Knowledge base endpoints
# ---------------------------------------------------------------------------


@app.get("/kb/articles")
def list_articles(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
):
    """Search knowledge base articles by keyword or category."""
    results = list(kb_articles.values())
    if category:
        results = [a for a in results if a["category"].lower() == category.lower()]
    if search:
        terms = search.lower().split()
        results = [
            a
            for a in results
            if any(
                t in a["title"].lower()
                or t in a["content"].lower()
                or any(t in tag for tag in a["tags"])
                for t in terms
            )
        ]
    # Return summaries (without full content) for list view
    return {
        "articles": [
            {"id": a["id"], "title": a["title"], "category": a["category"], "tags": a["tags"]}
            for a in results
        ]
    }


@app.get("/kb/articles/{article_id}")
def get_article(article_id: str):
    """Get full details for a knowledge base article."""
    article = kb_articles.get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
