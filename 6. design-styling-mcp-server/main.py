from __future__ import annotations

from copy import deepcopy
from typing import Any

from fastmcp import FastMCP

mcp = FastMCP("Design Styling MCP Demo")


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

COMPONENT_ORDER = ["button", "card", "navbar"]

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
    def get_design_documentation(topic: str = "overview") -> dict[str, Any]:
      """Return documentation and usage guidance for the demo design system.

      Use this when you want a quick explanation of how to use the HTML, CSS, and JavaScript snippets in this server.
      """
      documentation = DOCUMENTATION_TOPICS.get(topic.lower())
      if not documentation:
        return {
          "error": f"Unknown documentation topic '{topic}'.",
          "available_topics": sorted(DOCUMENTATION_TOPICS.keys()),
        }

      return {
        "topic": topic.lower(),
        **documentation,
      }


@mcp.tool()
def get_component_bundle(component_id: str) -> dict[str, Any]:
    """Return a component bundle with HTML, CSS, JS, and usage notes.

    Use this when you want a ready-to-paste UI component for a demo, prototype, or design handoff.
    """
    component = COMPONENTS.get(component_id.lower())
    if not component:
        available = ", ".join(COMPONENT_ORDER)
        return {
            "error": f"Unknown component '{component_id}'.",
            "available_components": available,
        }

    bundle = deepcopy(component)
    bundle["component_id"] = component_id.lower()
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
    }

    selected = tokens.get(theme.lower())
    if not selected:
        return {
            "error": f"Unknown theme '{theme}'.",
            "available_themes": sorted(tokens.keys()),
        }

    return {
        "theme": theme.lower(),
        "tokens": selected,
    }


@mcp.tool()
def build_component_page(component_id: str, title: str = "Design Demo") -> dict[str, str]:
    """Return a complete HTML page that previews one of the demo components.

    Use this when you want the component rendered in a standalone page with embedded CSS and JS.
    """
    component = COMPONENTS.get(component_id.lower())
    if not component:
        available = ", ".join(COMPONENT_ORDER)
        return {
            "error": f"Unknown component '{component_id}'.",
            "available_components": available,
        }

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
    }}

    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 2rem;
      background: radial-gradient(circle at top left, #ecfeff, transparent 36%),
                  linear-gradient(180deg, #f8fafc, #e2e8f0);
      color: #0f172a;
    }}

    .demo-shell {{
      width: min(100%, 56rem);
      display: grid;
      gap: 1.25rem;
    }}

    .demo-shell__header h1 {{
      margin: 0;
      font-size: clamp(2rem, 4vw, 3.25rem);
      line-height: 1.05;
    }}

    .demo-shell__header p {{
      max-width: 44rem;
      margin: 0.75rem 0 0;
      color: #475569;
      line-height: 1.7;
    }}
  </style>
</head>
<body>
  <main class=\"demo-shell\">
    <section class=\"demo-shell__header\">
      <h1>{title}</h1>
      <p>{component["purpose"]}</p>
    </section>
    <section>
      {component["html"]}
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
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()