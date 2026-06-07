# app/core/cache.py

import time
from collections import OrderedDict
from typing import Any, Optional

from app.core.logging import get_logger

logger = get_logger(__name__)


class InMemoryLRUCache:
    """
    High-performance in-memory LRU cache with TTL support.

    Features:
    - O(1) get/set operations
    - Automatic LRU eviction
    - Per-key TTL support
    - Manual invalidation
    - Expired key cleanup
    - Serverless-friendly (no Redis dependency)
    """

    def __init__(self, maxsize: int = 1024, default_ttl: int = 600):
        self.maxsize = maxsize
        self.default_ttl = default_ttl
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a cached value if present and not expired.
        """
        item = self.cache.get(key)

        if item is None:
            return None

        value, expires_at = item

        if time.time() > expires_at:
            self.cache.pop(key, None)
            return None

        self.cache.move_to_end(key)
        return value

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> None:
        """
        Store a value in cache.
        """
        chosen_ttl = ttl if ttl is not None else self.default_ttl
        expires_at = time.time() + chosen_ttl

        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = (value, expires_at)

        if len(self.cache) > self.maxsize:
            evicted_key, _ = self.cache.popitem(last=False)
            logger.debug(
                "cache.lru.evicted",
                key=evicted_key,
            )

    def invalidate(self, key: str) -> bool:
        """
        Remove a specific cache key.
        """
        removed = self.cache.pop(key, None)

        if removed:
            logger.debug(
                "cache.key.invalidated",
                key=key,
            )
            return True

        return False

    def clear(self) -> None:
        """
        Flush the entire cache.
        """
        self.cache.clear()

    def cleanup_expired(self) -> int:
        """
        Remove all expired entries.
        Returns number of deleted keys.
        """
        now = time.time()

        expired_keys = [
            key
            for key, (_, expires_at) in self.cache.items()
            if now > expires_at
        ]

        for key in expired_keys:
            self.cache.pop(key, None)

        return len(expired_keys)

    def stats(self) -> dict:
        """
        Cache metrics useful for debugging.
        """
        return {
            "size": len(self.cache),
            "maxsize": self.maxsize,
            "default_ttl": self.default_ttl,
        }

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    def __len__(self) -> int:
        return len(self.cache)


# ------------------------------------------------------------------
# Global Singleton
# ------------------------------------------------------------------

app_cache = InMemoryLRUCache(
    maxsize=1024,
    default_ttl=600,
)


# ------------------------------------------------------------------
# Lifecycle Hooks
# ------------------------------------------------------------------

async def init_cache() -> None:
    """
    Initialize cache during application startup.
    """
    logger.info(
        "cache.local_lru.initializing",
        maxsize=app_cache.maxsize,
    )

    app_cache.clear()

    logger.info("cache.local_lru.ready")


async def close_cache() -> None:
    """
    Cleanup cache during application shutdown.
    """
    logger.info("cache.local_lru.flushing")

    app_cache.clear()

    logger.info("cache.local_lru.closed")