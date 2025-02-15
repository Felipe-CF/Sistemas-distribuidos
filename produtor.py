import pika
import json


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='gateway')

message = {
    'method': 'POST',
    'data': 'teste'
}

channel.basic_publish(exchange='', routing_key='gateway', body=json.dumps(message))

print('[x] Sent "teste"')

connection.close()
