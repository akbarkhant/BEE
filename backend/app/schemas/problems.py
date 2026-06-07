from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ComplexitySchema(BaseModel):
    time: Optional[str] = None
    space: Optional[str] = None


class ProblemMinimalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    title: str
    category: str
    algorithm: Optional[str] = None
    difficulty: str
    explanation: str
    tags: list[str] = []

    @field_validator("tags", mode="before")
    @classmethod
    def extract_tag_names(cls, v: Any) -> list[str]:
        # If SQLAlchemy returns a list of Tag objects, extract their string names
        if isinstance(v, list) and v and not isinstance(v[0], str):
            return [getattr(tag, "name", getattr(tag, "tag_name", str(tag))) for tag in v]
        return v or []


class ProblemDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    title: str
    category: str
    algorithm: Optional[str] = None
    difficulty: str
    explanation: str
    markdown_content: str
    technologies: list[str] = Field(default_factory=list)
    complexity: Optional[ComplexitySchema] = None
    tags: list[str] = []
    created_at: datetime

    @field_validator("tags", mode="before")
    @classmethod
    def extract_tag_names(cls, v: Any) -> list[str]:
        if isinstance(v, list) and v and not isinstance(v[0], str):
            return [getattr(tag, "name", getattr(tag, "tag_name", str(tag))) for tag in v]
        return v or []


class ProblemListResponse(BaseModel):
    items: list[ProblemMinimalResponse]
    total: int
    page: int
    page_size: int