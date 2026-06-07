# BEE — Backend Engineering Encyclopedia

> **Project:** BEE (Backend Engineering Enclydopedia)  
> **Status:** Planning → Ready to build  
> **Last updated:** 2026-06-07  
> **Source assets:** `stitch_backend_engineering_search_encyclopedia.zip`  
> **Deployment:** Vercel (frontend + serverless API)

---

## 1. Vision

BEE is a **search-first, graph-driven knowledge platform** for backend engineers. It helps senior engineers quickly find, understand, and navigate relationships between backend problems, algorithms, and patterns — without the noise of generic tutorials.

**Core user flows:**

1. **Discover** — Browse categories (Performance, Scalability, Reliability, etc.) from a high-density homepage.
2. **Search** — Use a command palette (`⌘K`) with instant fuzzy + full-text search across 150+ encyclopedia entries.
3. **Learn** — Read rich markdown problem pages with code blocks, complexity metrics, and related concepts.
4. **Explore** — Visualize concept relationships in an interactive graph explorer.

**Design identity:** *Kinetic Syntax* — dark, Linear-like, glassmorphic, optimized for long deep-work sessions.

**Branding (locked):**

| Location | Copy |
|---|---|
| **Navbar** | `BEE` |
| **Homepage hero** | `BEE is a backend engineering encyclopidia` |
| **`<title>` / meta** | `BEE — Backend Engineering Encyclopedia` |

---

## 2. Source Materials (Stitch Export)

| Asset | Purpose |
|---|---|
| `bee_technical_spec.md` | Architecture, schema, component list, performance strategy |
| `kinetic_syntax/DESIGN.md` | Full design system (colors, typography, spacing, components) |
| `bee_homepage/code.html` | Homepage layout mockup (bento grid, sidebar, command palette) |
| `bee_circuit_breaker_detail/code.html` | Problem detail page mockup (TOC sidebar, code blocks, related tags) |
| `bee_graph_explorer/code.html` | Graph explorer mockup (node canvas, filters, relationship panel) |

These HTML mockups are the **visual source of truth** for UI implementation. They use Tailwind CDN + Material Symbols; the React app will translate them into CSS Modules + design tokens.

---

## 3. Tech Stack

| Layer | Choice | Notes |
|---|---|---|
| **Frontend** | React 19 + Vite + **TypeScript** | Migrate from JSX → TSX in Phase 0 |
| **State** | Zustand | Lightweight; search + UI prefs |
| **Routing** | React Router v7 | Already installed |
| **Animations** | Framer Motion | Already installed |
| **Client search** | Fuse.js | Offline fuzzy fallback over API-fetched index |
| **Styling** | CSS Modules + `token.css` | Kinetic Syntax tokens started |
| **Backend** | FastAPI (Python) via **Vercel Serverless** | Mangum ASGI adapter |
| **ORM** | SQLAlchemy (async) | Models → migrate to UUID PKs |
| **Validation** | Pydantic v2 | Schemas **not yet created** |
| **Database (prod)** | **Vercel Postgres** (Neon) | SQLite FTS5 for local dev only |
| **Server search** | PostgreSQL full-text (prod) / SQLite FTS5 (dev) | Dynamic queries — never serve raw JSON |
| **Graph** | **React Flow** | Best React integration + performance |
| **Markdown** | `react-markdown` + `rehype-highlight` | Full markdown articles per problem |
| **Deployment** | **Vercel** | Frontend static + API serverless functions |

---

## 4. Data Model

### Problem (core entity)

| Field | Type | Notes |
|---|---|---|
| `id` | **UUID** (`uuid4`) | Primary key — all FKs use UUID |
| `slug` | string | URL-safe kebab-case (`circuit-breaker-pattern`) |
| `title` | string | Display name |
| `category` | enum | API, Concurrency, Data, DevOps, Networking, Observability, Performance, Reliability, Scalability, Security |
| `algorithm` | string | e.g. "Circuit Breaker + Bulkhead" |
| `difficulty` | enum | Easy / Medium / Hard |
| `explanation` | text | Short summary for search/cards |
| `markdown_content` | text | **Full markdown article** (headings, code fences, lists) |
| `technologies` | JSON array | e.g. `["Redis", "Kafka"]` |
| `complexity` | JSON | `{ "time": "O(1)", "space": "O(n)" }` |
| `tags` | M2M via `Tag` | Searchable metadata |
| `related_problems` | M2M via `Relationship` | Graph edges (UUID FKs) |
| `created_at` | datetime | Audit |

