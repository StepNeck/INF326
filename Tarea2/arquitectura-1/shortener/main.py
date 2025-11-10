import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "log_service"))

from datetime import datetime, timezone
import grpc
from litestar import Litestar, post, get
from litestar.response import Redirect, Response
from urllib.parse import urlparse
from log_service import log_service_pb2, log_service_pb2_grpc
from .redis_utils import shortener_url, resolve_url

GRPC_SERVER = os.getenv("GRPC_SERVER", "log_service:50051")
BASE_LOCAL = "http://localhost:8000"


@post("/shorten")
async def create_short_url(data: dict) -> dict:
    try:
        full_url = data.get("url")
        if not full_url:
            return {"error": "Falta la URL"}
        if not full_url.startswith(("http://", "https://")):
            full_url = "https://" + full_url

        short_hash = await shortener_url(full_url)
        short_url = f"{BASE_LOCAL}/{short_hash}"
        return {"short_url": short_url}
    except Exception as e:
        return {"error": f"Error interno: {str(e)}"}


@get("/{short_hash:str}")
async def redirect_to_original(short_hash: str) -> Redirect | Response:
    try:
        long_url = await resolve_url(short_hash)
        if not long_url:
            return {"error": "URL no encontrada"}

        try:
            with grpc.insecure_channel(GRPC_SERVER) as channel:
                stub = log_service_pb2_grpc.LogServiceStub(channel)
                hit = log_service_pb2.UrlHit(
                    url=long_url,
                    timestamp=datetime.now(timezone.utc).isoformat()
                )
                stub.SendUrlHit(hit)
        except Exception as e:
            print(f"gRPC error: {e}")

        return Redirect(long_url, status_code=302)
    except Exception as e:
        return {"error": f"Error interno: {str(e)}"}


app = Litestar(route_handlers=[create_short_url, redirect_to_original])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("shortener.main:app", host="0.0.0.0", port=8000, reload=True)
