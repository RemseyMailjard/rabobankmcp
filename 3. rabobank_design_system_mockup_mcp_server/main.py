from __future__ import annotations

from copy import deepcopy
from typing import Any

from fastmcp import FastMCP

mcp = FastMCP("Design Styling MCP Demo")


def _normalize_identifier(value: str) -> str:
  return value.strip().lower()


def _get_component(component_id: str) -> dict[str, Any] | None:
  return COMPONENTS.get(_normalize_identifier(component_id))


def _component_error(component_id: str) -> dict[str, Any]:
  return {
    "error": f"Unknown component '{component_id}'.",
    "available_components": COMPONENT_ORDER,
    "next_step": "Use list_components() or search_components() to find a valid component id.",
  }


def _documentation_error(topic: str) -> dict[str, Any]:
  return {
    "error": f"Unknown documentation topic '{topic}'.",
    "available_topics": sorted(DOCUMENTATION_TOPICS.keys()),
    "next_step": "Try the overview, html, css, javascript, accessibility, or composition topic.",
  }


COMPONENTS: dict[str, dict[str, Any]] = {
    "button": {
        "name": "Glass Accent Button",
        "purpose": "Primary call-to-action button for modern product interfaces.",
        "variant": "modern",
        "html": """<button class=\"ui-button\" type=\"button\" data-ui-button>
  <span>Continue</span>
</button>""",
        "css": """.ui-button {
  appearance: none;
  border: 0;
  border-radius: 999px;
  padding: 0.9rem 1.35rem;
  font: 600 1rem/1 system-ui, sans-serif;
  color: #fff;
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  box-shadow: 0 16px 35px rgba(15, 118, 110, 0.28);
  cursor: pointer;
  transition: transform 160ms ease, box-shadow 160ms ease, filter 160ms ease;
}

.ui-button:hover {
  transform: translateY(-1px);
  filter: brightness(1.04);
  box-shadow: 0 20px 38px rgba(15, 118, 110, 0.34);
}

.ui-button:active {
  transform: translateY(0);
  box-shadow: 0 10px 24px rgba(15, 118, 110, 0.22);
}""",
        "js": """document.querySelectorAll('[data-ui-button]').forEach((button) => {
  button.addEventListener('click', () => {
    button.classList.add('is-pressed');
    window.setTimeout(() => button.classList.remove('is-pressed'), 180);
  });
});""",
        "notes": [
            "Use for primary actions only.",
            "Keep the label short and specific.",
        ],
    },
    "card": {
        "name": "Elevated Content Card",
        "purpose": "Reusable card for summaries, metrics, or feature highlights.",
        "variant": "editorial",
        "html": """<article class=\"ui-card\" data-ui-card>
  <p class=\"ui-card__eyebrow\">Workspace update</p>
  <h3>Design review ready</h3>
  <p>Ship a clean component preview with deliberate spacing, depth, and readable hierarchy.</p>
</article>""",
        "css": """.ui-card {
  max-width: 22rem;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 1.25rem;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(12px);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.1);
}

.ui-card__eyebrow {
  margin: 0 0 0.5rem;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #0f766e;
}

.ui-card h3 {
  margin: 0 0 0.75rem;
  font-size: 1.25rem;
}

.ui-card p:last-child {
  margin: 0;
  color: #475569;
  line-height: 1.6;
}""",
        "js": """document.querySelectorAll('[data-ui-card]').forEach((card) => {
  card.addEventListener('mouseenter', () => card.setAttribute('data-hovered', 'true'));
  card.addEventListener('mouseleave', () => card.removeAttribute('data-hovered'));
});""",
        "notes": [
            "Best on light backgrounds or soft gradients.",
            "Mix title, supporting text, and an optional action.",
        ],
    },
    "feature-panel": {
        "name": "Feature Panel",
        "purpose": "Large composed block for product stories, onboarding flows, or launch announcements.",
        "variant": "composed",
        "html": """<section class=\"ui-feature-panel\" data-ui-feature-panel>
  <div class=\"ui-feature-panel__content\">
    <p class=\"ui-feature-panel__eyebrow\">New release</p>
    <h3>Launch-ready workflow</h3>
    <p>Combine context, action, and guidance in one component that reads well inside a story page.</p>
  </div>
  <div class=\"ui-feature-panel__actions\">
    <button class=\"ui-feature-panel__cta\" type=\"button\">Explore</button>
    <a class=\"ui-feature-panel__link\" href=\"#\">View details</a>
  </div>
</section>""",
        "css": """.ui-feature-panel {
  display: grid;
  grid-template-columns: 1.45fr auto;
  gap: 1rem;
  align-items: end;
  max-width: 42rem;
  padding: 1.4rem;
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 1.5rem;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.95), rgba(236, 254, 255, 0.92));
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.1);
}

.ui-feature-panel__eyebrow {
  margin: 0 0 0.45rem;
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: #0f766e;
}

.ui-feature-panel h3 {
  margin: 0 0 0.7rem;
  font-size: clamp(1.4rem, 2vw, 1.9rem);
}

.ui-feature-panel p:last-child {
  margin: 0;
  color: #475569;
  line-height: 1.65;
}

.ui-feature-panel__actions {
  display: grid;
  justify-items: end;
  gap: 0.65rem;
}

.ui-feature-panel__cta {
  border: 0;
  border-radius: 999px;
  padding: 0.8rem 1.15rem;
  background: linear-gradient(135deg, #0f766e, #14b8a6);
  color: #fff;
  font-weight: 800;
}

.ui-feature-panel__link {
  color: #0f766e;
  font-weight: 700;
  text-decoration: none;
}""",
        "js": """document.querySelectorAll('[data-ui-feature-panel]').forEach((panel) => {
  panel.addEventListener('click', () => panel.toggleAttribute('data-highlighted'));
});""",
        "notes": [
            "Best for launch stories or onboarding summaries.",
            "Pairs well with one primary action and one supporting link.",
        ],
    },
    "navbar": {
        "name": "Floating Navbar",
        "purpose": "Compact top navigation with subtle glass styling.",
        "variant": "navigation",
        "html": """<header class=\"ui-navbar\">
  <a class=\"ui-navbar__brand\" href=\"#\">Northstar</a>
  <nav class=\"ui-navbar__links\">
    <a href=\"#overview\">Overview</a>
    <a href=\"#components\">Components</a>
    <a href=\"#tokens\">Tokens</a>
  </nav>
  <button class=\"ui-navbar__action\" type=\"button\">Try demo</button>
</header>""",
        "css": """.ui-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.9rem 1.1rem;
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 1rem;
  background: rgba(15, 23, 42, 0.78);
  color: #fff;
  backdrop-filter: blur(18px);
}

.ui-navbar__brand,
.ui-navbar__links a {
  color: inherit;
  text-decoration: none;
}

.ui-navbar__brand {
  font-weight: 800;
  letter-spacing: 0.02em;
}

.ui-navbar__links {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.ui-navbar__action {
  border: 0;
  border-radius: 999px;
  padding: 0.7rem 1rem;
  background: #f8fafc;
  color: #0f172a;
  font-weight: 700;
}""",
        "js": """document.querySelectorAll('.ui-navbar__action').forEach((button) => {
  button.addEventListener('click', () => {
    console.log('Demo CTA clicked');
  });
});""",
        "notes": [
            "Ideal for dashboards and product landing pages.",
            "Pair with a strong hero and clear page sections.",
        ],
    },
}