### Supporting entities

- **Tag** — normalized tag names
- **Relationship** — directed edges (`source_id`, `target_id`, `type`, `strength`)
- **Analytics** — search queries, concept views, trending (server-side only; no PII)

> **No auth, no bookmarks API.** Bookmarks are client-only (localStorage) if added later. The API is **read-only** (`GET` only on public routes).

### Content pipeline (not static JSON)

```
problem.json (seed source, dev only)
       ↓  one-time seed script
   PostgreSQL / SQLite DB
       ↓  SQLAlchemy + FTS
   FastAPI dynamic responses
       ↓  axios
   React frontend
```

- `problem.json` is **never** served directly to the client.
- Seed script transforms `description` → structured **markdown articles** and loads into DB.
- All `/api/v1/*` responses come from the database at request time.

### Seed data

`backend/app/data/problem.json` — **150 problems** across 10 categories. Seed script generates markdown bodies and assigns UUIDs.

---

## 5. Current State Audit

### ✅ Done

| Area | Status |
|---|---|
| Project folder structure (`frontend/`, `backend/app/`) | Exists |
| Kinetic Syntax design tokens (`frontend/src/styles/token.css`) | ~90% complete |
| Backend models (`Problem`, `Tag`, `Relationship`, `Bookmark`, `Analytics`) | Defined |
| Backend route stubs (`/problems`, `/search`, `/graph`, `/bookmarks`, `/analytics`, `/recommendations`) | Written |
| Backend repositories (problem, tag, relationship, bookmark, analytics) | Written |
| Search engine modules (FTS, tokenizer, query parser, ranking, suggestions) | Stubbed |
| Core config, logging, constants, dependencies | Written |
| Seed data (`problem.json`, 150 entries) | Ready |
| Frontend deps (axios, fuse.js, framer-motion, react-router-dom) | Installed |

### ❌ Missing / Incomplete

| Area | Gap |
|---|---|
| `backend/app/main.py` | FastAPI app entry point |
| `backend/app/database/` | Session factory, Base, migrations |
| `backend/app/schemas/` | Pydantic request/response models (referenced by routes) |
| `backend/app/services/` | Business logic layer (referenced by dependencies) |
| `requirements.txt` / `pyproject.toml` | Python dependencies not declared |
| DB seed script | Load `problem.json` → SQLite + FTS5 |
| Frontend UI | Still Vite boilerplate; zero BEE components |
| Zustand store | Not set up |
| React Router pages | Not set up |
| Graph visualization library | Not chosen/installed |
| Markdown renderer | Not installed |
| Tests | None |
| CI/CD, Docker | None |
| README for BEE | None |

### ⚠️ Inconsistencies to resolve

1. **Config paths:** `config.py` references `problems.json` but data file is `problem.json`.
2. ~~**ID type:**~~ **Resolved** — migrate all models to UUID.
3. **Difficulty labels:** Normalize to Easy / Medium / Hard everywhere.
4. **Field naming:** Seed `description` → `explanation` (summary) + generated `markdown_content` (article).
5. **Settings key:** Unify to `SEARCH_RESULT_LIMIT` across routes and config.
6. **Graph routes:** Update path params from `int` to `UUID`.

---

## 6. Implementation Phases

### Phase 0 — Foundation (Week 1)
*Goal: Backend runs, DB seeded, frontend shell matches design.*

- [ ] Fix config/data inconsistencies (paths, field names, settings keys)
- [ ] Migrate all models + routes from `int` IDs → **UUID**
- [ ] Add `requirements.txt` with pinned versions (+ `mangum` for Vercel)
- [ ] Create `database/session.py` + Alembic migrations
- [ ] Create all Pydantic schemas (`schemas/problems.py`, `search.py`, `graph.py`, etc.)
- [ ] Create service layer (`services/problem_service.py`, `search_service.py`, `graph_service.py`, etc.)
- [ ] Wire `main.py` — mount routers, CORS, security middleware, lifespan events
- [ ] Write seed script: `problem.json` → DB + markdown generation + FTS index
- [ ] Enforce **read-only API** — strip/disable all `POST`/`PUT`/`DELETE` public routes
- [ ] Verify all API endpoints via `/docs` (Swagger)
- [ ] **Migrate frontend to TypeScript** (`.jsx` → `.tsx`, add `tsconfig.json`)
- [ ] Frontend: app shell with navbar **"BEE"** + hero **"BEE is a backend engineering encyclopidia"**
- [ ] Import `token.css` globally; set up CSS Modules convention
- [ ] Add typed API client (`frontend/src/api/`) with axios + `VITE_API_URL` env
- [ ] Add `vercel.json` — frontend build + API rewrites to serverless handler

