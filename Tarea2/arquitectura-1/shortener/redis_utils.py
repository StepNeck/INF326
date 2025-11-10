import os
import base62
import redis.asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

START_ID = 597652313

async def shortener_url(long_url: str) -> str:
    """Genera una URL corta y la guarda en Redis"""
    # Incrementa el contador
    id_value = await redis_client.incr("next_url_id")
    
    if id_value == 1:
        await redis_client.set("next_url_id", START_ID)
        id_value = START_ID

    short_hash = base62.encode(id_value)
    await redis_client.set(f"url:{short_hash}", long_url)
    return short_hash

async def resolve_url(short_hash: str) -> str | None:
    """Devuelve la URL original"""
    value = await redis_client.get(f"url:{short_hash}")
    return value if value else None
