from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from apps.products import schemas,models


def get_products(db:Session):
    return db.query(models.Product).all()


def get_product(db:Session,id:int):
    return db.query(models.Product).filter_by(id=id)


def create_product(db:Session,product:schemas.Product):
    if db.query(models.Product).filter_by(title=product.title).exists():
        raise HTTPException(status_code=400,detail='title must be unique')
    product = models.Product(title=product.title,
                             descriptions=product.descriptions,
                             price=product.price,
                             amount=product.amount)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def put_product(db:Session,product:schemas.Product,id):
    product = db.query(models.Product).filter_by(id=id)
    if not product.first():
        raise HTTPException(status_code=400,
                            detail='product not found')
    product.update(product.dict())
    db.commit()
    return db.query(models.Product).filter_by(id=id).first()


def patch_product(db:Session,product:schemas.Product,id):
    product = db.query(models.Product).filter_by(id=id)
    if not product.first():
        raise HTTPException(status_code=400,
                            detail='product not found')
    product.update(product.dict(exclude_unset=True))
    db.commit()
    return db.query(models.Product).filter_by(id=id).first()


def delete_product(db:Session,product:schemas.Product,id):
    product = db.query(models.Product).filter_by(id=id)
    if not product.first():
        raise HTTPException(status_code=400,
                            detail='product not found')
    db.delete(product.first())
    db.commit()
    return JSONResponse({'success':True},
                        status_code=204)


def create_cart(db:Session,id:int):
    user = db.query(models.User).filter_by(id=id)
    if not user.first:
        raise HTTPException(status_code=400,detail='user not found')
    cart = models.Cart(user=user.first())
    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def add_products(db:Session,cart_id,products:schemas.AddProduct):
    cart = db.query(models.Cart).filter(models.Cart.id==cart_id).first()
    product = db.query(models.Product).filter_by(id=product.id).first()
    
    cart.cart_product