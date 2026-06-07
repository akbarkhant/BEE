from typing import Optional
from sqlalchemy import select, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.bookmark import Bookmark
from app.models.schemas import BookmarkCreate


class BookmarkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_session(
        self, session_id: str, limit: int = 50, offset: int = 0
    ) -> tuple[list[Bookmark], int]:
        count_result = await self.session.execute(
            select(func.count()).select_from(Bookmark).where(
                Bookmark.session_id == session_id
            )
        )
        total = count_result.scalar_one()

        result = await self.session.execute(
            select(Bookmark)
            .where(Bookmark.session_id == session_id)
            .options(selectinload(Bookmark.problem))
            .order_by(Bookmark.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all()), total

    async def get_by_problem_and_session(
        self, problem_id: str, session_id: str
    ) -> Optional[Bookmark]:
        result = await self.session.execute(
            select(Bookmark).where(
                and_(
                    Bookmark.problem_id == problem_id,
                    Bookmark.session_id == session_id,
                )
            )
        )
        return result.scalar_one_or_none()

    async def create(self, data: BookmarkCreate) -> Bookmark:
        bookmark = Bookmark(
            problem_id=data.problem_id,
            session_id=data.session_id,
            note=data.note,
        )
        self.session.add(bookmark)
        await self.session.flush()
        return bookmark

    async def delete(self, bookmark: Bookmark) -> None:
        await self.session.delete(bookmark)
        await self.session.flush()

    async def get_most_bookmarked_problem_ids(self, limit: int = 5) -> list[str]:
        result = await self.session.execute(
            select(Bookmark.problem_id, func.count(Bookmark.id).label("cnt"))
            .group_by(Bookmark.problem_id)
            .order_by(func.count(Bookmark.id).desc())
            .limit(limit)
        )
        return [row[0] for row in result.all()]