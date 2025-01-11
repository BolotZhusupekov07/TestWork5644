from redis.asyncio import Redis as ARedis
from redis import Redis

from src.common.configs import Settings


def get_async_cache_client(settings: Settings) -> ARedis:
    return ARedis(
        host=settings.redis.redis_host,
        port=settings.redis.redis_port,
        encoding="utf-8",
        decode_responses=True
    )

def get_cache_client(settings: Settings) -> Redis:
    return Redis(
        host=settings.redis.redis_host,
        port=settings.redis.redis_port,
        encoding="utf-8",
        decode_responses=True
    )
