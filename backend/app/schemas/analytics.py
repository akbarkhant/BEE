from uuid import UUID

from pydantic import BaseModel


class TrendingConceptResponse(BaseModel):
    problem_id: UUID
    slug: str
    title: str
    category: str
    view_count: int
