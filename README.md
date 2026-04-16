# laís. — personal blog

> This repo is used as a live demo for the DjangoCon EU 2026 talk. Slides: [pitch.com/v/djangocon_eu_26-iy8iir](https://pitch.com/v/djangocon_eu_26-iy8iir)

A travel and writing blog built with Django, deployed on Render. Posts support Markdown, interactive maps via Folium, and AI image generation.

## Stack

- **Backend:** Django 5.2, Python 3.13
- **Database:** PostgreSQL (Render) / SQLite (local)
- **Static files:** WhiteNoise
- **Media storage:** Render persistent disk
- **Task queue:** Django-Q (background image generation)
- **Maps:** Folium
- **Observability:** Logfire
- **Package manager:** uv

## Local setup

```bash
git clone https://github.com/laisbsc/django_diary.git
cd django_diary

# Install dependencies
uv sync

# Copy and fill in environment variables
cp .env.example .env

# Run migrations
uv run python manage.py migrate

# Create a superuser
uv run python manage.py createsuperuser

# Start the dev server
DJANGO_SETTINGS_MODULE=travel_diaries.settings.local uv run python manage.py runserver
```

App runs at `http://127.0.0.1:8000`. Admin at `/admin`.

### With Tailwind CSS live reload

Run these in two separate terminals:

```bash
# Terminal 1 — CSS watcher
DJANGO_SETTINGS_MODULE=travel_diaries.settings.local uv run python manage.py tailwind start

# Terminal 2 — dev server
DJANGO_SETTINGS_MODULE=travel_diaries.settings.local uv run python manage.py runserver
```

### AI image generator

Requires `OPENAI_API_KEY` in `.env`. Also run the task worker in a second terminal:

```bash
DJANGO_SETTINGS_MODULE=travel_diaries.settings.local uv run python manage.py qcluster
```

Visit `/ai/generate-image/` while logged in. Generation runs in the background — the page polls for completion automatically.

## Environment variables

See `.env.example`. Required locally: `SECRET_KEY` and `OPENAI_API_KEY`. Everything else is production-only and set in the Render dashboard.

## Deployment

Deployed via `render.yaml` (Infrastructure as Code). Two environments:

| Environment | Branch | Database |
|---|---|---|
| Production | `main` | Render PostgreSQL Starter |
| Staging | `staging` | Render PostgreSQL Free (ephemeral) |

Render runs the following on each deploy:
```bash
pip install uv && uv sync --frozen && uv run python manage.py collectstatic --no-input && uv run python manage.py migrate
```

Start command (runs web server and task worker in the same service):
```bash
bash -c "uv run python manage.py qcluster & uv run gunicorn travel_diaries.wsgi:application --bind 0.0.0.0:$PORT --workers 2"
```

## Project structure

```
travel_diaries/settings/
    base.py       # shared settings
    local.py      # local dev (SQLite, DEBUG=True)
    production.py # Render (PostgreSQL, WhiteNoise, persistent disk)

blog/             # posts, categories, about page
map/              # location model + Folium map views
ai_tools/         # image generation (pydantic-ai, Django-Q, gallery)
templates/        # project-level templates (base, blog list/detail)
docs/             # brand.md, seo.md
```

## Docs

- [`docs/brand.md`](docs/brand.md) — design system and brand guidelines
- [`docs/seo.md`](docs/seo.md) — SEO strategy and deployment checklist
- [`FRONTEND.md`](FRONTEND.md) — frontend dev conventions
- [`PLAN.md`](PLAN.md) — development roadmap
