<<<<<<< HEAD
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import crud

from db import engine, Base, get_db
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import func, text

# Create tables if not already exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title='SiteMaster Project API')

# Pydantic Schemas



from datetime import datetime

# Users
class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(UserCreate):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# Products
class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    price: float = 0.0

class ProductOut(ProductCreate):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# Orders
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: Optional[int] = 1

class OrderOut(OrderCreate):
    id: int
    ordered_at: Optional[datetime]

    class Config:
        from_attributes = True




# -------------------
# User Endpoints
# -------------------

@app.get('/users', response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

@app.get('/users/{user_id}', response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    u = crud.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail='User not found')
    return u

@app.post('/users', response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.name, user.email)

@app.put('/users/{user_id}', response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    up = crud.update_user(db, user_id, user.name, user.email)
    if not up:
        raise HTTPException(status_code=404, detail='User not found')
    return up

@app.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    res = crud.delete_user(db, user_id)
    if not res:
        raise HTTPException(status_code=404, detail='User not found')
    return {'ok': True}


# Product Endpoints


@app.get('/products', response_model=List[ProductOut])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip, limit)


@app.get('/products/{product_id}', response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    p = crud.get_product(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail='Product not found')
    return p


@app.post('/products', response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product.name, product.category, product.price)


@app.put('/products/{product_id}', response_model=ProductOut)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    up = crud.update_product(db, product_id, product.name, product.category, product.price)
    if not up:
        raise HTTPException(status_code=404, detail='Product not found')
    return up

@app.delete('/products/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    res = crud.delete_product(db, product_id)
    if not res:
        raise HTTPException(status_code=404, detail='Product not found')
    return {'ok': True}


# Orders Endpoints

@app.get('/orders', response_model=List[OrderOut])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip, limit)

@app.post('/orders', response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Check if user and product exist
    if not crud.get_user(db, order.user_id):
        raise HTTPException(status_code=400, detail='User not found')
    if not crud.get_product(db, order.product_id):
        raise HTTPException(status_code=400, detail='Product not found')
    return crud.create_order(db, order.user_id, order.product_id, order.quantity)


@app.delete('/orders/{order_id}')
def delete_order(order_id: int, db: Session = Depends(get_db)):
    res = crud.delete_order(db, order_id)
    if not res:
        raise HTTPException(status_code=404, detail='Order not found')
    return {'ok': True}


# Analytics Endpoints



@app.get('/analytics/most_purchased')
def most_purchased_products(limit: int = 5, db: Session = Depends(get_db)):
    q = db.query(models.Product.name, func.sum(models.OrderedProduct.quantity).label('total_qty')) \
        .join(models.OrderedProduct, models.Product.id == models.OrderedProduct.product_id) \
        .group_by(models.Product.id) \
        .order_by(func.sum(models.OrderedProduct.quantity).desc()) \
        .limit(limit)
    return [{'product': r[0], 'total_qty': int(r[1])} for r in q]


@app.get('/analytics/top_users')
def top_users(limit: int = 5, db: Session = Depends(get_db)):
    q = db.query(models.User.name, func.sum(models.OrderedProduct.quantity).label('total_qty')) \
        .join(models.OrderedProduct, models.User.id == models.OrderedProduct.user_id) \
        .group_by(models.User.id) \
        .order_by(func.sum(models.OrderedProduct.quantity).desc()) \
        .limit(limit)
    return [{'user': r[0], 'total_qty': int(r[1])} for r in q]


# Run Backup Endpoint (Stored Procedure)


@app.post('/run_backup')
def run_backup(db: Session = Depends(get_db)):
    try:
        db.execute(text('CALL copy_all_data()'))
        db.commit()
        return {'ok': True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
=======
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import crud

from db import engine, Base, get_db
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import func, text

# Create tables if not already exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title='SiteMaster Project API')

# -------------------
# Pydantic Schemas
# -------------------


from datetime import datetime

# Users
class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(UserCreate):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# Products
class ProductCreate(BaseModel):
    name: str
    category: Optional[str] = None
    price: float = 0.0

class ProductOut(ProductCreate):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# Orders
class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: Optional[int] = 1

class OrderOut(OrderCreate):
    id: int
    ordered_at: Optional[datetime]

    class Config:
        from_attributes = True




# -------------------
# User Endpoints
# -------------------

@app.get('/users', response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip, limit)

@app.get('/users/{user_id}', response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    u = crud.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail='User not found')
    return u

@app.post('/users', response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user.name, user.email)

@app.put('/users/{user_id}', response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    up = crud.update_user(db, user_id, user.name, user.email)
    if not up:
        raise HTTPException(status_code=404, detail='User not found')
    return up

@app.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    res = crud.delete_user(db, user_id)
    if not res:
        raise HTTPException(status_code=404, detail='User not found')
    return {'ok': True}

# -------------------
# Product Endpoints
# -------------------

@app.get('/products', response_model=List[ProductOut])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip, limit)

@app.get('/products/{product_id}', response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    p = crud.get_product(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail='Product not found')
    return p

@app.post('/products', response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product.name, product.category, product.price)

@app.put('/products/{product_id}', response_model=ProductOut)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    up = crud.update_product(db, product_id, product.name, product.category, product.price)
    if not up:
        raise HTTPException(status_code=404, detail='Product not found')
    return up

@app.delete('/products/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    res = crud.delete_product(db, product_id)
    if not res:
        raise HTTPException(status_code=404, detail='Product not found')
    return {'ok': True}

# -------------------
# Orders Endpoints
# -------------------

@app.get('/orders', response_model=List[OrderOut])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip, limit)

@app.post('/orders', response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Check if user and product exist
    if not crud.get_user(db, order.user_id):
        raise HTTPException(status_code=400, detail='User not found')
    if not crud.get_product(db, order.product_id):
        raise HTTPException(status_code=400, detail='Product not found')
    return crud.create_order(db, order.user_id, order.product_id, order.quantity)

@app.delete('/orders/{order_id}')
def delete_order(order_id: int, db: Session = Depends(get_db)):
    res = crud.delete_order(db, order_id)
    if not res:
        raise HTTPException(status_code=404, detail='Order not found')
    return {'ok': True}

# -------------------
# Analytics Endpoints
# -------------------

@app.get('/analytics/most_purchased')
def most_purchased_products(limit: int = 5, db: Session = Depends(get_db)):
    q = db.query(models.Product.name, func.sum(models.OrderedProduct.quantity).label('total_qty')) \
        .join(models.OrderedProduct, models.Product.id == models.OrderedProduct.product_id) \
        .group_by(models.Product.id) \
        .order_by(func.sum(models.OrderedProduct.quantity).desc()) \
        .limit(limit)
    return [{'product': r[0], 'total_qty': int(r[1])} for r in q]

@app.get('/analytics/top_users')
def top_users(limit: int = 5, db: Session = Depends(get_db)):
    q = db.query(models.User.name, func.sum(models.OrderedProduct.quantity).label('total_qty')) \
        .join(models.OrderedProduct, models.User.id == models.OrderedProduct.user_id) \
        .group_by(models.User.id) \
        .order_by(func.sum(models.OrderedProduct.quantity).desc()) \
        .limit(limit)
    return [{'user': r[0], 'total_qty': int(r[1])} for r in q]

# -------------------
# Run Backup Endpoint (Stored Procedure)
# -------------------

@app.post('/run_backup')
def run_backup(db: Session = Depends(get_db)):
    try:
        db.execute(text('CALL copy_all_data()'))
        db.commit()
        return {'ok': True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
>>>>>>> 498502810ca9416d5b074d8652d2c9ddec3e27ed
