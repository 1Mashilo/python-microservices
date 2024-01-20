from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    image = Column(String(200))

class ProductUser(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    product_id = Column(Integer)
