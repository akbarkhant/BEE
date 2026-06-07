from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class GraphNode(BaseModel):
    id: UUID
    slug: str
    title: str
    category: str
    difficulty: str


class GraphEdge(BaseModel):
    source_id: UUID
    target_id: UUID
    relationship_type: str
    strength: float


class GraphResponse(BaseModel):
    root_id: UUID
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class NeighborItem(BaseModel):
    id: UUID
    slug: str
    title: str
    relationship_type: str
    strength: float
    direction: str


class NeighborResponse(BaseModel):
    problem_id: UUID
    neighbors: list[NeighborItem]


class PathResponse(BaseModel):
    source_id: UUID
    target_id: UUID
    path: list[UUID] = Field(default_factory=list)
    found: bool = False


class ClusterResponse(BaseModel):
    category: str
    nodes: list[GraphNode]
    edges: list[GraphEdge]
