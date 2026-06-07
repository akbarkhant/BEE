# Backend Engineering Encyclopedia (BEE) Technical Specification

## Core Architecture
- **Frontend**: React.js + Vite, Zustand (State), Framer Motion (Animations), CSS Modules.
- **Backend**: FastAPI (Python), SQLAlchemy ORM, Pydantic (Validation).
- **Search Engine**: Hybrid approach (Fuse.js for client-side fuzzy matching, SQLite FTS5 / PostgreSQL for server-side full-text search).
- **Database**: PostgreSQL (Production) / SQLite (Development).

## Database Schema
### Problem
- `id`: UUID
- `title`: String
- `category`: Enum (Performance, Scalability, etc.)
- `algorithm`: String
- `explanation`: Markdown Text
- `tags`: List[String]
- `difficulty`: Enum (Easy, Medium, Hard)
- `technologies`: List[String]
- `related_problems`: List[UUID]
- `complexity`: JSON (Time, Space)
- `created_at`: DateTime

## Component Architecture
- **Search**: `CommandPalette`, `SearchInput`, `SuggestionList`, `ResultFilter`.
- **Display**: `MarkdownRenderer`, `CodeBlock` (with copy-to-clipboard), `ArchitectureDiagram`.
- **Graph**: `ConceptGraph` (D3.js/React Flow), `RelationshipLink`.
- **Navigation**: `StickySidebar`, `Breadcrumbs`, `ThemeToggle`.

## Performance Strategy
- **Search**: LRU Caching for recent queries, debounced input, pre-fetching related concepts.
- **Rendering**: Virtualized lists for large result sets, code-splitting for heavy graph components.
- **Backend**: Async database drivers, indexed search columns, Pydantic serialization.
