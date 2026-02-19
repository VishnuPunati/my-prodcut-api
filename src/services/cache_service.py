import json
import redis
from typing import Any, Optional
from src.config import settings


class CacheService:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=True
        )
        self.ttl = settings.CACHE_TTL_SECONDS

    def get(self, key: str) -> Optional[Any]:
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except redis.RedisError:
            # Fail silently (important for high availability)
            return None

    def set(self, key: str, value: Any):
        try:
            self.client.setex(
                key,
                self.ttl,
                json.dumps(value, default=str)
            )
        except redis.RedisError:
            pass

    def delete(self, key: str):
        try:
            self.client.delete(key)
        except redis.RedisError:
            pass


cache_service = CacheService()
