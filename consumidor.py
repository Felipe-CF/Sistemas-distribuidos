import pika

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")

# Conectar ao RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar a fila
channel.queue_declare(queue='hello')

# Consumir mensagens da fila
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

# Iniciar o consumo
channel.start_consuming()