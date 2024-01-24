import pika
import json

import logging

# RabbitMQ connection URL
rabbitmq_url = "amqp://guest:guest@localhost:5672/"

# Establish a connection
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
channel = connection.channel()

# Declare a queue for communication with "admin"
channel.queue_declare(queue='admin')

def publish_to_main(method, body):
    properties=pika.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key='admin',
        body=json.dumps(body),
        properties=properties
    )