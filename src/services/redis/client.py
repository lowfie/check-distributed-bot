import json

from redis.asyncio.client import Redis


def get_redis():
    from src.config import settings
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )


class RedisClient:
    def __init__(self) -> None:
        self.redis = Redis(host="redis", port=6379, db=0, decode_responses=True)

    async def set_str(self, key: str, value: str) -> None:
        await self.redis.set(key, value)

    async def get_str(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def get_float(self, key: str) -> float | None:
        value = await self.redis.get(key)
        if not value:
            return
        return float(value)

    async def set_float(self, key: str, value: float, ex: float = None) -> None:
        await self.redis.set(key, str(value), ex=ex)

    async def get_int(self, key: str) -> int | None:
        value = await self.redis.get(key)
        if not value:
            return
        return int(value)

    async def set_int(self, key: str, value: int, ex: float = None) -> None:
        await self.redis.set(key, str(value), ex=ex)

    async def set_dict(self, key: str, value: dict) -> None:
        await self.redis.set(key, json.dumps(value))

    async def get_dict(self, key: str) -> dict | None:
        try:
            return json.loads(await self.redis.get(key))
        except TypeError:
            return None


redis = RedisClient()
