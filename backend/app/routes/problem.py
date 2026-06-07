from fastapi import APIRouter, BackgroundTasks, HTTPException, Path, Query, status
from typing import Annotated, Optional

from app.core.dependencies import AnalyticsServiceDep, ProblemServiceDep, SettingsDep
from app.core.logging import get_logger
from app.schemas.problems import ProblemDetailResponse, ProblemListResponse

router = APIRouter(prefix="/problems", tags=["Problems"])
logger = get_logger(__name__)


@router.get("", response_model=ProblemListResponse, summary="List encyclopedia entries")
async def list_problems(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, alias="pageSize")] = 20,
    category: Annotated[Optional[str], Query()] = None,
    difficulty: Annotated[Optional[str], Query()] = None,
    problem_svc: ProblemServiceDep = None,
) -> ProblemListResponse:
    return await problem_svc.list_problems(
        page=page,
        page_size=page_size,
        category=category,
        difficulty=difficulty,
    )


@router.get(
    "/{slug}",
    response_model=ProblemDetailResponse,
    summary="Retrieve markdown article by slug",
)
async def get_problem(
    slug: Annotated[str, Path(min_length=2, max_length=200, pattern=r"^[a-z0-9-]+$")],
    background_tasks: BackgroundTasks,
    problem_svc: ProblemServiceDep = None,
    analytics_svc: AnalyticsServiceDep = None,
    settings: SettingsDep = None,
) -> ProblemDetailResponse:
    problem = await problem_svc.fetch_by_slug(slug=slug)
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No article found for slug '{slug}'.",
        )
    if settings.ANALYTICS_ENABLED and analytics_svc:
        background_tasks.add_task(
            analytics_svc.track_concept_view,
            problem_id=problem.id,
            slug=slug,
        )
    return problem
