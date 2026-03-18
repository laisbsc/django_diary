# SEO strategy — laisbsc.dev

Single source of truth for SEO configuration of the `laisbsc.dev` blog, built with Django and hosted on Render.

---

## Architecture

- **Domain strategy:** Subfolders (`laisbsc.dev/blog/`) — keeps SEO authority on the root domain rather than splitting it across subdomains.
- **Protocol:** HTTPS mandatory (required for `.dev` TLD). Managed automatically by Render.
- **Content source:** Django database (posts authored in admin, body stored as Markdown, rendered server-side). Not file-based — no sync script needed.
- **Staging:** Ephemeral database. **Production:** Persistent PostgreSQL on Render.

---

## Technical SEO files

### `robots.txt` — served at `/robots.txt`

```text
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /config/
Disallow: /private/

Sitemap: https://laisbsc.dev/sitemap.xml
```

### `sitemap.xml` — auto-generated at `/sitemap.xml`

Powered by `django.contrib.sitemaps` via `blog/sitemaps.py`.

| URL | Priority | Changefreq |
|---|---|---|
| `laisbsc.dev/` | 1.0 | weekly |
| `laisbsc.dev/blog/` (post list) | 0.8 | weekly |
| `laisbsc.dev/blog/<slug>/` (posts) | 0.6 | weekly |

---

## Meta tags (in `base.html`)

| Tag | Limit | Purpose |
|---|---|---|
| `<title>` | < 60 chars | Primary keyword + brand: `Post title \| laisbsc.dev` |
| `<meta name="description">` | < 160 chars | Action-oriented summary from `post.excerpt` |
| `<link rel="canonical">` | — | Prevents duplicate content if cross-posting to Dev.to / Medium |
| `og:image` | 1200×630px | Visual hook for Twitter / LinkedIn shares |

All meta tags are implemented in `templates/base.html` (`{% block meta %}`) and overridden per post in `templates/blog/detail.html`.

---

## Content structure per post

Follow this hierarchy in every post body so Google understands the technical depth:

1. **H1** — exactly one per page; contains the main keyword.
2. **TL;DR** — 2-sentence summary near the top (targets Featured Snippets).
3. **H2 / H3** — logical sub-headers for technical steps.
4. **Code blocks** — use language identifiers (` ```python `) for technical indexing.
5. **Alt text** — describe every image for accessibility and Image Search.
6. **Internal links** — at least one link to another page on `laisbsc.dev` per post.

---

## Deployment checklist (Render)

- [ ] `ALLOWED_HOSTS` includes `laisbsc.dev`
- [ ] `CSRF_TRUSTED_ORIGINS` includes `https://laisbsc.dev`
- [ ] SSL/TLS active (auto-managed by Render)
- [ ] Register site on Google Search Console and submit `https://laisbsc.dev/sitemap.xml`
- [ ] Verify `robots.txt` is accessible at `https://laisbsc.dev/robots.txt`
- [ ] Set `SECURE_HSTS_PRELOAD = True` in production settings (already done)

---

## Canonical tag

Add to `{% block meta %}` in `base.html` to handle cross-posting:

```html
<link rel="canonical" href="{{ request.build_absolute_uri }}">
```

This is the only tag not yet implemented — see base.html TODO below.
