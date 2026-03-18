# Frontend Guidelines

> For all design decisions — colours, typography, components, voice — refer to [`docs/brand.md`](docs/brand.md). That is the single source of truth. This file covers dev conventions only.

---

## Stack

| Concern | Tool |
|---|---|
| CSS framework | Tailwind CSS via PostCSS build (replacing Bootstrap 5.3.3) |
| Custom styles | `blog/static/blog/css/blog.css` |
| Fonts | Lora + DM Sans via Google Fonts (see `docs/brand.md`) |
| Maps | Folium (server-rendered, embedded as iframe/HTML) |
| JavaScript | Vanilla JS only — no framework |
| Icons | Heroicons (recommended, same Tailwind family) |

> **Migration note:** The project was originally built with Bootstrap 5.3.3. All Bootstrap classes and CDN references are being replaced with Tailwind. Do not mix the two frameworks.

---

## Tailwind setup

### `tailwind.config.js`

Register all brand colours and fonts as named tokens so Tailwind utilities (e.g. `bg-cream`, `text-cobalt`) map directly to the design system:

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html',
    './**/static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        cream:      '#F2EBD5',
        amber:      '#E8A62C',
        sand:       '#D9C49C',
        sienna:     '#D98723',
        cobalt:     '#153FB3',
        ink:        '#1A1610',
        'ink-muted':'#5C4F35',
        'ink-light':'#9A8A6A',
      },
      fontFamily: {
        serif: ['Lora', 'Georgia', 'serif'],
        sans:  ['DM Sans', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
```

### `postcss.config.js`

```js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### Build

Add to Render `buildCommand` after `uv sync`:
```
uv run python manage.py tailwind build
```

For local dev with live reload:
```
uv run python manage.py tailwind start
```

---

## Template Structure

Templates live inside each app under `<app>/templates/<app>/`.

```
blog/templates/blog/
    base.html         ← master layout, extended by all blog templates
    post_list.html
    post_detail.html

map/templates/map/
    post_list_by_location.html
```

### `base.html` blocks

| Block | Purpose |
|---|---|
| `{% block title %}` | Page `<title>` tag |
| `{% block content %}` | Main page body |
| `{% block extra_css %}` | Per-page styles (rare) |
| `{% block extra_js %}` | Per-page scripts, loaded at bottom of `<body>` |

New blocks must be added to `base.html` before use. Never use inline styles or `<script>` tags in child templates.

### Google Fonts

Load in `base.html` `<head>`, before any stylesheet:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap" rel="stylesheet">
```

---

## Naming Conventions

- Template files: `snake_case.html`
- CSS classes: Tailwind utilities first; custom classes only when Tailwind cannot do it
- Custom CSS class names: `kebab-case` (e.g. `.post-header`, `.map-embed`)
- IDs: `kebab-case`, used sparingly (only when JS needs a direct hook)

---

## CSS Rules

- All custom styles go in `blog/static/blog/css/blog.css`
- Use CSS variables for fonts (defined in `blog.css` root):
  ```css
  :root {
    --font-serif: 'Lora', Georgia, serif;
    --font-sans:  'DM Sans', system-ui, sans-serif;
  }
  ```
- Do not write `<style>` blocks inside templates
- Do not use inline `style=""` attributes
- Tailwind utilities are preferred over new CSS rules
- Custom CSS is only written when a Tailwind utility cannot do the job

---

## JavaScript Rules

- No JS frameworks (no React, Vue, Alpine, etc.)
- Vanilla JS only, loaded via `{% block extra_js %}` at the bottom of `base.html`
- Tailwind has no bundled JS — write vanilla JS for all interactive behaviour
- Do not load jQuery

---

## Static Files

- Source static files live in `<app>/static/<app>/` (e.g. `blog/static/blog/css/`)
- `collectstatic` outputs to `staticfiles/` at the project root (production only)
- Always reference with `{% load static %}` and `{% static 'path' %}`
- User-uploaded media (post covers, etc.) goes to Cloudflare R2 — never committed to the repo

---

## Responsive Design

- Mobile-first: use Tailwind's responsive prefixes (`sm:`, `md:`, `lg:`) for all layout
- Test at: 375px (mobile), 768px (tablet), 1280px (desktop)
- No horizontal scrolling at any breakpoint

---

## Accessibility

- Every `<img>` must have a descriptive `alt` attribute
- Use semantic HTML (`<article>`, `<header>`, `<footer>`, `<main>`, `<nav>`, `<time>`)
- Colour contrast must meet WCAG AA (4.5:1 for body text) — the brand palette is designed to meet this on Cream backgrounds
- Interactive elements must be keyboard-navigable

---

## Map Embeds (Folium)

- Folium maps are rendered server-side and injected as raw HTML
- Use `{{ map_html | safe }}` — never remove the `safe` filter, the output is trusted server HTML
- Map containers must have an explicit height in CSS (e.g. `height: 400px`)

---

## Things to Avoid

- Using Bootstrap (fully replaced by Tailwind)
- Mixing Tailwind with Bootstrap classes
- Inline styles or `<style>` blocks in templates
- JS frameworks without an explicit decision to adopt one
- Committing compiled/minified CSS or JS to the repo
- White (`#fff`) as a page background — use Cream (`#F2EBD5`)
- Pure black text — use Ink (`#1A1610`)
- Large border radii (>6px on content elements)
- Gradients (except hero card image decoration)
- Inter, Roboto, or system-ui in user-facing text — always load Lora + DM Sans