COMPONENT_ORDER = ["button", "card", "feature-panel", "navbar"]

DOCUMENTATION_TOPICS: dict[str, dict[str, Any]] = {
  "overview": {
    "title": "Design System Overview",
    "summary": "Use the demo components to keep layout, motion, and spacing consistent across small UI prototypes.",
    "guidelines": [
      "Prefer one clear primary action per screen.",
      "Use soft contrast, not harsh neon accents.",
      "Keep spacing generous and typography readable.",
      "Return HTML, CSS, and JS together when the component needs interaction.",
    ],
    "example_prompt": "Give me a button component with HTML, CSS, and JS.",
  },
  "html": {
    "title": "HTML Guidance",
    "summary": "Structure components with semantic elements and concise labels.",
    "guidelines": [
      "Use semantic tags like button, article, header, and nav.",
      "Keep HTML focused on structure rather than visual styling.",
      "Add data attributes only when the JavaScript needs a hook.",
    ],
    "example_prompt": "Show me a semantic card component in HTML.",
  },
  "css": {
    "title": "CSS Guidance",
    "summary": "Use a small token set, strong spacing rules, and deliberate visual hierarchy.",
    "guidelines": [
      "Define radius, color, and shadow values consistently.",
      "Prefer readable font sizes and line heights.",
      "Use transitions for subtle feedback, not constant motion.",
    ],
    "example_prompt": "Give me CSS guidance for a glass-style navbar.",
  },
  "javascript": {
    "title": "JavaScript Guidance",
    "summary": "Keep interaction small and purposeful.",
    "guidelines": [
      "Attach event listeners only where behavior is needed.",
      "Avoid framework assumptions in demo snippets.",
      "Use JS to enhance interaction, not to build layout.",
    ],
    "example_prompt": "Explain the JavaScript behavior for a button component.",
  },
  "accessibility": {
    "title": "Accessibility Guidance",
    "summary": "Design components that remain usable with keyboard, screen readers, and low vision.",
    "guidelines": [
      "Preserve native controls for interactive elements whenever possible.",
      "Keep visible focus states and sufficient contrast.",
      "Use descriptive labels and short text.",
    ],
    "example_prompt": "Give me accessibility notes for the navbar component.",
  },
  "composition": {
    "title": "Composition Guidance",
    "summary": "Use the demo components together without losing hierarchy.",
    "guidelines": [
      "Keep one primary action per surface.",
      "Balance text, whitespace, and supporting actions.",
      "Maintain visible focus states in every composed layout.",
      "Return a short explanation for how the pieces fit together.",
    ],
    "example_prompt": "Explain how to combine a hero and a button component.",
  },
}


