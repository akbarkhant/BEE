from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import Annotated, List

from app.core.dependencies import RecommendationServiceDep, SettingsDep
from app.core.logging import get_logger
from app.schemas.problems import ProblemMinimalResponse

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])
logger = get_logger(__name__)

ProblemId = Annotated[UUID, Path(description="Context problem UUID")]


@router.get("/{problem_id}", response_model=List[ProblemMinimalResponse])
async def get_recommendations(
    problem_id: ProblemId,
    limit: Annotated[int, Query(ge=1, le=20)] = 6,
    recommendation_svc: RecommendationServiceDep = None,
    settings: SettingsDep = None,
) -> List[ProblemMinimalResponse]:
    recommendations = await recommendation_svc.generate_recommendations(
        problem_id=problem_id,
        limit=limit,
        min_score=settings.RECOMMENDATION_MIN_SCORE,
    )
    if recommendations is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem {problem_id} not found.",
        )
    return recommendations