**Exit criteria:** `GET /api/v1/search?q=circuit` returns results; homepage renders with correct dark theme.

---

### Phase 1 — Search & Navigation (Week 2)
*Goal: Command palette works end-to-end.*

- [ ] `CommandPalette` component (glassmorphic overlay, `⌘K` shortcut)
- [ ] `SearchInput` with debounced input (300ms)
- [ ] `SuggestionList` — calls `GET /search/suggestions`
- [ ] `ResultFilter` — category, difficulty, tag chips
- [ ] Hybrid search: server FTS primary, Fuse.js client-side fallback
- [ ] LRU cache for recent queries (in-memory, Zustand)
- [ ] `StickySidebar` — category navigation (10 categories from seed data)
- [ ] `Breadcrumbs` component
- [ ] Homepage bento grid (featured problems, trending, category cards)
- [ ] Route: `/` (home), `/search` (results page)

**Exit criteria:** User can `⌘K` → type → see suggestions → click → land on problem page.

---

### Phase 2 — Content Display (Week 3)
*Goal: Problem detail pages are readable and beautiful.*

- [ ] `MarkdownRenderer` (react-markdown + syntax highlighting)
- [ ] `CodeBlock` with copy-to-clipboard + language label
- [ ] `DifficultyBadge` (Easy=green, Medium=amber, Hard=red)
- [ ] `TechnologyTag` chips
- [ ] `ComplexityMatrix` (time/space display)
- [ ] Problem detail layout from `bee_circuit_breaker_detail` mockup
- [ ] `StickySidebar` TOC — auto-generated from markdown headings
- [ ] `RelatedConcepts` horizontal card row
- [ ] Route: `/problems/:slug`
- [ ] Pre-fetch related concepts on hover (performance)

**Exit criteria:** `/problems/circuit-breaker-pattern` renders full article with working TOC and code copy.

---

### Phase 3 — Graph Explorer (Week 4)
*Goal: Interactive concept relationship visualization.*

- [ ] Install **React Flow** (`@xyflow/react`)
- [ ] `ConceptGraph` component with zoom, pan, node click
- [ ] `RelationshipLink` — typed edges (depends_on, alternative_to, extends)
- [ ] Graph filter panel (depth slider, relationship type, category)
- [ ] Node detail side panel on click
- [ ] Backend: wire `GET /graph/{id}` + neighbor/path endpoints
- [ ] Route: `/graph` (standalone explorer), `/graph/:id` (focused view)
- [ ] Code-split graph bundle (lazy load — heavy component)

**Exit criteria:** Clicking a node in the graph navigates to its problem page; filters work.

---

### Phase 4 — Polish & Extras (Week 5)
*Goal: Production-ready feel.*

- [ ] `ThemeToggle` (dark-only for MVP; light theme stub for future)
- [ ] Bookmarks (localStorage only — no server endpoint)
- [ ] Analytics tracking (background tasks already stubbed in routes)
- [ ] Trending concepts widget on homepage
- [ ] Recommendation engine (`GET /recommendations/{id}`)
- [ ] Virtualized search results list (react-window) for large result sets
- [ ] Mobile responsive: sidebar → bottom drawer, command palette full-screen
- [ ] Error boundaries + loading skeletons
- [ ] SEO meta tags per problem page

**Exit criteria:** App feels polished; Lighthouse performance > 85.

---

### Phase 5 — Vercel Deployment & Hardening (Week 6+)
*Goal: Live on Vercel with strict public-read-only security.*

