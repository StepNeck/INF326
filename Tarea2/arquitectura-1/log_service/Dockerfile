FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto (para que shortener vea log_service_pb2, etc.)
COPY . .

EXPOSE 50051

CMD ["python", "-m", "log_service.server"]
