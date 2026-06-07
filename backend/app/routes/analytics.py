from fastapi import APIRouter
from typing import List

from app.core.dependencies import AnalyticsServiceDep, SettingsDep
from app.core.logging import get_logger
from app.schemas.analytics import TrendingConceptResponse

router = APIRouter(tags=["Analytics"])
logger = get_logger(__name__)


@router.get("/trending", response_model=List[TrendingConceptResponse])
async def get_trending_concepts(
    analytics_svc: AnalyticsServiceDep = None,
    settings: SettingsDep = None,
) -> List[TrendingConceptResponse]:
    return await analytics_svc.calculate_trending(
        time_window_hours=settings.TRENDING_WINDOW_HOURS,
        limit=settings.TRENDING_LIMIT,
    )
