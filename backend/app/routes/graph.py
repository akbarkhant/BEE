from uuid import UUID

from fastapi import APIRouter, Path, Query
from typing import Annotated, Optional

from app.core.constants import GRAPH_DEFAULT_DEPTH, RelationshipType
from app.core.dependencies import AnalyticsServiceDep, GraphServiceDep, SettingsDep
from app.core.logging import get_logger
from app.schemas.graph import ClusterResponse, GraphResponse, NeighborResponse, PathResponse

router = APIRouter(prefix="/graph", tags=["Graph"])
logger = get_logger(__name__)

ProblemId = Annotated[UUID, Path(description="Problem UUID")]


@router.get("/cluster/{category}", response_model=ClusterResponse)
async def get_cluster(
    category: Annotated[str, Path()],
    min_strength: Annotated[float, Query(ge=0.0, le=1.0, alias="minStrength")] = 0.3,
    graph_svc: GraphServiceDep = None,
    settings: SettingsDep = None,
) -> ClusterResponse:
    cluster = await graph_svc.build_cluster(
        category=category,
        min_strength=min_strength,
        max_nodes=settings.GRAPH_MAX_NODES,
    )
    return ClusterResponse(category=category, nodes=cluster.nodes, edges=cluster.edges)


@router.get("/{problem_id}", response_model=GraphResponse, summary="Relationship graph")
async def get_graph(
    problem_id: ProblemId,
    depth: Annotated[int, Query(ge=1, le=5)] = GRAPH_DEFAULT_DEPTH,
    relationship_type: Annotated[Optional[RelationshipType], Query(alias="type")] = None,
    min_strength: Annotated[float, Query(ge=0.0, le=1.0, alias="minStrength")] = 0.3,
    graph_svc: GraphServiceDep = None,
    analytics_svc: AnalyticsServiceDep = None,
    settings: SettingsDep = None,
) -> GraphResponse:
    graph = await graph_svc.build_graph(
        problem_id=problem_id,
        depth=depth,
        relationship_type=relationship_type,
        min_strength=min_strength,
        max_nodes=settings.GRAPH_MAX_NODES,
    )
    if settings.ANALYTICS_ENABLED and analytics_svc:
        await analytics_svc.track_graph_traversal(
            problem_id=problem_id,
            depth=depth,
            node_count=len(graph.nodes),
        )
    return graph


@router.get("/{problem_id}/neighbors", response_model=NeighborResponse)
async def get_neighbors(
    problem_id: ProblemId,
    relationship_type: Annotated[Optional[RelationshipType], Query(alias="type")] = None,
    graph_svc: GraphServiceDep = None,
) -> NeighborResponse:
    neighbors = await graph_svc.get_neighbors(
        problem_id=problem_id,
        relationship_type=relationship_type,
    )
    return NeighborResponse(problem_id=problem_id, neighbors=neighbors)


@router.get("/{problem_id}/path", response_model=PathResponse)
async def get_path(
    problem_id: ProblemId,
    target_id: Annotated[UUID, Query(alias="targetId")],
    graph_svc: GraphServiceDep = None,
) -> PathResponse:
    path = await graph_svc.shortest_path(source_id=problem_id, target_id=target_id)
    return PathResponse(
        source_id=problem_id,
        target_id=target_id,
        path=path,
        found=bool(path),
    )
