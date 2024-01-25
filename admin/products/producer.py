import pika
import json

params = pika.URLParameters('your_rabbitmq_url')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish_to_main(method, body):
    """
    Publish a message to the 'main' RabbitMQ queue.

    Parameters:
    - method (str): The method for the message (e.g., 'product_created', 'product_updated', 'product_deleted').
    - body (dict): The message body as a dictionary.

    Returns:
    None
    """
    properties = pika.BasicProperties(method)
    channel.basic_publish(
        exchange='',
        routing_key='main',
        body=json.dumps(body),
        properties=properties
    )
