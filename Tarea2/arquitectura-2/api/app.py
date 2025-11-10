from litestar import Litestar, post, get
from litestar.response import Redirect, Response
from litestar.stores.redis import RedisStore
from litestar.config.response_cache import ResponseCacheConfig
from litestar.middleware.rate_limit import RateLimitConfig
import redis, base62, os

# Configuración de entorno

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
API_URL = os.getenv("API_URL", "http://localhost:8000")

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
def create_short_url(data: dict) -> dict:
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return Response({"error": "Internal server error"}, status_code=500)
    
    try:
        last_id = r.get("last_id")
        new_id = int(last_id) + 1 if last_id else 597652312
        hash_code = base62.encode(new_id)
        long_url = data["long_url"]

    except Exception as e:
        print(f"Error processing request data: {e}")
        return Response({"error": "Internal server error"}, status_code=500)
    
    try:
        r.hset(f"url:{hash_code}", mapping={"id": new_id, "long_url": long_url})
        r.set("last_id", new_id)
    except Exception as e:
        print(f"Error saving to Redis: {e}")
        return {"error": "Internal server error"}, 500
    
    return {"short_url": f"{API_URL}/{hash_code}"}

# Ruta GET para redirigir a URL larga

@get("/{hash_code:str}", cache=True)
def redirect(hash_code: str) -> Redirect:
    print(f"Received hash_code: {hash_code}")
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()

    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return Response({"error": "Internal server error"}, status_code=500)
    
    try:
        long_url = r.hget(f"url:{hash_code}", "long_url")

    except Exception as e:
        print(f"Error retrieving from Redis: {e}")
        return Response({"error": "Internal server error"}, status_code=500)
    
    if not long_url:
        return Response({"error": "url not found"}, status_code=404)

    return Redirect(long_url, status_code=301)

app = Litestar(
    route_handlers=[create_short_url, redirect],
    middleware=[rate_limit_config.middleware],    # controla arribo de eventos
    stores={"redis_cache": redis_store},          # registra el store
    response_cache_config=response_cache_config,  # cachea respuestas
)
