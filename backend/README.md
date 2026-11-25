# NearCart Backend

Django REST API powering NearCart: multi-shop inventory, POS billing, purchasing, geo-search of nearby shops, and a branded admin dashboard.

## Features

**Accounts & auth**
- Custom user model (UUID, email login) with roles: `shopper`, `owner`, `staff`, `admin`
- Email OTP signup (6-digit code, 10-minute expiry, 5 attempts, 3/min throttle) — OTP and pending data kept in Redis cache, password stored hashed
- JWT access tokens (15 min); refresh token in an HttpOnly cookie (7 days, scoped to `/api/auth/`), blacklist on logout
- `StaffMembership` model for per-shop staff permissions

**Shops**
- Shops with PostGIS `location`, categories, images, opening hours (JSON), status/verification, floor-plan URL
- `GET /api/shops/nearby/?lat=&lng=&radius=` radius search (km) over active shops
- Owners list their shops via `/api/shops/mine/`; slug-based detail with owner-only edits

**Inventory** (shop-scoped via `X-Shop-ID` header or `shop_id` param)
- Products, variants (JSON attributes), brands, categories, barcode/SKU, MRP vs price
- Multi-image upload with primary image
- In-store location: free-text floor/aisle/shelf/bin labels plus a 6-level `LocationNode` tree (floor → section → aisle → rack → shelf → bin)
- Stock adjustments with immutable `StockMovement` audit log (sale, restock, adjustment, import, damaged, return)
- Low-stock / out-of-stock endpoints; signals keep `total_stock` in sync and record price history

**Billing**
- Customers, suppliers, tax rates, discounts (percentage / flat, validate endpoint)
- Purchase orders with receive action (updates stock)
- Sales orders (POS / online / phone channels): create → complete (deducts stock, writes movements, auto-generates invoice) or cancel; daily summary endpoint
- Invoices (read-only), payments (cash, UPI, card, bank, store credit), returns with approval
- `BulkImport` model for CSV import jobs (admin-side; no public endpoint yet)

**Admin**
- django-unfold admin with KPI/chart dashboard (`apps/core/dashboard.py`), sidebar badges for pending orders and unpaid invoices

**Modelled but not exposed yet**
- `analytics` (search events, impressions, direction clicks), `notifications` (wishlist, price alerts, recently seen), `search` (empty)
- Celery and Redis are configured, but no tasks are defined yet

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| Framework | Django 6, Django REST Framework |
| Auth | djangorestframework-simplejwt |
| Database | PostgreSQL 16 + PostGIS (GeoDjango) |
| Cache / broker | Redis 7 (django-redis, Celery) |
| Storage | Local disk (dev), S3-compatible via django-storages + boto3 (prod, e.g. Cloudflare R2) |
| Admin UI | django-unfold |
| Static files | WhiteNoise |
| Server | Gunicorn (prod), runserver (dev) |
| Tooling | uv, Ruff, pytest, pytest-django, factory-boy |
| Container | Docker, Docker Compose |
| CI | GitHub Actions (Ruff), CodeQL, Dependabot |

## Project structure

```
backend/
├── apps/
│   ├── accounts/       # CustomUser, StaffMembership, auth + OTP views
│   ├── shops/          # Shop, ShopCategory, ShopImage, nearby search
│   ├── inventory/      # Product, Variant, Brand, Category, LocationNode, StockMovement, PriceHistory
│   ├── billing/        # Customer, Supplier, PO, SalesOrder, Invoice, Payment, Return, BulkImport
│   ├── analytics/      # SearchEvent, ProductImpression, DirectionClick (models only)
│   ├── notifications/  # Wishlist, PriceAlert, RecentlySeen (models only)
│   ├── search/         # placeholder
│   └── core/           # Unfold dashboard callbacks
├── config/settings/    # base.py, local.py, production.py
├── templates/admin/    # custom dashboard template
├── Dockerfile
└── pyproject.toml
```

## API overview

Base: `/api/`. Pagination: 20 per page. Default permission: authenticated or read-only.

| Prefix | Endpoints |
|---|---|
| `auth/` | `login/`, `refresh/`, `logout/`, `me/`, `register/request-otp/`, `register/verify-otp/` |
| `shops/` | `categories/`, `nearby/`, `mine/`, list/create, `<slug>/` |
| `inventory/` | `products/` (+ `images`, `adjust-stock`, `movements`, `low-stock`, `out-of-stock`), `variants/`, `locations/`, `categories/`, `brands/`, `movements/` |
| `billing/` | `customers/`, `suppliers/`, `tax-rates/`, `discounts/` (+`validate`), `purchase-orders/` (+`receive`), `sales-orders/` (+`complete`, `cancel`, `summary`), `invoices/`, `payments/`, `returns/` (+`approve`) |

Shop-scoped endpoints require `X-Shop-ID: <shop uuid>`.

## Getting started

Prerequisites: Docker, Docker Compose (uv only if running outside Docker).

```bash
# from the repo root, after creating backend/.env
docker compose up --build

docker compose exec backend uv run python manage.py migrate
docker compose exec backend uv run python manage.py createsuperuser
docker compose exec backend uv run pytest
docker compose exec backend uv run ruff check .
```

### Environment variables

| Variable | Description |
|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.local` (dev) or `config.settings.production` |
| `DJANGO_SECRET_KEY` | Secret key |
| `DEBUG` | `True` / `False` |
| `ALLOWED_HOSTS` | Comma-separated hosts |
| `DATABASE_URL` | Must use the `postgis://` scheme |
| `REDIS_URL` | Redis connection URL |
| `CORS_ALLOWED_ORIGINS` | Allowed web origins (default `http://localhost:5173`) |
| `CSRF_TRUSTED_ORIGINS` | Trusted origins |

Never commit `.env`.

## Known issues / TODO

- Python: `pyproject.toml` requires 3.14, `Dockerfile` uses `python:3.12-slim`.
- Add `/api/auth/register/` or switch clients to the OTP flow (`RegisterView` exists but is not routed).
- Mobile clients expect a refresh token in the JSON body; only the cookie is issued.
- Email settings in `base.py` contain placeholders; move to env vars and define `DEFAULT_FROM_EMAIL`.
- Production S3/R2 storage needs `AWS_*` settings; they are not read yet.
- Implement search, analytics, notification endpoints, bulk import API, and Celery tasks.
- Hard-coded GDAL/GEOS paths in `base.py` are Linux specific.
