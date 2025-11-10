import os
import sys
sys.path.append(os.path.dirname(__file__))

import grpc
from concurrent import futures
from datetime import datetime
import redis.asyncio as aioredis
import asyncio
import log_service_pb2 as pb2
import log_service_pb2_grpc as pb2_grpc

# URL Redis desde variable de entorno
REDIS_URL = os.getenv("REDIS_LOG_URL", "redis://redis:6379/1")
redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)

class LogServiceServicer(pb2_grpc.LogServiceServicer):
    async def send_log_to_redis(self, url: str, timestamp: str):
        # Guardamos cada log como lista en Redis
        await redis_client.rpush("url_hits", f"{timestamp}|{url}")

    def SendUrlHit(self, request, context):
        try:
            asyncio.run(self.send_log_to_redis(request.url, request.timestamp))
        except Exception as e:
            print(f"Error guardando log en Redis: {e}")
        print(f"[{datetime.now()}] URL visitada: {request.url} @ {request.timestamp}")
        return pb2.LogResponse(status="OK")


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_LogServiceServicer_to_server(LogServiceServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC LogService ejecutándose en el puerto 50051...")
    server.start()
    server.wait_for_termination()
