from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SearchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    title: str
    category: str
    algorithm: Optional[str] = None
    difficulty: str
    explanation: str
    tags: list[str] = Field(default_factory=list)
    score: float = 0.0


class SuggestionResponse(BaseModel):
    slug: str
    title: str
    category: str
