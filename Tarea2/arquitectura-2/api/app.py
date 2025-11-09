from litestar import Litestar, post, get
from litestar.response import Redirect
from litestar.stores.redis import RedisStore
from litestar.config.response_cache import ResponseCacheConfig
from litestar.middleware.rate_limit import RateLimitConfig
import redis, base62, os

# Configuración de entorno
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
HOST = os.getenv("HOST", "http://localhost:8000")

# Store Redis para caché
redis_store = RedisStore.with_client(url=REDIS_URL)

# Configuración de caché de respuestas 
response_cache_config = ResponseCacheConfig(
    store="redis_cache",   # referencia al store registrado abajo
    default_expiration=60  # segundos que se mantendrá cada respuesta en cache
)

# Configuración del rate limiter
rate_limit_config = RateLimitConfig(rate_limit=("minute", 5))

# Definición de rutas

# Ruta POST para crear URL corta
@post("/")
async def create_short_url(data: dict) -> dict:
    redis = await redis.from_url(REDIS_URL, decode_responses=True)
    new_id = await redis.incr("next_id")  # autoincremento desde Redis
    hash_code = base62.encode(new_id)

    await redis.hset(f"url:{hash_code}", mapping={"id": new_id, "long_url": data["long_url"]})
    return {"id": new_id, "hash": hash_code, "short": f"{HOST}/{hash_code}"}

# Ruta GET para redirigir a URL larga

@get("/{hash_code:str}", cache=True)
async def redirect(hash_code: str) -> Redirect:
    redis = await redis.from_url(REDIS_URL, decode_responses=True)
    long_url = await redis.hget(f"url:{hash_code}", "long_url")

    if not long_url:
        return {"error": "URL no encontrada"}, 404

    return Redirect(url=long_url, status_code=301)

# --- Aplicación principal ---
app = Litestar(
    route_handlers=[create_short_url, redirect],
    middleware=[rate_limit_config.middleware],    # controla arribo de eventos
    stores={"redis_cache": redis_store},          # registra el store
    response_cache_config=response_cache_config,  # cachea respuestas
)
