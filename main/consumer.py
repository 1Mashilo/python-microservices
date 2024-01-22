import pika
import json
from flask import Flask  
from main import db, Product 
import logging


app = Flask(__name__)

# Enable RabbitMQ logging in your application code
logging.basicConfig(level=logging.DEBUG)
pika_logger = logging.getLogger('pika')
pika_logger.setLevel(logging.DEBUG)

# RabbitMQ connection URL
rabbitmq_url = "amqp://guest:guest@localhost:5672/"

# Establish a connection
connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
channel = connection.channel()

# Declare a queue for communication with "admin"
channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('Received in main (Flask backend):', body.decode())

    # Handle the received message based on properties.content_type
    data = json.loads(body)
    
    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
    
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        if product:
            product.title = data['title']
            product.image = data['image']
            db.session.commit()
    
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data['id'])
        if product:
            db.session.delete(product)
            db.session.commit()

# Set up the consumer to listen for messages on the "admin" queue
channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages from "admin" (Django backend). To exit, press CTRL+C')
channel.start_consuming()


