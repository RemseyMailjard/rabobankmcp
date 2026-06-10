# Design Styling MCP Server Demo

This is a small demo MCP server that returns UI components as ready-to-use HTML, CSS, and JavaScript bundles.

## What it does

The server exposes a few tools for frontend-style prompts:

- `list_components` to inspect the demo catalog
- `get_design_documentation` to return usage guidance for the component system
- `get_component_bundle` to fetch HTML, CSS, and JS for a component
- `get_design_tokens` to retrieve a small design token set
- `build_component_page` to generate a full preview page

## Example prompts

- "Give me a modern button component"
- "Return a card component in HTML, CSS, and JS"
- "Show me documentation for the CSS topic"
- "Build a preview page for the navbar component"
- "Show me the design tokens for the ocean theme"

## Run it

From this folder:

```bash
uv sync
uv run design-mcp
```

If you do not want to use the script, you can also run the file directly with:

```bash
uv run main.py
```

## Notes

The components are intentionally small and opinionated so they work well as demo output in Copilot Chat or in a training session.