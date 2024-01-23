import os
from dotenv import load_dotenv
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from producer import publish_to_main
from sqlalchemy import Column, Integer, UniqueConstraint
import requests
from urllib.parse import quote_plus


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Construct the database URL
quoted_password = quote_plus(os.getenv("POSTGRES_PASSWORD"))
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{quoted_password}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
CORS(app)
# Configure Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and migration
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Product(db.Model):
    id = db.Column(Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))

class ProductUser(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')

@app.route('/api/products')
def index():
    products = Product.query.all()

    # Convert Product instances to a list of dictionaries
    products_list = []
    for product in products:
        product_dict = {
            'id': product.id,
            'title': product.title,
            'image': product.image
        }
        products_list.append(product_dict)

    return jsonify(products_list)

@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    try:
        req = requests.get('http://localhost:8000/api/user')
        json_data = req.json()

        product_user = ProductUser(user_id=json_data['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()

        publish_to_main('product_liked', id)

    except:
        abort(400, 'you already like the post')

    return jsonify({'message': 'success'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
