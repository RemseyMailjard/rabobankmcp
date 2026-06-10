# IT Helpdesk API

A REST API simulating a company IT helpdesk system with employees, support tickets, and a knowledge base.

## Running the API

```bash
cd helpdesk-api
uv sync
uv run uvicorn server:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

All data is stored in memory and resets when the server restarts.

---

## Endpoints

### Employees

#### `GET /employees`

List all employees. Optionally filter by department.

**Query parameters:**

| Parameter    | Type   | Description                                      |
|-------------|--------|--------------------------------------------------|
| `department` | string | Filter by department (e.g. `Engineering`, `Sales`) |

**Example:** `GET /employees?department=Engineering`

**Response:**
```json
{
  "employees": [
    {
      "id": "EMP001",
      "name": "Alice Johnson",
      "email": "alice@example.com",
      "department": "Engineering",
      "role": "Senior Developer"
    }
  ]
}
```

#### `GET /employees/{employee_id}`

Get details for a single employee.

**Example:** `GET /employees/EMP001`

Returns `404` if the employee ID does not exist.

---

### Tickets

#### `GET /tickets`

List all support tickets. Supports multiple optional filters.

**Query parameters:**

| Parameter     | Type   | Values                                        |
|--------------|--------|-----------------------------------------------|
| `status`      | string | `open`, `in_progress`, `resolved`, `closed`    |
| `priority`    | string | `low`, `medium`, `high`                        |
| `employee_id` | string | e.g. `EMP001`                                  |
| `category`    | string | `network`, `software`, `hardware`, `account`, `general` |

**Example:** `GET /tickets?status=open&priority=high`

**Response:**
```json
{
  "tickets": [
    {
      "id": "TKT-001",
      "title": "VPN not connecting from home",
      "description": "I can't connect to the corporate VPN...",
      "status": "open",
      "priority": "high",
      "employee_id": "EMP002",
      "category": "network",
      "created_at": "2025-06-10T09:15:00",
      "comments": [
        {
          "author": "IT Support",
          "text": "Have you tried restarting your router?",
          "timestamp": "2025-06-10T10:00:00"
        }
      ]
    }
  ]
}
```

#### `GET /tickets/{ticket_id}`

Get full details for a single ticket.

**Example:** `GET /tickets/TKT-001`

Returns `404` if the ticket ID does not exist.

#### `POST /tickets`

Create a new support ticket.

**Request body:**

| Field         | Type   | Required | Default     | Description                          |
|--------------|--------|----------|-------------|--------------------------------------|
| `title`       | string | yes      |             | Short summary of the issue           |
| `description` | string | yes      |             | Detailed description of the problem  |
| `employee_id` | string | yes      |             | ID of the employee reporting (e.g. `EMP001`) |
| `priority`    | string | no       | `"medium"`  | `low`, `medium`, or `high`           |
| `category`    | string | no       | `"general"` | `network`, `software`, `hardware`, `account`, `general` |

**Example:**
```json
{
  "title": "Monitor flickering",
  "description": "My external monitor flickers every few seconds.",
  "employee_id": "EMP003",
  "priority": "high",
  "category": "hardware"
}
```

**Errors:**
- `400` if `employee_id` is invalid
- `400` if `priority` is not `low`, `medium`, or `high`

#### `PUT /tickets/{ticket_id}`

Update a ticket's status, priority, or add a comment.

**Request body** (all fields optional):

| Field      | Type   | Values                                      |
|-----------|--------|---------------------------------------------|
| `status`   | string | `open`, `in_progress`, `resolved`, `closed`  |
| `priority` | string | `low`, `medium`, `high`                      |
| `comment`  | string | Free text comment to add to the ticket       |

**Example:**
```json
{
  "status": "resolved",
  "comment": "Replaced the HDMI cable, issue fixed."
}
```

Returns `404` if the ticket ID does not exist.

---

### Knowledge Base

#### `GET /kb/articles`

Search knowledge base articles. Returns summaries (no full content).

**Query parameters:**

| Parameter  | Type   | Description                                              |
|-----------|--------|----------------------------------------------------------|
| `search`   | string | Keyword search across title, content, and tags           |
| `category` | string | `network`, `software`, `hardware`, `account`              |

**Example:** `GET /kb/articles?search=vpn`

**Response:**
```json
{
  "articles": [
    {
      "id": "KB-001",
      "title": "How to connect to the VPN",
      "category": "network",
      "tags": ["vpn", "remote", "network", "globalprotect"]
    }
  ]
}
```

#### `GET /kb/articles/{article_id}`

Get the full content of a knowledge base article.

**Example:** `GET /kb/articles/KB-001`

**Response:**
```json
{
  "id": "KB-001",
  "title": "How to connect to the VPN",
  "category": "network",
  "content": "1. Download the GlobalProtect VPN client from the IT portal...",
  "tags": ["vpn", "remote", "network", "globalprotect"]
}
```

Returns `404` if the article ID does not exist.

---

## Sample Data

The API comes pre-loaded with the following data:

**Employees:**

| ID     | Name           | Department  | Role              |
|--------|----------------|-------------|-------------------|
| EMP001 | Alice Johnson  | Engineering | Senior Developer  |
| EMP002 | Bob Martinez   | Marketing   | Marketing Manager |
| EMP003 | Carol Chen     | Engineering | DevOps Engineer   |
| EMP004 | David Kim      | Sales       | Account Executive |
| EMP005 | Eva Rossi      | HR          | HR Specialist     |

**Tickets:**

| ID      | Title                       | Status      | Priority | Employee | Category |
|---------|-----------------------------|-------------|----------|----------|----------|
| TKT-001 | VPN not connecting from home | open        | high     | EMP002   | network  |
| TKT-002 | Need access to Figma         | in_progress | medium   | EMP001   | software |

**Knowledge Base Articles:**

| ID     | Title                              | Category |
|--------|------------------------------------|----------|
| KB-001 | How to connect to the VPN          | network  |
| KB-002 | Requesting new software licenses   | software |
| KB-003 | Setting up your new laptop         | hardware |
| KB-004 | Resetting your password            | account  |
| KB-005 | Printer setup and troubleshooting  | hardware |
