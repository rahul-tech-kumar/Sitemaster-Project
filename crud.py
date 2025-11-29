from sqlalchemy.orm import Session
import models
from db import get_db, engine
from datetime import datetime

# Users
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, name: str, email: str):
    user = models.User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, name: str = None, email: str = None):
    user = get_user(db, user_id)
    if not user:
        return None
    if name:
        user.name = name
    if email:
        user.email = email
        db.commit()
        db.refresh(user)
        return user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return True


# Products
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, name: str, category: str, price: float):
    p = models.Product(name=name, category=category, price=price)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def update_product(db: Session, product_id: int, name: str = None, category: str = None, price: float = None):
    p = get_product(db, product_id)
    if not p:
        return None
    if name:
        p.name = name
    if category:
        p.category = category
    if price is not None:
        p.price = price
    db.commit()
    db.refresh(p)
    return p


def delete_product(db: Session, product_id: int):
    p = get_product(db, product_id)
    if not p:
        return None
    db.delete(p)
    db.commit()
    return True



# Orders
def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OrderedProduct).offset(skip).limit(limit).all()


def create_order(db: Session, user_id: int, product_id: int, quantity: int = 1, ordered_at: datetime = None):
    if ordered_at is None:
        ordered_at = datetime.utcnow()
    order = models.OrderedProduct(user_id=user_id, product_id=product_id, quantity=quantity, ordered_at=ordered_at)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order_id: int):
    order = db.query(models.OrderedProduct).filter(models.OrderedProduct.id == order_id).first()
    if not order:
        return None
    db.delete(order)
    db.commit()
    return True