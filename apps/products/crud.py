from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from products.models import Product
from users.models import User

from products import schemas, models


def exist(filter):
    if not filter.first():
        raise HTTPException(status_code=400, detail=f'not found')
    return filter.first()


def get_products(db: Session):
    return db.query(models.Product).all()


def get_product(db: Session, id: int):
    return db.query(models.Product).filter_by(id=id).first()


def create_product(db: Session, product: schemas.Product):
    if db.query(models.Product).filter_by(title=product.title).first():
        raise HTTPException(status_code=400, detail='title must be unique')
    product = models.Product(title=product.title,
                             descriptions=product.descriptions,
                             price=product.price,
                             amount=product.amount)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def put_product(db: Session, product: schemas.Product, id: int):
    db_product = db.query(models.Product).filter_by(id=id)
    if not db_product.first():
        raise HTTPException(status_code=400,
                            detail='product not found')
    db_product.update(product.dict(exclude={'amount_products'}))
    db.commit()
    return db.query(models.Product).filter_by(id=id).first()


def patch_product(db: Session, product: schemas.PatchProduct, id: int):
    db_product = db.query(models.Product).filter_by(id=id)
    if not db_product.first():
        raise HTTPException(status_code=400,
                            detail='product not found')
    db_product.update(product.dict(
        exclude={'amount_products'}, exclude_unset=True))
    db.commit()
    return db.query(models.Product).filter_by(id=id).first()


def delete_product(db: Session, id: int):
    product = exist(db.query(models.Product).filter_by(id=id))

    db.delete(product)
    db.commit()
    return JSONResponse({'success': True},
                        status_code=204)


def create_cart(db: Session, id: int):
    user = exist(db.query(User.id).filter_by(id=id))
    cart = models.Cart(user_id=user[0])

    db.add(cart)
    db.commit()
    db.refresh(cart)
    return cart


def add_products(db: Session, cart_id, product: schemas.SetProduct):
    id = cart_id.get('userID')
    db_product = exist(db.query(models.Product).filter_by(id=product.id))
    cart = exist(db.query(models.Cart).filter_by(id=id))

    # declare cart_product secondary object
    if cart.products:
        cart.products.append(db_product)
    else:
        cart.products = [db_product]
    cart_product = db.query(models.CartProduct).filter_by(
        cart_id=cart.id, product_id=db_product.id).first()

    # i need add amount of db_product if amount of product less
    print(product.amount, ' - ', cart_product.amount_products,
          ' - ', db_product.amount)
    if product.amount + cart_product.amount_products > db_product.amount:

        # my mistake is that i mixed up places
        cart.total_price += db_product.price * \
            (db_product.amount - cart_product.amount_products)
        cart_product.amount_products += (db_product.amount -
                                         cart_product.amount_products)
    else:
        cart.total_price += db_product.price * product.amount
        cart_product.amount_products += product.amount

    db.commit()
    return cart


def remove_products(db: Session, cart_id, product: schemas.SetProduct):
    id = cart_id.get('userID')
    db_product = exist(db.query(models.Product).filter_by(id=product.id))
    cart = exist(db.query(models.Cart).filter_by(id=id))

    cart_product = exist(db.query(models.CartProduct).filter_by(
        cart_id=cart.id, product_id=db_product.id))

    # if removable amount bigger then number of product in car
    if cart_product.amount_products - product.amount < 1:
        cart_product_ids = [x.id for x in cart.products]
        db_cart_product_index = cart_product_ids.index(product.id)

        del cart.products[db_cart_product_index]
        cart.total_price -= db_product.price * cart_product.amount_products
        db.delete(cart_product)
    else:
        cart.total_price -= db_product.price * product.amount
        cart_product.amount_products -= product.amount

    db.commit()
    return cart


def remove_all_products(db: Session, cart_id):
    id = cart_id.get('userID')
    cart = exist(db.query(models.Cart).filter_by(id=id))

    db.query(models.CartProduct).filter_by(cart_id=cart.id).delete()

    cart.products = []
    cart.total_price = 0

    db.commit()
    return JSONResponse({'message': 'purchase is completed, please wait, our manager will contact you'})


def product_filter(db:Session,dict_filter:dict):
    db_products = db.query(Product).filter(
                               Product.price>dict_filter['price_from'],
                               Product.price<dict_filter['price_to'],
                               Product.amount>dict_filter['amount_from'],
                               Product.amount<dict_filter['amount_to']
                               )
    return db_products.all()


def get_cart(db: Session, id: int):
    return db.query(models.Cart).filter_by(id=id).first()
