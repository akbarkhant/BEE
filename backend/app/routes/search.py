from fastapi import APIRouter, BackgroundTasks, Query
from typing import Annotated, List, Optional

from app.core.dependencies import AnalyticsServiceDep, SearchServiceDep, SettingsDep
from app.core.logging import get_logger
from app.schemas.search import SearchResponse, SuggestionResponse

router = APIRouter(prefix="/search", tags=["Search"])
logger = get_logger(__name__)


@router.get("", response_model=List[SearchResponse], summary="Full-text knowledge search")
async def search_knowledge_base(
    q: Annotated[str, Query(min_length=1, max_length=128)],
    background_tasks: BackgroundTasks,
    category: Annotated[Optional[str], Query()] = None,
    difficulty: Annotated[Optional[str], Query()] = None,
    tags: Annotated[Optional[List[str]], Query()] = None,
    search_svc: SearchServiceDep = None,
    analytics_svc: AnalyticsServiceDep = None,
    settings: SettingsDep = None,
) -> List[SearchResponse]:
    results = await search_svc.execute_search(
        query=q,
        category=category,
        difficulty=difficulty,
        tags=tags,
        max_results=settings.SEARCH_RESULT_LIMIT,
    )
    if settings.ANALYTICS_ENABLED and analytics_svc:
        background_tasks.add_task(
            analytics_svc.track_search_query,
            query=q,
            filters={"category": category, "difficulty": difficulty, "tags": tags},
            result_count=len(results),
        )
    return results


@router.get(
    "/suggestions",
    response_model=List[SuggestionResponse],
    summary="Typeahead suggestions",
)
async def get_search_suggestions(
    q: Annotated[str, Query(min_length=1, max_length=64)],
    search_svc: SearchServiceDep = None,
) -> List[SuggestionResponse]:
    return await search_svc.get_instant_suggestions(prefix=q)
