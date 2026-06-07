from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.events import lifespan
from app.middleware.security import SecurityHeadersMiddleware
from app.routes import analytics, graph, problem, recommendations, search

settings = get_settings()

app = FastAPI(
    title="BEE API",
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=settings.openapi_url,
)

# 1. Security & Context Wrappers
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# 2. Scope-Isolated API Routes
# Appends distinct resource names right after your base API prefix (e.g., /api/v1/problems)
app.include_router(problem.router, prefix=f"{settings.API_PREFIX}/problems", tags=["Problems"])
app.include_router(search.router, prefix=f"{settings.API_PREFIX}/search", tags=["Search"])
app.include_router(graph.router, prefix=f"{settings.API_PREFIX}/graph", tags=["Graph Explorer"])
app.include_router(recommendations.router, prefix=f"{settings.API_PREFIX}/recommendations", tags=["Recommendations"])
app.include_router(analytics.router, prefix=f"{settings.API_PREFIX}/analytics", tags=["Analytics"])


# 3. Diagnostics
@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok", "app": "BEE", "version": settings.APP_VERSION}