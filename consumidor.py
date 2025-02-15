import os
import pika
import json
from zeep import Client
from flask import send_file



def list_and_send(ch, method, properties, body):

    message_json = json.loads(body.decode())

    client = Client(message_json['url_wsdl'])

    if message_json['service'] == 'upload':

        response = client.service.UploadArquivo(
            message_json['file_name'],
            message_json['file'],
        )

    elif message_json['service'] == 'download':

        response = client.service.DownloadArquivo(message_json['file_name'])

        temp_file = os.path.join(message_json['file_name'])

        dir = os.path.dirname(os.path.abspath(__file__)) + "//temp"

        temp_file_path = os.path.join(dir, message_json['file_name'])

        with open(temp_file_path, 'wb') as f:

            f.write(response)

    else:
        response = client.service.DeleteArquivo(message_json['file_name'])

    x = 2


# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar a fila
channel.queue_declare(queue='gateway')

# Consumir mensagens da fila
channel.basic_consume(queue='gateway', on_message_callback=list_and_send, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

# Iniciar o consumo
channel.start_consuming()