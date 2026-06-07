"""FTS5 bootstrap — no-op for MVP; search uses SQLAlchemy ilike."""

from app.core.logging import get_logger

logger = get_logger(__name__)


async def bootstrap_fts() -> None:
    logger.debug("fts.skipped", reason="using_sqlalchemy_search")
