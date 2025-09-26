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

with open("events.json") as f:
    events = json.load(f)

for event in events:
    publish_event(event)
