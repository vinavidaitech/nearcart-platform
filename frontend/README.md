# NearCart Shopper Web (frontend)

Customer-facing React web app for finding a product at nearby stores and being guided to its exact spot in the store. **Currently a UI prototype running on hard-coded sample data.**

## Features

- Marketing landing page (hero, features, how it works, store-owner section, stats, testimonials)
- Product search results with category navigation, filter chips and product cards (price, stock, rating, badges, colour swatches)
- Product detail page: images, size/colour selectors, store info, in-store aisle location, related products, wishlist toggle
- In-store navigation page: map visualisation with markers and step-by-step directions (floor → aisle → rack → shelf)
- API layer and React Query hooks written (not yet wired to pages)

## Tech stack

| | |
|---|---|
| Framework | React 19 + Vite 8 (React Compiler via Babel) |
| Styling | Tailwind CSS 4, custom CSS variables, Outfit and Nunito fonts |
| Routing | React Router 7 |
| Data | TanStack Query 5 (+ devtools), Axios |
| Icons | lucide-react, react-icons |
| Tooling | ESLint 10, Bun lockfile |

## Routes

| Path | Page |
|---|---|
| `/` | Landing |
| `/search` | Search results |
| `/product/:id` | Product detail |
| `/navigate/:id` | In-store navigation |

## Getting started

```bash
cd frontend
bun install        # or npm install
bun run dev        # http://localhost:5173
bun run build
```

Vite proxies `/api` to `http://localhost:8000`. Set `VITE_API_URL` to point elsewhere.

## Structure

```
src/
├── api/            # raw API calls
├── components/     # layout, ui, sections (landing + search)
├── constants/      # sample product data (current data source)
├── hooks/          # React Query hooks
├── lib/            # axios instance, query client
└── pages/
```

## Status & TODO

- Pages read from `src/constants/data.js`; the hooks in `src/hooks/useProducts.jsx` are written but commented out.
- API paths (`/products/`, `/stores/`, `/auth/token/`) do not match the backend. Backend has `/api/shops/nearby/` and `/api/inventory/...`; a public shopper search endpoint still needs to be built.
- Auth redirects to `/login`, which has no route.
- CI workflow caches `package-lock.json`, but this folder uses `bun.lock`.
