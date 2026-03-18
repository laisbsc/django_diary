# Frontend Guidelines

> For all design decisions — colours, typography, components, voice — refer to [`docs/brand.md`](docs/brand.md). That is the single source of truth. This file covers dev conventions only.

---

## Stack

| Concern | Tool |
|---|---|
| CSS framework | Tailwind CSS v3 via `django-tailwind` (PostCSS build) |
| Tailwind app | `theme/` — managed by `django-tailwind` |
| Fonts | Lora + DM Sans via Google Fonts `<link>` in `base.html` |
| Maps | Folium (server-rendered, embedded as iframe/HTML) |
| JavaScript | Vanilla JS only — no framework |
| Icons | Heroicons (recommended, same Tailwind family) |

Bootstrap has been fully removed. Do not reintroduce it.

---

## Tailwind setup

Tailwind is managed through the `theme` Django app created by `django-tailwind`.

| File | Purpose |
|---|---|
| `theme/static_src/tailwind.config.js` | Brand tokens, content paths, plugins |
| `theme/static_src/src/styles.css` | Tailwind directives + `@layer base` for CSS custom properties |
| `theme/static/css/dist/styles.css` | Compiled output — **do not edit directly** |

### Brand tokens in `tailwind.config.js`

```js
colors: {
  cream:       '#F2EBD5',
  amber:       '#E8A62C',
  sand:        '#D9C49C',
  sienna:      '#D98723',
  cobalt:      '#153FB3',
  ink:         '#1A1610',
  'ink-muted': '#5C4F35',
  'ink-light': '#9A8A6A',
},
fontFamily: {
  serif: ['Lora', 'Georgia', 'serif'],
  sans:  ['DM Sans', 'system-ui', 'sans-serif'],
},
```

### CSS custom properties

Kept in `styles.css` `@layer base` for CSS variables used by dynamic model-driven inline styles (category colour bars and tags — values come from `post.category.color` at runtime and cannot be resolved at build time by Tailwind):

```css
:root {
  --cobalt: #153FB3;
  --amber:  #E8A62C;
  --sienna: #D98723;
  /* ...full list in styles.css */
}
```

### Plugins installed

| Plugin | Use |
|---|---|
| `@tailwindcss/typography` | Prose styles for markdown-rendered post bodies (`prose` class) |
| `@tailwindcss/forms` | Minimal form resets |
| `@tailwindcss/aspect-ratio` | Aspect ratio utilities |

### Local dev commands

```bash
# Watch mode — recompiles on template changes
uv run python manage.py tailwind start

# One-off production build
uv run python manage.py tailwind build
```

Run `tailwind start` alongside `runserver` in separate terminals during development.

### Render build command

See `render.yaml` — the build command includes `tailwind build` before `collectstatic`.

---

## Template Structure

Templates live in the project-level `templates/` directory. There are no app-level templates.

```
templates/
    base.html               ← master layout
    robots.txt
    blog/
        list.html           ← post list + hero
        detail.html         ← post article + sidebar
        about.html          ← about page (markdown body)
```

### `base.html` blocks

| Block | Purpose |
|---|---|
| `{% block title %}` | Page `<title>` tag |
| `{% block meta %}` | SEO/OG meta tags — overridden per page |
| `{% block content %}` | Main page body |
| `{% block extra_css %}` | Per-page styles (rare) |
| `{% block extra_js %}` | Per-page scripts, loaded at bottom of `<body>` |

### `{% tailwind_css %}` tag

`base.html` loads Tailwind via `{% load tailwind_tags %}` and `{% tailwind_css %}`. Do not add a manual `<link>` to the compiled CSS — the tag handles it.

---

## Naming Conventions

- Template files: `snake_case.html`
- Tailwind utilities inline in HTML — no custom class names unless a utility cannot do the job
- If a custom class is needed, add it to `styles.css` using `@layer components`

---

## CSS Rules

- Tailwind utilities inline in HTML are the default approach
- Do not write `<style>` blocks inside templates
- Do not use inline `style=""` attributes **except** for dynamic model-driven values (category colour bars/tags use `style="background: var(--{{ post.category.color }});"` — this is intentional)
- Custom CSS goes in `theme/static_src/src/styles.css` using `@layer components` or `@layer utilities`

---

## JavaScript Rules

- No JS frameworks (no React, Vue, Alpine, etc.)
- Vanilla JS only, loaded via `{% block extra_js %}` at the bottom of `base.html`
- Do not load jQuery

---

## Static Files

- Tailwind compiled CSS: `theme/static/css/dist/styles.css` (generated — not committed)
- `collectstatic` outputs to `staticfiles/` at the project root (production only)
- User-uploaded media (post covers) → Cloudflare R2 — never committed to the repo
- Always reference static files with `{% load static %}` and `{% static 'path' %}`

---

## Responsive Design

- Mobile-first: use Tailwind's responsive prefixes (`sm:`, `md:`, `lg:`)
- Test at: 375px (mobile), 768px (tablet), 1280px (desktop)
- No horizontal scrolling at any breakpoint

---

## Accessibility

- Every `<img>` must have a descriptive `alt` attribute
- Use semantic HTML (`<article>`, `<header>`, `<footer>`, `<main>`, `<nav>`, `<time>`)
- Colour contrast must meet WCAG AA (4.5:1 for body text)
- Interactive elements must be keyboard-navigable

---

## Map Embeds (Folium)

- Folium maps are rendered server-side and injected as raw HTML
- Use `{{ map_html | safe }}` — never remove the `safe` filter
- Map containers must have an explicit height (e.g. `class="h-[400px]"`)

---

## Things to Avoid

- Reintroducing Bootstrap
- Editing `theme/static/css/dist/styles.css` directly (it gets overwritten on build)
- Committing `theme/static_src/node_modules/`
- Inline styles except for dynamic category colour values
- White (`#fff`) as a page background — use `bg-cream`
- Pure black text — use `text-ink`
- Border radii above `rounded` (4px) on content elements
- Gradients except on the hero featured card image
- Inter, Roboto, or system-ui in user-facing text
