from collections import deque
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import RelationshipType
from app.repositories.problem_repo import ProblemRepository
from app.repositories.relationship_repo import RelationshipRepository
from app.schemas.graph import (
    ClusterResponse,
    GraphEdge,
    GraphNode,
    GraphResponse,
    NeighborItem,
    NeighborResponse,
    PathResponse,
)


def _node(problem) -> GraphNode:
    return GraphNode(
        id=problem.id,
        slug=problem.slug,
        title=problem.title,
        category=problem.category,
        difficulty=problem.difficulty,
    )


class GraphService:
    def __init__(self, db: AsyncSession) -> None:
        self.problems = ProblemRepository(db)
        self.relationships = RelationshipRepository(db)

    async def build_graph(
        self,
        problem_id: UUID,
        *,
        depth: int = 2,
        relationship_type: Optional[RelationshipType] = None,
        min_strength: float = 0.3,
        max_nodes: int = 50,
    ) -> GraphResponse:
        root = await self.problems.get_by_id(problem_id)
        if not root:
            return GraphResponse(root_id=problem_id, nodes=[], edges=[])

        nodes: dict[UUID, GraphNode] = {root.id: _node(root)}
        edges: list[GraphEdge] = []
        seen_edges: set[tuple] = set()
        frontier = [problem_id]

        for _ in range(depth):
            next_frontier = []
            for pid in frontier:
                rels = await self.relationships.get_for_problem(pid)
                for rel in rels:
                    if rel.strength < min_strength:
                        continue
                    if relationship_type and rel.relationship_type != relationship_type.value:
                        continue
                    other = rel.target_node if rel.source_id == pid else rel.source_node
                    if other.id not in nodes and len(nodes) < max_nodes:
                        nodes[other.id] = _node(other)
                        next_frontier.append(other.id)
                    key = (rel.source_id, rel.target_id, rel.relationship_type)
                    if key not in seen_edges:
                        seen_edges.add(key)
                        edges.append(
                            GraphEdge(
                                source_id=rel.source_id,
                                target_id=rel.target_id,
                                relationship_type=rel.relationship_type,
                                strength=rel.strength,
                            )
                        )
            frontier = next_frontier
            if len(nodes) >= max_nodes:
                break

        return GraphResponse(root_id=problem_id, nodes=list(nodes.values()), edges=edges)

    async def get_neighbors(
        self,
        problem_id: UUID,
        relationship_type: Optional[RelationshipType] = None,
    ) -> list[NeighborItem]:
        rels = await self.relationships.get_for_problem(problem_id)
        neighbors = []
        for rel in rels:
            if relationship_type and rel.relationship_type != relationship_type.value:
                continue
            if rel.source_id == problem_id:
                target = rel.target_node
                direction = "outgoing"
            else:
                target = rel.source_node
                direction = "incoming"
            neighbors.append(
                NeighborItem(
                    id=target.id,
                    slug=target.slug,
                    title=target.title,
                    relationship_type=rel.relationship_type,
                    strength=rel.strength,
                    direction=direction,
                )
            )
        return neighbors

    async def shortest_path(self, source_id: UUID, target_id: UUID) -> list[UUID]:
        if source_id == target_id:
            return [source_id]
        adj: dict[UUID, list[UUID]] = {}
        all_rels = await self.relationships.get_all()
        for rel in all_rels:
            adj.setdefault(rel.source_id, []).append(rel.target_id)
            adj.setdefault(rel.target_id, []).append(rel.source_id)
        queue = deque([(source_id, [source_id])])
        visited = {source_id}
        while queue:
            current, path = queue.popleft()
            for neighbor in adj.get(current, []):
                if neighbor in visited:
                    continue
                new_path = path + [neighbor]
                if neighbor == target_id:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
        return []

    async def build_cluster(
        self,
        category: str,
        *,
        min_strength: float = 0.3,
        max_nodes: int = 50,
    ) -> ClusterResponse:
        problems = await self.problems.get_by_category(category)
        problems = problems[:max_nodes]
        nodes = [_node(p) for p in problems]
        id_set = {p.id for p in problems}
        edges = []
        for rel in await self.relationships.get_edges_for_category(category):
            if rel.strength < min_strength:
                continue
            if rel.source_id in id_set and rel.target_id in id_set:
                edges.append(
                    GraphEdge(
                        source_id=rel.source_id,
                        target_id=rel.target_id,
                        relationship_type=rel.relationship_type,
                        strength=rel.strength,
                    )
                )
        return ClusterResponse(category=category, nodes=nodes, edges=edges)
