import pika
import json
from flask import Flask  # Replace with your actual Flask imports
from database import db  # Replace with your actual module for database operations
from models import Product  # Replace with your actual model definition

app = Flask(__name__)

# RabbitMQ connection URL
rabbitmq_url = "amqps://cavynprl:2koEdoR42NgR6EX18jlc4zTkn9BcBlhP@shark.rmq.cloudamqp.com/cavynprl"
params = pika.URLParameters(rabbitmq_url)

# Establish a connection
connection = pika.BlockingConnection(params)
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

if __name__ == "__main__":
    app.run()