COMPONENT_OUTLINES: dict[str, list[str]] = {
  "button": ["Action", "Label", "Interaction"],
  "card": ["Eyebrow", "Title", "Body", "Optional action"],
  "feature-panel": ["Eyebrow", "Title", "Body", "Primary action", "Secondary link"],
  "navbar": ["Brand", "Links", "Action"],
}


@mcp.tool()
def list_components() -> list[dict[str, str]]:
    """List the demo design components that the server can return."""
    return [
        {
            "id": component_id,
            "name": COMPONENTS[component_id]["name"],
            "purpose": COMPONENTS[component_id]["purpose"],
            "variant": COMPONENTS[component_id]["variant"],
        }
        for component_id in COMPONENT_ORDER
    ]


@mcp.tool()
def search_components(query: str) -> dict[str, Any]:
  """Search the demo catalog by component name, purpose, notes, or outline.

  Use this when you know the desired interaction or layout pattern but not the exact component id.
  """
  normalized_query = query.strip().lower()
  if not normalized_query:
    return {
      "error": "Query cannot be empty.",
      "next_step": "Ask for a layout type like button, card, panel, navbar, or launch story.",
    }

  matches: list[dict[str, Any]] = []
  for component_id in COMPONENT_ORDER:
    component = COMPONENTS[component_id]
    outline = COMPONENT_OUTLINES.get(component_id, [])
    haystack = " ".join(
      [component_id, component["name"], component["purpose"], component["variant"], " ".join(component["notes"]), " ".join(outline)]
    ).lower()

    if normalized_query in haystack:
      matches.append(
        {
          "id": component_id,
          "name": component["name"],
          "purpose": component["purpose"],
          "variant": component["variant"],
          "outline": outline,
        }
      )

  return {
    "query": query,
    "match_count": len(matches),
    "matches": matches,
    "next_step": "Use get_component_bundle() or get_component_outline() for the best match.",
  }


