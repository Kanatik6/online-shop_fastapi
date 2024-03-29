from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query
from users.auth.jwt_bearer import get_current_user
from users.auth.jwt_bearer import JWTBearer
from users.auth.permissions import test_permission

from database import get_db
from products import schemas, crud

router = APIRouter(prefix='/products')

async def query_params(price_from:int = Query(default=1,gt=0),
                       price_to:int = Query(default=1000000),
                       amount_from:int = Query(default=1,gt=0),
                       amount_to:int = Query(default=100000,gt=1)):
    return {'price_from':price_from,
            'price_to':price_to,
            'amount_from':amount_from,
            'amount_to':amount_to
            }
    

@router.get('/', response_model=list[schemas.ReturnProduct], tags=['products'])
async def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db=db)


@router.get('/{id}/', response_model=schemas.ReturnProduct, tags=['products'],dependencies=[Depends(test_permission)])
async def get_product(*, db: Session = Depends(get_db), id: int):
    return crud.get_product(db=db, id=id)


@router.get('/{id}/filter', response_model=list[schemas.ReturnProduct], tags=['products'])
async def get_product(*, db: Session = Depends(get_db),
                      filter_params = Depends(query_params)):
    return crud.product_filter(db=db,dict_filter=filter_params)


@router.post('/',dependencies=[Depends(JWTBearer())], response_model=schemas.ReturnProduct, tags=['products'])
async def create_products(*, db: Session = Depends(get_db), product: schemas.Product):
    return crud.create_product(db=db, product=product)


@router.put('/{id}/',dependencies=[Depends(JWTBearer())], response_model=schemas.ReturnProduct, tags=['products'])
async def put_products(*, db: Session = Depends(get_db), product: schemas.Product, id: int):
    return crud.put_product(db=db, product=product, id=id)


@router.patch('/{id}/', dependencies=[Depends(JWTBearer())],response_model=schemas.ReturnProduct, tags=['products'])
async def patch_products(*, db: Session = Depends(get_db), product: schemas.PatchProduct, id: int):
    return crud.patch_product(db=db, product=product, id=id)


@router.delete('/{id}/', dependencies=[Depends(JWTBearer())],response_model=schemas.ReturnProduct, tags=['products'])
async def delete_products(*, db: Session = Depends(get_db), id: int):
    return crud.delete_product(db=db, id=id)


@router.post('/{id}/add/', response_model=schemas.ReturnCart, dependencies=[Depends(JWTBearer())], tags=['cart'])
async def add_products(*, db: Session = Depends(get_db), cart_id: int = Depends(get_current_user), product: schemas.SetProduct):
    return crud.add_products(db=db, cart_id=cart_id, product=product)


@router.post('/{id}/remove/', response_model=schemas.ReturnCart, dependencies=[Depends(JWTBearer())], tags=['cart'])
async def remove_products(*, db: Session = Depends(get_db), cart_id: int = Depends(get_current_user), product: schemas.SetProduct):
    return crud.remove_products(db=db, cart_id=cart_id, product=product)


@router.post('/{id}/buy/', response_model=schemas.ReturnCart, dependencies=[Depends(JWTBearer())], tags=['cart'])
async def buy_products(*, db: Session = Depends(get_db), cart_id: int = Depends(get_current_user)):
    return crud.remove_all_products(db=db, cart_id=cart_id)


@router.get('/cart/{id}/', response_model=schemas.ReturnCart, tags=['cart'])
async def get_cart(*, db: Session = Depends(get_db), id: int):
    return crud.get_cart(db=db, id=id)
