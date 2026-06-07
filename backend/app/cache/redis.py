# app/cache/redis.py

from app.core.cache import (
    app_cache,
    init_cache,
    close_cache,
)

__all__ = [
    "app_cache",
    "init_cache",
    "close_cache",
]