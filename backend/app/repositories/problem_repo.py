from __future__ import annotations

import re
from typing import Optional
from uuid import UUID

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.problem import Problem
from app.models.tag import Tag


def slugify(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug[:200]


class ProblemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(Problem))
        return result.scalar_one()

    async def get_by_id(self, problem_id: UUID) -> Optional[Problem]:
        result = await self.session.execute(
            select(Problem)
            .where(Problem.id == problem_id)
            .options(selectinload(Problem.tags))
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Optional[Problem]:
        result = await self.session.execute(
            select(Problem)
            .where(Problem.slug == slug)
            .options(selectinload(Problem.tags))
        )
        return result.scalar_one_or_none()

    async def list_problems(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> tuple[list[Problem], int]:
        query = select(Problem).options(selectinload(Problem.tags))
        count_query = select(func.count()).select_from(Problem)
        filters = []
        if category:
            filters.append(Problem.category == category)
        if difficulty:
            filters.append(Problem.difficulty == difficulty)
        if filters:
            query = query.where(and_(*filters))
            count_query = count_query.where(and_(*filters))
        total = (await self.session.execute(count_query)).scalar_one()
        result = await self.session.execute(
            query.order_by(Problem.title).offset(offset).limit(limit)
        )
        return list(result.scalars().all()), total

    async def search(
        self,
        *,
        query: str,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        tags: Optional[list[str]] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Problem]:
        stmt = select(Problem).options(selectinload(Problem.tags))
        conditions = []
        if query.strip():
            q = f"%{query.strip()}%"
            conditions.append(
                or_(
                    Problem.title.ilike(q),
                    Problem.algorithm.ilike(q),
                    Problem.explanation.ilike(q),
                    Problem.category.ilike(q),
                )
            )
        if category:
            conditions.append(Problem.category == category)
        if difficulty:
            conditions.append(Problem.difficulty == difficulty)
        if conditions:
            stmt = stmt.where(and_(*conditions))
        stmt = stmt.order_by(Problem.title).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        problems = list(result.scalars().all())
        if tags:
            tag_set = {t.lower() for t in tags}
            problems = [
                p
                for p in problems
                if tag_set.intersection({t.name.lower() for t in p.tags})
            ]
        return problems

    async def get_suggestions(self, prefix: str, limit: int = 8) -> list[Problem]:
        q = f"{prefix.strip()}%"
        result = await self.session.execute(
            select(Problem)
            .where(Problem.title.ilike(q))
            .order_by(Problem.title)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_ids(self, ids: list[UUID]) -> list[Problem]:
        if not ids:
            return []
        result = await self.session.execute(
            select(Problem)
            .where(Problem.id.in_(ids))
            .options(selectinload(Problem.tags))
        )
        return list(result.scalars().all())

    async def get_by_category(self, category: str) -> list[Problem]:
        result = await self.session.execute(
            select(Problem)
            .where(Problem.category == category)
            .options(selectinload(Problem.tags))
        )
        return list(result.scalars().all())

    async def get_or_create_tag(self, name: str) -> Tag:
        result = await self.session.execute(select(Tag).where(Tag.name == name))
        tag = result.scalar_one_or_none()
        if tag:
            return tag
        tag = Tag(name=name)
        self.session.add(tag)
        await self.session.flush()
        return tag
