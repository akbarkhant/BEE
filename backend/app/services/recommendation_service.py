from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.problem_repo import ProblemRepository
from app.repositories.relationship_repo import RelationshipRepository
from app.schemas.problems import ProblemMinimalResponse


class RecommendationService:
    def __init__(self, db: AsyncSession) -> None:
        self.problems = ProblemRepository(db)
        self.relationships = RelationshipRepository(db)

    async def generate_recommendations(
        self,
        problem_id: UUID,
        *,
        limit: int = 6,
        min_score: float = 0.2,
    ) -> Optional[list[ProblemMinimalResponse]]:
        problem = await self.problems.get_by_id(problem_id)
        if not problem:
            return None

        scores: dict[UUID, float] = {}
        rels = await self.relationships.get_for_problem(problem_id)
        for rel in rels:
            other_id = rel.target_id if rel.source_id == problem_id else rel.source_id
            scores[other_id] = scores.get(other_id, 0) + rel.strength * 0.6

        tag_names = {t.name for t in problem.tags}
        same_category = await self.problems.get_by_category(problem.category)
        for candidate in same_category:
            if candidate.id == problem_id:
                continue
            shared = len(tag_names.intersection({t.name for t in candidate.tags}))
            if shared:
                scores[candidate.id] = scores.get(candidate.id, 0) + shared * 0.2

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        ranked = [(pid, s) for pid, s in ranked if s >= min_score][:limit]
        if not ranked:
            ranked = [(p.id, 0.1) for p in same_category if p.id != problem_id][:limit]

        ids = [pid for pid, _ in ranked]
        items = await self.problems.get_by_ids(ids)
        by_id = {p.id: p for p in items}
        return [
            ProblemMinimalResponse(
                id=p.id,
                slug=p.slug,
                title=p.title,
                category=p.category,
                algorithm=p.algorithm,
                difficulty=p.difficulty,
                explanation=p.explanation,
                tags=[t.name for t in p.tags],
            )
            for pid, _ in ranked
            if (p := by_id.get(pid))
        ]
