from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tag import Tag
from app.models.problem import Problem


class TagRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Tag]:
        result = await self.session.execute(select(Tag).order_by(Tag.name))
        return list(result.scalars().all())

    async def get_popular_tags(self, limit: int = 20) -> list[dict]:
        """Return tags with occurrence counts aggregated from problems JSON."""
        result = await self.session.execute(select(Problem.tags))
        tag_counts: dict[str, int] = {}
        for row in result.scalars().all():
            for tag in (row or []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"name": t, "count": c} for t, c in sorted_tags[:limit]]