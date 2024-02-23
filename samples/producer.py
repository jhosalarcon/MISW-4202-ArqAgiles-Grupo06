import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

message = "Q'hubo viejo Cristian !!!"
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print(" [x] Sent 'Hello World!'")

connection.close()

