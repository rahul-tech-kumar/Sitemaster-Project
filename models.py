from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


    orders = relationship('OrderedProduct', back_populates='user', cascade='all, delete')


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    category = Column(String(100))
    price = Column(DECIMAL(10,2), default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)


    orders = relationship('OrderedProduct', back_populates='product', cascade='all, delete')


class OrderedProduct(Base):
    __tablename__ = 'ordered_products'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, default=1)
    ordered_at = Column(DateTime, default=datetime.utcnow)


    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')