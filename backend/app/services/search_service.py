from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.problem_repo import ProblemRepository
from app.schemas.search import SearchResponse, SuggestionResponse


class SearchService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = ProblemRepository(db)

    async def execute_search(
        self,
        *,
        query: str,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        tags: Optional[list[str]] = None,
        max_results: int = 20,
    ) -> list[SearchResponse]:
        problems = await self.repo.search(
            query=query,
            category=category,
            difficulty=difficulty,
            tags=tags,
            limit=max_results,
        )
        results = []
        q_lower = query.lower()
        for p in problems:
            score = 0.0
            if q_lower in p.title.lower():
                score += 10
            if p.algorithm and q_lower in p.algorithm.lower():
                score += 8
            if q_lower in p.explanation.lower():
                score += 3
            results.append(
                SearchResponse(
                    id=p.id,
                    slug=p.slug,
                    title=p.title,
                    category=p.category,
                    algorithm=p.algorithm,
                    difficulty=p.difficulty,
                    explanation=p.explanation,
                    tags=[t.name for t in p.tags],
                    score=score,
                )
            )
        results.sort(key=lambda r: r.score, reverse=True)
        return results

    async def get_instant_suggestions(self, prefix: str) -> list[SuggestionResponse]:
        problems = await self.repo.get_suggestions(prefix, limit=8)
        return [
            SuggestionResponse(slug=p.slug, title=p.title, category=p.category)
            for p in problems
        ]
