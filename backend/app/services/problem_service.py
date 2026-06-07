from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.problem_repo import ProblemRepository
from app.schemas.problems import (
    ComplexitySchema,
    ProblemDetailResponse,
    ProblemListResponse,
    ProblemMinimalResponse,
)


def _tags(problem) -> list[str]:
    return [t.name for t in problem.tags]


def _to_minimal(problem) -> ProblemMinimalResponse:
    return ProblemMinimalResponse(
        id=problem.id,
        slug=problem.slug,
        title=problem.title,
        category=problem.category,
        algorithm=problem.algorithm,
        difficulty=problem.difficulty,
        explanation=problem.explanation,
        tags=_tags(problem),
    )


def _to_detail(problem) -> ProblemDetailResponse:
    complexity = None
    if problem.complexity:
        complexity = ComplexitySchema(**problem.complexity)
    return ProblemDetailResponse(
        id=problem.id,
        slug=problem.slug,
        title=problem.title,
        category=problem.category,
        algorithm=problem.algorithm,
        difficulty=problem.difficulty,
        explanation=problem.explanation,
        markdown_content=problem.markdown_content,
        technologies=problem.technologies or [],
        complexity=complexity,
        tags=_tags(problem),
        created_at=problem.created_at,
    )


class ProblemService:
    def __init__(self, db: AsyncSession) -> None:
        self.repo = ProblemRepository(db)

    async def fetch_by_slug(self, slug: str) -> Optional[ProblemDetailResponse]:
        problem = await self.repo.get_by_slug(slug)
        if not problem:
            return None
        return _to_detail(problem)

    async def fetch_by_id(self, problem_id: UUID) -> Optional[ProblemDetailResponse]:
        problem = await self.repo.get_by_id(problem_id)
        if not problem:
            return None
        return _to_detail(problem)

    async def list_problems(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
    ) -> ProblemListResponse:
        offset = (page - 1) * page_size
        problems, total = await self.repo.list_problems(
            limit=page_size,
            offset=offset,
            category=category,
            difficulty=difficulty,
        )
        return ProblemListResponse(
            items=[_to_minimal(p) for p in problems],
            total=total,
            page=page,
            page_size=page_size,
        )
