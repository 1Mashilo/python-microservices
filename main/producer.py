import pika
import json

# Set up RabbitMQ connection parameters
params = pika.URLParameters('your_rabbitmq_url')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish_to_main(method, body):
    # Set up RabbitMQ message properties
    properties = pika.BasicProperties(method)
    
    # Publish message to the 'admin' queue
    channel.basic_publish(
        exchange='',
        routing_key='admin',
        body=json.dumps(body),
        properties=properties
    )

# Close RabbitMQ connection
connection.close()
