from litestar import Litestar, post, get
from litestar.response import Redirect, Response
from litestar.stores.redis import RedisStore
from litestar.config.response_cache import ResponseCacheConfig
from litestar.middleware.rate_limit import RateLimitConfig
import redis, base62, os

# Variables de entorno (inyectadas por docker-compose)
REDIS_URL = os.getenv("REDIS_URL", "redis://redis2:6379")
REDIS_HOST = os.getenv("REDIS_HOST", "redis2")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
API_URL = os.getenv("API_URL", "http://localhost:8080")

# Store Redis para caché
redis_store = RedisStore.with_client(url=REDIS_URL)

# Configuración de caché de respuestas 
response_cache_config = ResponseCacheConfig(
    store="redis_cache",
    default_expiration=60
)

# Configuración del rate limiter
rate_limit_config = RateLimitConfig(rate_limit=("minute", 5))

START_ID = 597652313

# Ruta POST para crear URL corta
@post("/shorten")
def create_short_url(data: dict) -> dict:
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        # Incrementa el contador
        new_id = r.incr("next_url_id")
    
        if new_id == 1:
            r.set("next_url_id", START_ID)
            new_id = START_ID
        hash_code = base62.encode(new_id)
        long_url = data["url"]

        r.hset(f"url:{hash_code}", mapping={"id": new_id, "long_url": long_url})
        r.set("last_id", new_id)

        return {"short_url": f"{API_URL}/{hash_code}"}
    except Exception as e:
        print(f"Error interno: {e}")
        return Response({"error": "Internal server error"}, status_code=500)

# Ruta GET para redirigir a URL larga
@get("/{hash_code:str}", cache=True)
def redirect(hash_code: str) -> Redirect | Response:
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        long_url = r.hget(f"url:{hash_code}", "long_url")
        if not long_url:
            return Response({"error": "url not found"}, status_code=404)
        return Redirect(long_url, status_code=301)
    except Exception as e:
        print(f"Error interno: {e}")
        return Response({"error": "Internal server error"}, status_code=500)

app = Litestar(
    route_handlers=[create_short_url, redirect],
    middleware=[rate_limit_config.middleware],
    stores={"redis_cache": redis_store},
    response_cache_config=response_cache_config,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=False)
