from uuid import UUID

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.relationship import Relationship


class RelationshipRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Relationship]:
        result = await self.session.execute(select(Relationship))
        return list(result.scalars().all())

    async def get_for_problem(self, problem_id: UUID) -> list[Relationship]:
        result = await self.session.execute(
            select(Relationship)
            .where(
                or_(
                    Relationship.source_id == problem_id,
                    Relationship.target_id == problem_id,
                )
            )
            .options(
                selectinload(Relationship.source_node),
                selectinload(Relationship.target_node),
            )
        )
        return list(result.scalars().all())

    async def get_edges_for_category(self, category: str) -> list[Relationship]:
        result = await self.session.execute(
            select(Relationship).options(
                selectinload(Relationship.source_node),
                selectinload(Relationship.target_node),
            )
        )
        edges = list(result.scalars().all())
        return [
            e
            for e in edges
            if e.source_node.category == category and e.target_node.category == category
        ]

    async def create(
        self,
        source_id: UUID,
        target_id: UUID,
        relationship_type: str = "related_to",
        strength: float = 1.0,
    ) -> Relationship:
        rel = Relationship(
            source_id=source_id,
            target_id=target_id,
            relationship_type=relationship_type,
            strength=strength,
        )
        self.session.add(rel)
        await self.session.flush()
        return rel
