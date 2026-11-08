# Smart QA Framework – Python

## Overview

A hybrid **API + UI** test automation framework. The system under test is split
into two deliberately small pieces:

| Layer | What it is | Owns |
| :--- | :--- | :--- |
| **Backend data** | [Fake Store API](https://fakestoreapi.com) — real, external, read-only | Product catalog (`GET /products`, `GET /products/<id>`; 20 products) |
| **Frontend UI** | [`flask-shop-demo`](https://github.com/fransuarez/flask-shop-demo) — thin Flask + Jinja app | UI routes, templates, **session cart / checkout** |
| **Test harness** | This repository | BDD scenarios, API-direct tests, page objects, CI |

> **Why the split?** The test framework is the deliverable. A real external
> catalog (Fake Store) plus a small, fully-controlled UI (Flask) gives the tests
> a stable data source *and* a UI we can drive deterministically, without
> building or maintaining a full backend.

> **Critical constraint — read before writing tests**
> Fake Store API's write endpoints (`/carts`, etc.) are **simulated and do not
> persist**. They are never used as a source of truth. The catalog is read-only.
> **Cart and checkout state live entirely in the Flask session** and belong to
> the frontend, not to Fake Store.

## Architecture in one picture

```
Fake Store API (real, external)          ← GET /products, /products/<id>
        ▲
        │ HTTP (re-fetched per request)
Flask + Jinja frontend (thin, no DB)     ← UI routes + session cart {id: qty}
        ▲
        │ HTTP + browser
behave / pytest / Playwright             ← this repository
   ├── API-direct: hits Fake Store for catalog checks
   ├── UI: drives Flask pages via data-testid
   └── Applitools / LLM / Healenium (planned)
```

No database. No migrations. No admin CRUD. Any of those would re-introduce a
backend we deliberately chose not to build.

## Quick Start — two terminals, no Docker, no DB

**Terminal 1 — the frontend under test**

```bash
git clone git@github.com:fransuarez/flask-shop-demo.git
cd flask-shop-demo
python -m venv .venv && source .venv/bin/activate
pip install flask requests
flask run                     # http://127.0.0.1:5000
# or: python app.py
```

**Terminal 2 — the test suite**

```bash
git clone git@github.com:fransuarez/smart-qa-framework-python.git
cd smart-qa-framework-python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
behave                        # BDD / UI scenarios
pytest tests/api              # API-direct checks against Fake Store
```

That is the whole setup. If both terminals print success, the hybrid flow works.

## Project Status

| Area | State |
| :--- | :--- |
| `flask-shop-demo` thin frontend (session cart, no DB) | ✅ external |
| Fake Store API as read-only catalog | ✅ external |
| Framework bootstrap (README, layout) | ✅ present |
| behave skeleton (`features/`, `environment.py`) | 🚧 planned |
| `data-testid` hooks in `flask-shop-demo` templates | ✅ present (13 hooks) |
| Page objects (`pages/`) keyed on `data-testid` | 🚧 planned |
| API-direct pytest suite (`tests/api/`) | 🚧 planned |
| Session-reset fixture (fresh cookie jar per scenario) | 🚧 planned |
| LLM test-data generator (`utils/ai_data_generator.py`) | 🚧 planned |
| Applitools wrapper (`utils/visual_ai.py`) | 🚧 planned |
| Healenium docker-compose (`docker/healenium.yml`) | 🚧 planned |
| CI workflow (`.github/workflows/test-pipeline.yml`) | 🚧 planned |

No CI badge until the workflow exists.

## SUT Contract — as implemented by `flask-shop-demo/app.py`

The framework relies on exactly these facts. **If any change, update both the
owning repo and this table.**

### Fake Store (catalog, read-only)

| Surface | Contract |
| :--- | :--- |
| Base URL | `https://fakestoreapi.com` (override: `FAKESTORE_BASE_URL`) |
| `GET /products` | 20 products; each has `id`, `title`, `price`, `category`, `image` |
| `GET /products/<id>` | Single product; `404` for unknown IDs |
| IDs | Stable within a run; **never assume an ID beyond 1–20 exists** |
| Writes | **Simulated, non-persistent. Never used as a source of truth.** |

### Flask frontend (UI + session cart)

| Surface | Method | Contract |
| :--- | :--- | :--- |
| `/` | GET | Renders `products.html`. On catalog fetch error: empty list + flash (`"The product catalog is temporarily unavailable."`). |
| `/cart/add/<int:product_id>` | POST | **Re-fetches the catalog to validate the ID.** Unknown ID → `404`. Known ID → increments `session["cart"][str(id)]` by 1, flashes `"Added to cart."`, redirects to `/`. |
| `/cart` | GET | Fetches catalog, builds `{product, quantity, subtotal}` list, computes `total` (`Decimal`), renders `cart.html`. |
| `/cart/remove/<int:product_id>` | POST | Removes the ID from the session cart, redirects to `/cart`. |
| `/checkout` | GET | **If cart empty → redirects to `/` with flash `"Your cart is empty."`.** Otherwise renders `checkout.html` with `completed=False`. |
| `/checkout` | POST | Same empty-cart guard. Requires non-empty form field `name`; missing → flash `"Please enter your name."` + redirect to `/checkout`. Success → clears `session["cart"]`, renders `checkout.html` with `completed=True`, `order_name=<name>`. |
| Persistence | — | **Session cookie only.** Cart is `{ "<product_id>": <quantity> }`. No DB, no server store. |
| `secret_key` | — | Hardcoded `"poc-secret-key"` in the PoC — acceptable locally, must be replaced before any deployment. |

> Negative paths (`404` on unknown product, `302` redirects for empty cart and
> missing `name`, catalog-unavailable flash) are enumerated in
> [Negative and edge scenarios](#negative-and-edge-scenarios).

### Test Hook Contract

All UI elements addressed by the suite carry a `data-testid` attribute. Tests
select by these only — never by CSS classes or XPath. The list below is the
**verified** contract; it mirrors `flask-shop-demo/README.md` *Testing Hooks*
exactly, and both files must change together if a hook is added or renamed.

| Element | Selector | Location |
| :--- | :--- | :--- |
| Product card | `[data-testid="product-card"][data-product-id="<id>"]` | `products.html` |
| Add to cart | `[data-testid="add-to-cart-<id>"]` | `products.html` |
| Empty catalog | `[data-testid="products-empty"]` | `products.html` |
| Cart link (header) | `[data-testid="cart-link"]` | `base.html` |
| Cart row | `[data-testid="cart-row"][data-product-id="<id>"]` | `cart.html` |
| Cart quantity | `[data-testid="cart-qty-<id>"]` | `cart.html` |
| Remove from cart | `[data-testid="remove-from-cart-<id>"]` | `cart.html` |
| Empty cart | `[data-testid="cart-empty"]` | `cart.html` |
| Checkout button | `[data-testid="checkout-btn"]` | `cart.html` |
| Name input | `[data-testid="checkout-name"]` | `checkout.html` |
| Place order | `[data-testid="confirm-order"]` | `checkout.html` |
| Order confirmation (Applitools anchor) | `[data-testid="order-confirmed"]` | `checkout.html` |
| Flash message | `[data-testid="flash"][data-category="<success\|error>"]` | `base.html` |

If a hook is missing, add it to `flask-shop-demo` and update both READMEs —
never fall back to CSS or XPath in the tests.

## Test Isolation — session, not DB

Because there is no database and Fake Store is read-only:

- **Per-scenario cookie jar reset** — each Playwright context starts empty, so
  `session["cart"]` is fresh.
- **Catalog is shared** — assert against known IDs (product 1 exists; IDs 1–20)
  rather than "whatever rendered first."
- **No ordering assumptions** — scenarios pass in any order and can run in parallel.
- **No DB to reset, no migrations to run** — this is a feature, not a gap.
- **Network failures are skips, not failures** — if Fake Store is unreachable,
  `/` renders the flash fallback. CI should treat that as `@skip` (or use a
  network-failure fixture that asserts the flash path explicitly).

## Demo Flow (the hybrid link)

### Happy path

1. **API-direct**: `GET https://fakestoreapi.com/products`, pick a known ID (e.g. `1`).
2. **UI**: open `http://127.0.0.1:5000/`, click `[data-testid="add-to-cart-1"]`.
3. Go to `/cart`, assert `[data-testid="cart-row"][data-product-id="1"]` exists
   (and quantity is at least 1).
4. Go to `/checkout` (GET), fill `[data-testid="checkout-name"]`, submit
   (**POST**) → assert `[data-testid="order-confirmed"]` visible.
5. Applitools captures the confirmation page.

Step 1 (API) and steps 2–4 (UI) run against the **same catalog**, so the ID
asserted via the API is the ID clicked in the UI. That is the hybrid guarantee.

### Negative and edge scenarios

These fall out of `flask-shop-demo/app.py` as written and must be covered by the
suite. Each is pinned to a route behavior in the *SUT Contract* table above and
to a `data-testid` hook where applicable.

| Scenario | Expected outcome | Hook / assertion |
| :--- | :--- | :--- |
| `POST /cart/add/9999` (unknown ID) | `404`, cart unchanged | HTTP status only — no DOM hook needed |
| `GET /checkout` with an empty cart | `302` → `/`, error flash | `[data-testid="flash"][data-category="error"]` |
| `POST /checkout` with empty `name` | `302` → `/checkout`, error flash, **cart preserved** | `[data-testid="flash"][data-category="error"]` + `[data-testid="cart-row"]` still present on `/cart` |
| `POST /checkout` with valid `name` | confirmation page rendered | `[data-testid="order-confirmed"]` visible |
| Fake Store unreachable (mocked) | `GET /` renders empty catalog + error flash | `[data-testid="products-empty"]` + `[data-testid="flash"][data-category="error"]` |
| Add the same product twice | quantity becomes `2`, **one row only** | `[data-testid="cart-qty-<id>"]` reads `2`; exactly one `[data-testid="cart-row"][data-product-id="<id>"]` |

## Project Structure

```
smart-qa-framework-python/
├── README.md
├── requirements.txt
├── requirements-dev.txt          # 🚧 planned
├── features/                     # 🚧 planned: behave + environment.py
├── pages/                        # 🚧 planned: page objects on data-testid
├── tests/api/                    # 🚧 planned: pytest vs Fake Store
├── utils/                        # 🚧 planned: ai_data_generator, visual_ai, self_healing
└── docs/
    ├── context.md                # 🚧 planned: architecture decisions (incl. Option A/B)
    ├── setup.md                  # 🚧 planned
    └── ai-modules.md             # 🚧 planned
```

## Configuration

| Variable | Purpose | Default |
| :--- | :--- | :--- |
| `FAKESTORE_BASE_URL` | Fake Store endpoint | `https://fakestoreapi.com` |
| `FLASK_BASE_URL` | Frontend under test | `http://127.0.0.1:5000` |
| `APPLITOOLS_API_KEY` | Enables visual checks | unset → skipped |
| `OPENAI_API_KEY` / `GEMINI_API_KEY` | Enables LLM data | unset → deterministic fixtures |

Unset keys **skip** the corresponding feature; they never fail the run. CI
without secrets still executes the core suite.

## Documentation

- `flask-shop-demo/README.md` — UI routes, templates, `data-testid` hooks
- `flask-shop-demo/app.py` — the authoritative source for route behavior
- `https://fakestoreapi.com` — catalog payload contract
- `docs/context.md`, `docs/setup.md`, `docs/ai-modules.md` — 🚧 planned

## Working across sessions

```bash
git archive --format=zip --output=../smart-qa-snapshot.zip HEAD
git ls-files > ../smart-qa-files.txt
```

## TODO

- Scaffold `features/` + `environment.py` (Playwright + session reset + Applitools hook)
- Add page objects keyed on the verified `data-testid` contract
- Add API-direct pytest suite against Fake Store
- Decide `/api/products` mirror vs direct; record in `docs/context.md`
- Add negative scenarios (404, empty-cart redirect, missing name)
- Add LLM test-data generator with deterministic fallback
- Add Applitools wrapper gated on `APPLITOOLS_API_KEY`
- Add Healenium docker-compose + driver wrapper
- Add CI workflow; then enable the badge
- Add `LICENSE`