@mcp.tool()
def get_component_outline(component_id: str) -> dict[str, Any]:
  """Return the structure, notes, and suggested usage for one component.

  Use this when you need a compact overview before asking for the full HTML, CSS, and JS bundle.
  """
  component = _get_component(component_id)
  if not component:
    return _component_error(component_id)

  normalized_id = _normalize_identifier(component_id)
  return {
    "component_id": normalized_id,
    "name": component["name"],
    "purpose": component["purpose"],
    "variant": component["variant"],
    "outline": COMPONENT_OUTLINES.get(normalized_id, []),
    "notes": component["notes"],
    "recommended_prompt": f"Use the {normalized_id} component for a polished design demo.",
  }


@mcp.tool()
def list_design_topics() -> list[dict[str, str]]:
  """List the available documentation topics in the demo server."""
  return [
    {
      "topic": topic,
      "title": documentation["title"],
      "summary": documentation["summary"],
    }
    for topic, documentation in DOCUMENTATION_TOPICS.items()
  ]


@mcp.tool()
def get_design_documentation(topic: str = "overview") -> dict[str, Any]:
  """Return documentation and usage guidance for the demo design system.

  Use this when you want a quick explanation of how to use the HTML, CSS, and JavaScript snippets in this server.
  """
  documentation = DOCUMENTATION_TOPICS.get(_normalize_identifier(topic))
  if not documentation:
    return _documentation_error(topic)

  return {
    "topic": _normalize_identifier(topic),
    **documentation,
  }


@mcp.tool()
def get_component_bundle(component_id: str) -> dict[str, Any]:
    """Return a component bundle with HTML, CSS, JS, and usage notes.

    Use this when you want a ready-to-paste UI component for a demo, prototype, or design handoff.
    """
    component = COMPONENTS.get(component_id.lower())
    if not component:
      return _component_error(component_id)

    bundle = deepcopy(component)
    normalized_id = _normalize_identifier(component_id)
    bundle["component_id"] = normalized_id
    bundle["outline"] = COMPONENT_OUTLINES.get(normalized_id, [])
    return bundle


@mcp.tool()
def get_design_tokens(theme: str = "ocean") -> dict[str, Any]:
    """Return a compact design token set for the demo UI system.

    Use this when you need colors, spacing, and typography values to keep multiple components visually aligned.
    """
    tokens = {
        "ocean": {
            "background": "#f8fafc",
            "surface": "#ffffff",
            "text": "#0f172a",
            "muted": "#475569",
            "primary": "#0f766e",
            "secondary": "#14b8a6",
            "radius": "1rem",
            "shadow": "0 18px 40px rgba(15, 23, 42, 0.1)",
        },
        "midnight": {
            "background": "#020617",
            "surface": "#0f172a",
            "text": "#e2e8f0",
            "muted": "#94a3b8",
            "primary": "#38bdf8",
            "secondary": "#60a5fa",
            "radius": "1rem",
            "shadow": "0 22px 45px rgba(2, 6, 23, 0.35)",
        },
        "sunset": {
            "background": "#fff7ed",
            "surface": "#ffffff",
            "text": "#1f2937",
            "muted": "#6b7280",
            "primary": "#c2410c",
            "secondary": "#fb923c",
            "radius": "1rem",
            "shadow": "0 22px 45px rgba(194, 65, 12, 0.18)",
        },
        "forest": {
            "background": "#f0fdf4",
            "surface": "#ffffff",
            "text": "#0f172a",
            "muted": "#475569",
            "primary": "#166534",
            "secondary": "#22c55e",
            "radius": "1rem",
            "shadow": "0 18px 40px rgba(22, 101, 52, 0.18)",
        },
    }

    selected = tokens.get(_normalize_identifier(theme))
    if not selected:
        return {
            "error": f"Unknown theme '{theme}'.",
            "available_themes": sorted(tokens.keys()),
            "next_step": "Try ocean, midnight, sunset, or forest.",
        }

    return {
        "theme": _normalize_identifier(theme),
        "tokens": selected,
    }


