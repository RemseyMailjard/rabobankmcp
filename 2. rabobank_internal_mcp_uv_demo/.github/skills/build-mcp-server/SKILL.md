---
name: build-mcp-server
description: 'Build or design an MCP server. Use when the user asks to build an MCP server, create an MCP integration, wrap an API for AI tools, expose internal systems through Model Context Protocol, choose between stdio and HTTP, design MCP tools/resources/prompts, package a FastMCP server, or test an MCP server from VS Code or Python.'
argument-hint: 'Describe the system to expose, target users, transport, and preferred stack.'
version: 0.2.0
---

# Build an MCP Server

You are guiding a developer through building an MCP server that exposes a well-bounded capability to an AI client. Start with discovery. Do not scaffold until you can state what the server wraps, who will use it, which transport it needs, and how it will be validated.

This skill is for practical MCP server design and implementation in environments like VS Code, Copilot, Claude, and other MCP hosts. Prefer concrete engineering decisions over generic architecture talk.

## When to Use

Use this skill when the user wants to:

- build an MCP server from scratch
- wrap an internal API or service behind MCP tools
- choose between `stdio`, local HTTP, or remote streamable HTTP
- design MCP tools, resources, and prompts
- package a Python FastMCP server or TypeScript SDK server
- test an MCP server locally before connecting it to an AI client

Do not use this skill for generic app deployment that does not involve MCP.

## Phase 1: Discover the Server Shape

Gather the smallest set of answers that determine the build path.

### 1. What system is being exposed?

- REST or GraphQL API
- database or search system
- local files, desktop app, or localhost service
- pure workflow logic with no external dependency

### 2. Who will use it?

- one developer on one machine
- a small internal team
- many users across machines or tenants

### 3. What should the model be allowed to do?

- read-only lookup
- safe mutations with validation
- long-running workflows
- documentation or standards retrieval

### 4. Which MCP primitives are needed?

- `tool` for actions or retrieval with parameters
- `resource` for stable reference content such as policy or documentation
- `prompt` for reusable structured workflows

Prefer tools first. Add resources and prompts only when they reduce repeated instructions or expose durable context.

### 5. What transport is appropriate?

- `stdio` for local development, VS Code integration, or single-machine prototypes
- remote HTTP for shared hosted services and easier distribution
- avoid overcomplicating local demos with remote deployment too early

### 6. What auth and policy boundaries exist?

- none or demo key
- API key passthrough
- OAuth or workload identity
- sensitive-data restrictions, audit requirements, approval checks

## Phase 2: Make the Key Decisions

State the recommendation explicitly before coding.

### Transport decision

- Choose `stdio` when the user is prototyping locally or connecting from a local MCP client such as VS Code.
- Choose remote HTTP when the server must be shared broadly or integrated as a managed service.

### Framework decision

- Choose `FastMCP` for Python-first teams, internal API wrappers, and low-boilerplate prototypes.
- Choose the official TypeScript MCP SDK when the team is already on Node.js or needs tighter alignment with SDK-first MCP features.

### Tool-surface decision

- Fewer than about 15 clear operations: one tool per action.
- Large or dynamic API catalog: use a discovery tool plus one execution tool, or a small curated tool set for the high-value operations.

### Safety decision

- Separate read and write capabilities.
- Require explicit parameters instead of hidden inference for risky operations.
- Keep sensitive production data out of demo or developer-facing tools.

## Phase 3: Design the MCP Interface

Design the interface before writing code.

### Tool design rules

- One verb per tool.
- Clear names such as `get_customer_profile` or `run_architecture_check`.
- Tight parameter schemas with concrete examples.
- Return structured JSON that a model can summarize without guessing.
- Put upstream API calls behind small internal helper functions.

### Resource design rules

- Use resources for stable content such as security policies, standards, and product catalogs.
- Give each resource a durable URI-like identifier.
- Keep resource content self-contained and readable.

### Prompt design rules

- Add prompts only for recurring workflows.
- Prompts should reference existing tools or resources and specify the desired output shape.

## Phase 4: Scaffold the Smallest Useful Server

Build the thinnest end-to-end slice first.

### Recommended first slice

1. Create the server entrypoint.
2. Add one helper for outbound calls or data access.
3. Add one read-only tool.
4. Run the backing dependency if one exists.
5. Start the MCP server.
6. Call the tool from a real MCP client.

For Python and FastMCP, prefer this structure:

```text
app/
    mcp_server.py
    internal_api.py
    data.py
    run_api.py
.vscode/mcp.json
pyproject.toml
```

Keep packaging correct from the start:

- define the script entrypoint in `pyproject.toml`
- ensure the declared readme file exists
- keep the package import path stable

## Phase 5: Validate Through the MCP Layer

Do not stop at "the server starts". Validate a real call.

### Validation checklist

1. Start the backing system, if applicable.
2. Start the MCP server over the intended transport.
3. Initialize it with an MCP client.
4. Call the tool with realistic input.
5. Confirm the returned structure matches the contract.

For local Python validation, a one-off client using `mcp.client.stdio` and `ClientSession` is an acceptable smoke test.

If validation fails, check these first:

- packaging metadata such as missing readme files or broken script entrypoints
- transport mismatch between the client and server
- missing environment variables or API keys
- upstream API availability
- overly broad or ambiguous tool schemas

## Phase 6: Finish the Server for Real Use

Once the first tool works, expand carefully.

### Add the next capabilities in this order

1. Additional read-only tools
2. Resources for stable reference content
3. Prompts for reusable review or analysis flows
4. Write tools only after validation and guardrails are clear

### Final quality checks

- tool names and descriptions are specific and discoverable
- outputs are structured and deterministic enough for summarization
- dangerous operations are separated and constrained
- setup instructions match the actual commands
- local configuration such as `.vscode/mcp.json` is runnable

## Decision Matrix

| Scenario | Recommendation |
|---|---|
| Local internal API demo in VS Code | `stdio` + FastMCP |
| Python wrapper around internal REST endpoints | FastMCP tools with helper functions |
| Stable policy or standards content | MCP resources |
| Reusable review workflow | MCP prompt |
| Large shared service across many users | remote HTTP MCP server |

## Completion Criteria

The task is complete when all of these are true:

- the server shape is justified
- at least one tool works end to end through an MCP client
- the packaging and startup commands are correct
- the user can explain how to run, connect, and extend the server

## Example Prompts

- Build an MCP server that wraps our internal customer API using FastMCP.
- Help me choose between `stdio` and HTTP for a team-shared MCP server.
- Add a policy resource and a reusable prompt to my Python MCP server.
- Validate my MCP server locally by calling one tool through a Python client.
