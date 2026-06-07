from collections import Counter
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.analytics import Analytics
from app.models.problem import Problem


class AnalyticsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def log_event(
        self,
        event_type: str,
        *,
        search_query: Optional[str] = None,
        target_problem_id: Optional[UUID] = None,
        metadata_json: Optional[str] = None,
    ) -> None:
        event = Analytics(
            event_type=event_type,
            search_query=search_query,
            target_problem_id=target_problem_id,
            metadata_json=metadata_json,
        )
        self.session.add(event)
        await self.session.flush()

    async def get_trending(self, *, hours: int = 24, limit: int = 10) -> list[dict]:
        since = datetime.utcnow() - timedelta(hours=hours)
        result = await self.session.execute(
            select(Analytics.target_problem_id, func.count(Analytics.id).label("cnt"))
            .where(
                Analytics.event_type == "problem_view",
                Analytics.target_problem_id.isnot(None),
                Analytics.timestamp >= since,
            )
            .group_by(Analytics.target_problem_id)
            .order_by(func.count(Analytics.id).desc())
            .limit(limit)
        )
        rows = result.all()
        if not rows:
            result = await self.session.execute(
                select(Problem).order_by(Problem.created_at.desc()).limit(limit)
            )
            return [
                {
                    "problem_id": p.id,
                    "slug": p.slug,
                    "title": p.title,
                    "category": p.category,
                    "view_count": 0,
                }
                for p in result.scalars().all()
            ]
        problem_ids = [row[0] for row in rows]
        problems_result = await self.session.execute(
            select(Problem).where(Problem.id.in_(problem_ids))
        )
        by_id = {p.id: p for p in problems_result.scalars().all()}
        trending = []
        for pid, cnt in rows:
            p = by_id.get(pid)
            if p:
                trending.append(
                    {
                        "problem_id": p.id,
                        "slug": p.slug,
                        "title": p.title,
                        "category": p.category,
                        "view_count": cnt,
                    }
                )
        return trending
