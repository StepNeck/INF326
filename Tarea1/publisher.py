import pika, json

def publish_event(event):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='sismos', exchange_type='fanout')

    channel.basic_publish(
        exchange='sismos',
        routing_key='',
        body=json.dumps(event)
    )
    print(" [x] Evento enviado:", event)
    connection.close()

# Ejemplo
# event = {
#     "id": "318410",
#     "fecha_hora": "2025-09-23T02:34:56Z",
#     "lat": -33.12,
#     "lon": -70.56,
#     "profundidad_km": 10,
#     "magnitud": 4.8,
#     "magnitud_tipo": "Mw"
# }
with open("events.json") as f:
    events = json.load(f)

for event in events:
    publish_event(event)