@mcp.tool()
def build_component_page(component_id: str, title: str = "Design Demo", theme: str = "ocean") -> dict[str, str]:
    """Return a complete HTML page that previews one of the demo components.

    Use this when you want the component rendered in a standalone page with embedded CSS and JS.
    """
    component = _get_component(component_id)
    if not component:
        return _component_error(component_id)

    selected_tokens = get_design_tokens(theme)
    if "error" in selected_tokens:
        return selected_tokens

    normalized_id = _normalize_identifier(component_id)
    outline = COMPONENT_OUTLINES.get(normalized_id, [])

    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title}</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      --bg: {selected_tokens['tokens']['background']};
      --surface: {selected_tokens['tokens']['surface']};
      --text: {selected_tokens['tokens']['text']};
      --muted: {selected_tokens['tokens']['muted']};
      --primary: {selected_tokens['tokens']['primary']};
      --secondary: {selected_tokens['tokens']['secondary']};
      --radius: {selected_tokens['tokens']['radius']};
      --shadow: {selected_tokens['tokens']['shadow']};
    }}

    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 2rem;
      background: radial-gradient(circle at top left, rgba(20, 184, 166, 0.2), transparent 36%),
                  linear-gradient(180deg, var(--bg), #ffffff);
      color: var(--text);
    }}

    .demo-shell {{
      width: min(100%, 56rem);
      display: grid;
      gap: 1.25rem;
    }}

    .demo-shell__meta {{
      display: flex;
      gap: 0.75rem;
      flex-wrap: wrap;
      margin-top: 0.75rem;
    }}

    .demo-shell__chip {{
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      padding: 0.4rem 0.7rem;
      border-radius: 999px;
      background: var(--surface);
      border: 1px solid rgba(15, 23, 42, 0.08);
      color: var(--muted);
      font-size: 0.85rem;
      box-shadow: var(--shadow);
    }}

    .demo-shell__header h1 {{
      margin: 0;
      font-size: clamp(2rem, 4vw, 3.25rem);
      line-height: 1.05;
    }}

    .demo-shell__header p {{
      max-width: 44rem;
      margin: 0.75rem 0 0;
      color: var(--muted);
      line-height: 1.7;
    }}

    .demo-shell__notes {{
      display: grid;
      gap: 0.75rem;
      padding: 1rem 1.1rem;
      border-radius: var(--radius);
      border: 1px solid rgba(15, 23, 42, 0.08);
      background: var(--surface);
      box-shadow: var(--shadow);
    }}

    .demo-shell__notes strong {{
      color: var(--primary);
    }}

    .demo-shell__notes ul {{
      margin: 0;
      padding-left: 1.2rem;
      color: var(--muted);
    }}
  </style>
</head>
<body>
  <main class=\"demo-shell\">
    <section class=\"demo-shell__header\">
      <h1>{title}</h1>
      <p>{component["purpose"]}</p>
      <div class=\"demo-shell__meta\">
        <span class=\"demo-shell__chip\">Theme: {selected_tokens['theme']}</span>
        <span class=\"demo-shell__chip\">Variant: {component['variant']}</span>
        <span class=\"demo-shell__chip\">Outline: {len(outline)} parts</span>
      </div>
    </section>
    <section>
      {component["html"]}
    </section>
    <section class=\"demo-shell__notes\">
      <strong>Component outline</strong>
      <ul>
        {''.join(f'<li>{item}</li>' for item in outline)}
      </ul>
    </section>
  </main>
  <script>
{component["js"]}
  </script>
