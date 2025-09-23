import sys
import json
import pika
import requests
from geopy.distance import geodesic

# Diccionario con las coordenadas de cada ciudad; (latitud, longitud)
region = {
    "Arica": (-18.4746, -70.29792),
    "Coquimbo": (-29.95332, -71.33947),
    "Valparaiso": (-33.036, -71.62963),
    "Concepcion": (-36.82699, -73.04977),
    "PuntaArenas": (-53.16282, -70.90922),
}

# Verificamos que se pase una ciudad como argumento
if len(sys.argv) < 2:
    print("⚠️  Debes indicar una ciudad (Arica, Coquimbo, Valparaiso, Concepcion, PuntaArenas)")
    sys.exit(1)

ciudad = sys.argv[1]

if ciudad not in region:
    print(f"⚠️  Ciudad {ciudad} no es válida. Usa una de: {', '.join(region.keys())}")
    sys.exit(1)

coordenada = region[ciudad]

print(f" [*] Subscriber iniciado para {ciudad} en {coordenada}")

# Callback cuando llega un mensaje desde RabbitMQ
def callback(ch, method, properties, body):
    evento = json.loads(body)
    epicentro = (evento["lat"], evento["lon"])
    distancia = geodesic(coordenada, epicentro).km

    if distancia < 500:
        print(f"✅ {ciudad} interesado. Distancia: {distancia:.2f} km")
        try:
            r = requests.get(f"http://127.0.0.1:8000/sismos/{evento['id']}")
            print(f"ℹ️  Detalles detallada del sismo: {r.json()}")
        except Exception as e:
            print(f"⚠️  Error al consultar API: {e}")
    else:
        print(f"❌ {ciudad} ignorado. Distancia: {distancia:.2f} km")

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(exchange='sismos', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='sismos', queue=queue_name)

# Consumimos mensajes
channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print(" [*] Esperando eventos de sismos...\n")
channel.start_consuming()
