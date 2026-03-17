# Frontend Guidelines

## Stack

| Concern | Tool |
|---|---|
| CSS framework | Tailwind CSS via PostCSS build (replacing Bootstrap 5.3.3) |
| Custom styles | `blog/static/css/blog.css` |
| Maps | Folium (server-rendered, embedded as iframe/HTML) |
| JavaScript | Vanilla JS only — no framework |
| Icons | To be decided (Heroicons recommended, same Tailwind family) |

> **Migration note:** The project was originally built with Bootstrap 5.3.3. All Bootstrap classes and CDN references are being replaced with Tailwind. Do not mix the two frameworks.

---

## Template Structure

Templates live inside each app under `<app>/templates/<app>/`.

```
blog/templates/blog/
    base.html         ← master layout, imported by all blog templates
    post_list.html
    post_detail.html

map/templates/map/
    post_list_by_location.html
```

All templates extend `blog/base.html` unless a new base is explicitly needed.

### base.html blocks

| Block | Purpose |
|---|---|
| `{% block title %}` | Page `<title>` tag |
| `{% block content %}` | Main page body |

New blocks (e.g. `{% block extra_css %}`, `{% block extra_js %}`) should be added to `base.html` before use — never inline styles or scripts in child templates.

---

## Naming Conventions

- Template files: `snake_case.html`
- CSS classes: Bootstrap utilities first, custom classes only when Bootstrap cannot do it
- Custom CSS class names: `kebab-case` (e.g. `.post-header`, `.map-embed`)
- IDs: `kebab-case`, used sparingly (only when JS needs a hook)

---

## CSS Rules

- All custom styles go in `blog/static/css/blog.css`
- Do not write `<style>` blocks inside templates
- Do not use inline `style=""` attributes
- Tailwind utility classes are preferred over writing new CSS
- Custom CSS is only written when a Tailwind utility cannot do the job

### Colour palette

| Name | Hex | Role |
|---|---|---|
| Cream | `#F2EBD5` | Page background |
| Amber | `#E8A62C` | Primary accent, CTA buttons |
| Sand | `#D9C49C` | Secondary backgrounds, cards |
| Sienna | `#D98723` | Hover states, borders |
| Cobalt | `#153FB3` | Links, active states |

Add these to `tailwind.config.js` under `theme.extend.colors`:

```js
colors: {
  cream:   '#F2EBD5',
  amber:   '#E8A62C',
  sand:    '#D9C49C',
  sienna:  '#D98723',
  cobalt:  '#153FB3',
}
```

---

## JavaScript Rules

- No JS frameworks (no React, Vue, Alpine, etc.)
- Vanilla JS only, loaded at the bottom of `base.html` via `{% block extra_js %}`
- Tailwind's CDN does not include JS components — use vanilla JS for interactive behaviour (modals, dropdowns)
- Do not load jQuery

---

## Static Files

- Source static files live in `<app>/static/<app>/` (e.g. `blog/static/blog/css/`)
- `collectstatic` outputs to `staticfiles/` at the project root (production only)
- Always reference static files with `{% load static %}` and `{% static 'path' %}`
- Images uploaded by users (post covers, etc.) go to Cloudflare R2 — never committed to the repo

---

## Responsive Design

- Mobile-first: use Tailwind's responsive prefixes (`sm:`, `md:`, `lg:`) for all layout
- Test at: 375px (mobile), 768px (tablet), 1280px (desktop)
- No horizontal scrolling at any breakpoint

---

## Accessibility

- Every `<img>` must have a descriptive `alt` attribute
- Use semantic HTML (`<article>`, `<header>`, `<footer>`, `<main>`, `<nav>`, `<time>`)
- Colour contrast must meet WCAG AA minimum (4.5:1 for body text)
- Interactive elements must be keyboard-navigable

---

## Map embeds (Folium)

- Folium maps are rendered server-side and embedded as raw HTML
- Use `{{ map_html | safe }}` — never strip the `safe` filter, the output is trusted server HTML
- Map containers should have an explicit height set in CSS (e.g. `height: 400px`)
- Do not nest a Folium embed inside a Bootstrap `table`

---

## Things to avoid

- Using Bootstrap (fully replaced by Tailwind)
- Mixing Tailwind with Bootstrap classes
- Inline styles or `<style>` blocks in templates
- JavaScript frameworks without an explicit decision to adopt one
- Committing compiled/minified CSS or JS to the repo
