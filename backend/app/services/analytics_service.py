from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.analytics_repo import AnalyticsRepository
from app.schemas.analytics import TrendingConceptResponse


class AnalyticsService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = AnalyticsRepository(db)

    async def track_concept_view(self, problem_id: UUID, slug: str) -> None:
        await self.repo.log_event(
            "problem_view",
            target_problem_id=problem_id,
            metadata_json=f'{{"slug":"{slug}"}}',
        )

    async def track_search_query(
        self,
        query: str,
        filters: dict,
        result_count: int,
    ) -> None:
        await self.repo.log_event(
            "search",
            search_query=query,
            metadata_json=str({"filters": filters, "result_count": result_count}),
        )

    async def track_graph_traversal(
        self,
        problem_id: UUID,
        depth: int,
        node_count: int,
    ) -> None:
        await self.repo.log_event(
            "graph_traversal",
            target_problem_id=problem_id,
            metadata_json=str({"depth": depth, "node_count": node_count}),
        )

    async def calculate_trending(
        self,
        *,
        time_window_hours: int = 24,
        limit: int = 10,
    ) -> list[TrendingConceptResponse]:
        rows = await self.repo.get_trending(hours=time_window_hours, limit=limit)
        return [TrendingConceptResponse(**row) for row in rows]