</body>
</html>"""

    return {
        "html": html,
        "css": component["css"],
        "js": component["js"],
        "theme": selected_tokens["theme"],
        "outline": outline,
    }


@mcp.tool()
def build_component_story_page(component_id: str, theme: str = "ocean", topic: str = "overview", title: str = "Design Story") -> dict[str, Any]:
    """Return a story page that combines a component, theme, outline, and documentation.

    Use this when you want a richer design review page instead of a plain component preview.
    """
    component = _get_component(component_id)
    if not component:
        return _component_error(component_id)

    selected_tokens = get_design_tokens(theme)
    if "error" in selected_tokens:
        return selected_tokens

    documentation = DOCUMENTATION_TOPICS.get(_normalize_identifier(topic))
    if not documentation:
        return _documentation_error(topic)

    normalized_id = _normalize_identifier(component_id)
    outline = COMPONENT_OUTLINES.get(normalized_id, [])
    preview = build_component_page(component_id, title=f"{title}: {component['name']}", theme=theme)

    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{title} - {component['name']}</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: Inter, ui-sans-serif, system-ui, sans-serif;
      --bg: {selected_tokens['tokens']['background']};
      --surface: {selected_tokens['tokens']['surface']};
      --text: {selected_tokens['tokens']['text']};
      --muted: {selected_tokens['tokens']['muted']};
      --primary: {selected_tokens['tokens']['primary']};
      --secondary: {selected_tokens['tokens']['secondary']};
      --radius: {selected_tokens['tokens']['radius']};
      --shadow: {selected_tokens['tokens']['shadow']};
    }}

    body {{
      margin: 0;
      min-height: 100vh;
      padding: 2rem;
      background: linear-gradient(180deg, var(--bg), #ffffff);
      color: var(--text);
    }}

    .story-shell {{
      width: min(100%, 74rem);
      margin: 0 auto;
      display: grid;
      gap: 1.25rem;
    }}

    .story-hero, .story-card {{
      background: var(--surface);
      border: 1px solid rgba(15, 23, 42, 0.08);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 1.2rem;
    }}

    .story-hero h1 {{
      margin: 0;
      font-size: clamp(2rem, 4vw, 3.4rem);
      line-height: 1.05;
    }}

    .story-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-top: 0.85rem;
    }}

    .story-meta span {{
      padding: 0.4rem 0.7rem;
      border-radius: 999px;
      background: rgba(15, 118, 110, 0.08);
      color: var(--primary);
      font-size: 0.86rem;
      font-weight: 700;
    }}

    .story-grid {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 1rem;
      align-items: start;
    }}

    .story-card h2 {{
      margin: 0 0 0.75rem;
      font-size: 1.15rem;
    }}

    .story-card p, .story-card li {{ color: var(--muted); line-height: 1.65; }}

    .story-card ul {{ margin: 0; padding-left: 1.2rem; }}

    .story-preview {{
      display: grid;
      gap: 0.8rem;
    }}

    .story-preview__frame {{
      padding: 1rem;
      border-radius: var(--radius);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.76));
      border: 1px solid rgba(15, 23, 42, 0.08);
      box-shadow: var(--shadow);
    }}

    {preview['css']}
  </style>
</head>
<body>
  <main class=\"story-shell\">
    <section class=\"story-hero\">
      <h1>{title}: {component['name']}</h1>
      <p>{documentation['summary']}</p>
      <div class=\"story-meta\">
        <span>Theme: {selected_tokens['theme']}</span>
        <span>Topic: {_normalize_identifier(topic)}</span>
        <span>Variant: {component['variant']}</span>
        <span>Outline parts: {len(outline)}</span>
      </div>
    </section>

    <div class=\"story-grid\">
      <section class=\"story-card\">
        <h2>Why this works</h2>
        <ul>
          {''.join(f'<li>{item}</li>' for item in documentation['guidelines'])}
        </ul>
        <h2>Component outline</h2>
        <ul>
          {''.join(f'<li>{item}</li>' for item in outline)}
        </ul>
      </section>

      <aside class=\"story-preview\">
        <section class=\"story-card\">
          <h2>Preview data</h2>
          <p><strong>Prompt:</strong> {documentation['example_prompt']}</p>
          <p><strong>Outline:</strong> {', '.join(outline)}</p>
        </section>
        <section class=\"story-preview__frame\">
          {component['html']}
        </section>
      </aside>
    </div>
  </main>
  <script>
{preview['js']}
  </script>
</body>
</html>"""

    return {
        "html": html,
        "css": preview["css"],
        "js": preview["js"],
        "component_id": normalized_id,
        "theme": selected_tokens["theme"],
        "topic": _normalize_identifier(topic),
        "outline": outline,
        "documentation": documentation,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()