- [ ] Provision **Vercel Postgres** (Neon) for production DB
- [ ] Deploy FastAPI via **Mangum** serverless handler (`api/index.py`)
- [ ] Deploy Vite frontend as Vercel static build
- [ ] Configure `vercel.json` rewrites: `/api/*` → serverless, `/*` → SPA
- [ ] Set env vars: `DATABASE_URL`, `ALLOWED_ORIGINS`, `ENVIRONMENT=production`
- [ ] Security headers middleware (see §13)
- [ ] Rate limiting on search/analytics endpoints
- [ ] GitHub Actions CI (lint, typecheck, test, build)
- [ ] API integration tests (pytest + httpx)
- [ ] Frontend E2E tests (Playwright — search flow, detail page)
- [ ] Lighthouse audit on Vercel preview deploys

---

## 7. Target File Structure

```
Backend-Problems/
├── plan.md                          ← this file
├── README.md
├── docker-compose.yml               (Phase 5)
│
├── frontend/
│   ├── src/
│   │   ├── api/                     # axios client + endpoint functions
│   │   ├── components/
│   │   │   ├── search/              # CommandPalette, SearchInput, SuggestionList, ResultFilter
│   │   │   ├── display/             # MarkdownRenderer, CodeBlock, DifficultyBadge
│   │   │   ├── graph/               # ConceptGraph, RelationshipLink, GraphFilters
│   │   │   ├── navigation/          # Header, StickySidebar, Breadcrumbs, ThemeToggle
│   │   │   └── layout/              # AppShell, PageContainer
│   │   ├── pages/                   # Home, Search, ProblemDetail, GraphExplorer
│   │   ├── stores/                  # Zustand: searchStore, uiStore, bookmarkStore
│   │   ├── hooks/                   # useSearch, useDebounce, useCommandPalette
│   │   ├── styles/
│   │   │   ├── token.css            # ✅ exists
│   │   │   └── global.css
│   │   ├── utils/                   # slugify, formatComplexity, cache
│   │   ├── types/                   # shared TS interfaces (Problem, SearchResult, GraphNode)
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── tsconfig.json
│   ├── vercel.json
│   └── package.json
│
├── api/                             # Vercel serverless entry
│   └── index.py                     # Mangum handler wrapping FastAPI app
│
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py                  # FastAPI entry
│       ├── database/
│       │   ├── session.py
│       │   └── seed.py
│       ├── models/                  # ✅ exists
│       ├── schemas/                 # Pydantic models
│       ├── services/                # Business logic
│       ├── repositories/              # ✅ exists
│       ├── routes/                  # ✅ exists
│       ├── search_engine/           # ✅ exists
│       ├── core/                    # ✅ exists
│       └── data/
│           └── problem.json         # ✅ 150 entries
│
└── design/                          # Copy Stitch assets here for reference
    ├── kinetic_syntax/DESIGN.md
    ├── mockups/
    │   ├── homepage.html
    │   ├── problem_detail.html
    │   └── graph_explorer.html
    └── bee_technical_spec.md
```

---

## 8. API Surface (MVP)

| Method | Endpoint | Purpose | Auth |
|---|---|---|---|
| `GET` | `/api/v1/problems/{slug}` | Full problem detail (markdown article) | Public |
| `GET` | `/api/v1/search?q=&category=&difficulty=&tags=` | Full-text search (DB-backed) | Public |
| `GET` | `/api/v1/search/suggestions?q=` | Typeahead suggestions | Public |
| `GET` | `/api/v1/graph/{uuid}` | Relationship graph | Public |
| `GET` | `/api/v1/graph/{uuid}/neighbors` | 1-hop neighbors | Public |
| `GET` | `/api/v1/graph/{uuid}/path?target=` | Shortest path | Public |
| `GET` | `/api/v1/graph/cluster/{category}` | Category cluster | Public |
| `GET` | `/api/v1/recommendations/{uuid}` | Related concepts | Public |
| `GET` | `/api/v1/analytics/trending` | Trending concepts | Public |

> **No write endpoints.** Bookmarks live in `localStorage` on the client. Analytics writes happen server-side only (background tasks), never exposed as public `POST`.

---

## 9. Design Implementation Notes

### Translating Stitch HTML → React

The mockups use Tailwind CDN. Our approach:

1. **Tokens** — `token.css` CSS variables (already started) map 1:1 to Kinetic Syntax palette.
2. **Components** — Each mockup section becomes a CSS Module component using token variables.
3. **No Tailwind in production** — Avoid CDN dependency; use CSS Modules for tree-shaking and consistency.
4. **Material Symbols** — Load via Google Fonts link (same as mockups).
5. **Glassmorphism** — `.glass-panel` utility class (already defined in mockups).

