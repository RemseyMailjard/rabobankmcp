# Design Styling MCP Demo

This is a small demo MCP server that returns UI components as ready-to-use HTML, CSS, and JavaScript bundles.

## Demo lab

Open [demo-lab.html](demo-lab.html) for the guided lab that expands the component catalog, token system, and preview helpers.

## What it does

The server exposes a few tools for frontend-style prompts:

- `list_components` to inspect the demo catalog
- `search_components` to find the best match by interaction or layout type
- `get_component_outline` to inspect the structure and usage of one component
- `get_design_documentation` to return usage guidance for the component system
- `list_design_topics` to discover all documentation topics
- `get_component_bundle` to fetch HTML, CSS, and JS for a component
- `get_design_tokens` to retrieve a small design token set
- `build_component_page` to generate a full preview page
- `build_component_story_page` to generate a richer review page with docs and tokens

## Example prompts

- "Give me a modern button component"
- "Return a card component in HTML, CSS, and JS"
- "Show me documentation for the CSS topic"
- "Build a preview page for the navbar component"
- "Show me the design tokens for the ocean theme"
- "Search for the best component for a launch story"
- "Create a feature panel component and return a story page"
- "Add a sunset token theme for the new component"
- "Explain the composition guidance for the demo design system"

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