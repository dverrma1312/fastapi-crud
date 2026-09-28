from typing import Any
import time

_cache: dict[str, dict[str, Any]] = {}


def get_cache(key: str) -> Any | None:
    if key not in _cache:
        return None
    
    entry = _cache[key]
    if time.time() - entry["timestamp"] > entry["ttl"]:
        del _cache[key]
        return None
    
    return entry["data"]


def set_cache(key: str, data: Any, ttl: int = 3600) -> None:
    _cache[key] = {
        "data": data,
        "timestamp": time.time(),
        "ttl": ttl,
    }


def clear_cache() -> None:
    _cache.clear()