# NearCart (Vinavidai)

**Hyperlocal shop management + in-store product discovery.**
Shop owners run billing (POS), inventory and purchasing; shoppers find which nearby shop has a product in stock and *where in the store* it sits (floor → aisle → shelf → bin).

---

## Repositories

| Folder | GitHub repo | What it is |
|---|---|---|
| `backend/` | `ROMANVIKI/vinavidai` (this repo) | Django REST API + PostGIS |
| `frontend/` | `ROMANVIKI/vinavidai` (this repo) | Shopper-facing web app (prototype) |
| `nearCartMaster/` | `ROMANVIKI/nearCartBilling` | Shop-owner web dashboard (POS, inventory) |
| `nearCartMob2/` | `ROMANVIKI/nearCartMob` | Shop-owner mobile app (Expo) |
| `nearCartMobBuyer/` | `ROMANVIKI/nearCartBuyerApp` | Shopper mobile app (Expo, sample data) |

## Architecture

```
 Shopper web (frontend)      Shopper app (nearCartMobBuyer)
          │  (sample data today)          │  (sample data today)
          ▼                               ▼
 ┌────────────────────────────────────────────────┐
 │              Django REST API (backend)         │
 │  accounts · shops · inventory · billing        │
 │  JWT auth · PostGIS · Redis · Unfold admin     │
 └────────────────────────────────────────────────┘
          ▲                               ▲
          │                               │
 Owner web (nearCartMaster)     Owner app (nearCartMob2)
```

## Tech stack at a glance

- **Backend:** Python 3.14, Django 6, DRF, SimpleJWT, PostgreSQL 16 + PostGIS, Redis, Celery (configured), django-unfold admin, uv
- **Web:** React 19, Vite 8 (React Compiler), Tailwind CSS 4, Zustand / TanStack Query, Recharts
- **Mobile:** Expo SDK 54, React Native 0.81, React 19, TypeScript, React Navigation 7, Zustand
- **Infra:** Docker Compose (PostGIS, Redis, backend, Metabase), GitHub Actions (Ruff lint, frontend build, CodeQL), Dependabot

## Quick start (backend + database)

```bash
# create backend/.env first (variables listed in backend/README.md)
docker compose up --build
docker compose exec backend uv run python manage.py migrate
docker compose exec backend uv run python manage.py createsuperuser
```

- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/
- Metabase (BI): http://localhost:3000/

Then run whichever client you need — see that folder's README.

## Current status

| Area | Status |
|---|---|
| Auth (email OTP signup, JWT login) | Working on backend |
| Inventory, products, images, stock movements | Working end to end (backend, owner web, owner mobile) |
| POS billing → order → invoice | Working end to end |
| Purchase orders, suppliers, returns | Backend + owner mobile; owner web still on mock data |
| Shop geo search (`/api/shops/nearby/`) | Backend ready, no client uses it yet |
| Shopper apps (web + mobile) | UI prototypes on hard-coded sample data |
| Search, analytics, notifications apps | Models only, no endpoints yet |

## Known issues to fix first

1. Mobile signup calls `/api/accounts/register/...` but the backend serves `/api/auth/register/...`.
2. Mobile sessions expect a `refresh` token in the response body; the backend only sets an HttpOnly cookie, so mobile cannot refresh.
3. Owner web signup calls `/api/auth/register/`, which is not routed (only the OTP endpoints are).
4. Shopper web API layer targets endpoints (`/products/`, `/stores/`, `/auth/token/`) that do not exist on the backend.
5. Python version mismatch: `pyproject.toml`/CI use 3.14, `Dockerfile` uses `python:3.12-slim`.
6. `docker-compose.yml` healthcheck references `${DB_USER}` which is not defined.
7. Frontend CI caches `frontend/package-lock.json` but the folder uses `bun.lock`.
8. Rotate any credentials that were ever stored in `.env` files shared outside git.
