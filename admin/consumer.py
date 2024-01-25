import pika
import json
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

# Import the Product model
from products.models import Product

# Set up RabbitMQ connection parameters
params = pika.URLParameters('your_rabbitmq_url')
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Declare the queue for admin messages
channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    """
    Callback function to handle messages received from the "main" queue.

    Parameters:
    - ch: Channel
    - method: AMQP method
    - properties: Message properties
    - body: Message body
    """
    print('Received in admin')
    id = json.loads(body)

    # Retrieve the Product object by ID and increment the 'likes' count
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()

# Set up the consumer to listen for messages on the "admin" queue
channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages from "main" (Flask backend). To exit, press CTRL+C')
channel.start_consuming()