### Key UI patterns from mockups

- **Homepage:** 12-column bento grid, left sidebar (280px), fixed header (56px), command palette centered overlay.
- **Detail page:** 3-column layout — TOC sidebar | content | metadata panel. Active TOC line indicator.
- **Graph explorer:** Full-width canvas, floating filter toolbar, right-side node detail drawer.

---

## 10. Locked Decisions

| # | Decision | Your choice |
|---|---|---|
| 1 | **MVP scope** | All 3 pages — Home, Problem Detail, Graph Explorer |
| 2 | **Authentication** | **No auth system.** Strict security on a **public read-only** API |
| 3 | **Content delivery** | **Dynamic DB responses** — never serve static `problem.json` to clients |
| 4 | **ID strategy** | **UUID** primary keys across all entities |
| 5 | **Graph library** | **React Flow** (`@xyflow/react`) |
| 6 | **Frontend language** | **TypeScript** (migrate from JSX) |
| 7 | **Deployment** | **Vercel** — static frontend + serverless FastAPI + Vercel Postgres |
| 8 | **Relationship data** | Auto-generate edges from shared tags + category proximity |
| 9 | **Article format** | **Full markdown articles** generated from seed descriptions |
| 10 | **Branding** | Navbar: **"BEE"** · Hero: **"BEE is a backend engineering encyclopidia"** |

---

## 11. Security Model (No Auth, Strict Read-Only)

Even without user accounts, the platform enforces defense-in-depth:

| Layer | Measure |
|---|---|
| **API surface** | `GET`-only public routes; no `POST`/`PUT`/`DELETE` exposed |
| **CORS** | Locked to Vercel production + preview domains |
| **Rate limiting** | 60 req/min on search; 120 req/min on analytics reads |
| **Input validation** | Pydantic schemas on all query params; max query length 128 chars |
| **SQL safety** | SQLAlchemy ORM + parameterized FTS queries only |
| **Headers** | `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin`, CSP restricting script sources |
| **Error handling** | Generic 404/500 messages — no stack traces in production |
| **Secrets** | `DATABASE_URL` and env vars in Vercel dashboard only; never in repo |
| **Dependencies** | Pinned versions; `pip audit` + `npm audit` in CI |
| **Analytics** | Server-side background writes only; no client-submitted analytics payloads |

---

## 12. Vercel Deployment Architecture

```
┌─────────────────────────────────────────────────┐
│                   Vercel                         │
│                                                  │
│  ┌──────────────┐    rewrite /api/*              │
│  │  Vite Build  │──────────────────┐             │
│  │  (React TS)  │                  ▼             │
│  │  Static SPA  │         ┌──────────────┐      │
│  └──────────────┘         │  Serverless   │      │
│                           │  FastAPI      │      │
│                           │  (Mangum)     │      │
│                           └──────┬───────┘      │
└──────────────────────────────────┼──────────────┘
                                   │
                          ┌────────▼────────┐
                          │  Vercel Postgres │
                          │  (Neon)          │
                          └─────────────────┘
```

**Key files:**

- `vercel.json` — build command, output dir, API rewrites, security headers
- `api/index.py` — Mangum handler: `handler = Mangum(app)`
- `frontend/.env.production` — `VITE_API_URL=/api/v1` (same-origin)

**Local dev:** SQLite + `uvicorn` on `:8000`; Vite dev server on `:5173` with proxy to API.

---

## 13. Immediate Next Steps

1. **Copy Stitch design assets** into `design/` folder for permanent reference.
2. **Start Phase 0** — UUID migration, backend wiring, TypeScript setup.
3. **Build app shell** — navbar "BEE" + hero tagline + sidebar from homepage mockup.
4. **Iterate page by page** — Home → Search → Detail → Graph.
5. **Configure Vercel** — project link, Postgres provisioning, env vars.

---

## 14. Success Metrics

| Metric | Target |
|---|---|
| Search latency (server) | < 50ms for FTS5 queries |
| Search latency (client Fuse.js) | < 10ms for cached index |
| Time to interactive (homepage) | < 2s on 3G |
| Problems indexed | 150/150 |
| API test coverage | > 80% of endpoints |
| Lighthouse performance | > 85 |
| Mobile usable | Sidebar collapses, command palette works |

---

*This plan will be updated as phases complete and decisions are made.*
