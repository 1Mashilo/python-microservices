import pika
import json

import logging

# Enable RabbitMQ logging in your application code
logging.basicConfig(level=logging.DEBUG)
pika_logger = logging.getLogger('pika')
pika_logger.setLevel(logging.DEBUG)
# RabbitMQ connection URL
rabbitmq_url = "amqp://guest:guest@localhost:5672/"

# Establish a connection
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
channel = connection.channel()

# Declare a queue for communication with "main"
channel.queue_declare(queue='main')

def publish_to_main(message_body, content_type):
    channel.basic_publish(
        exchange='',
        routing_key='main',
        body=json.dumps(message_body),
        properties=pika.BasicProperties(content_type=content_type)
    )

# Example: Publishing a message from "admin" service (Django backend)
message_body = {"id": 1, "title": "Product 1", "image": "image_url"}
publish_to_main(message_body, content_type='product_created')

# Close the RabbitMQ connection
#connection.close()
