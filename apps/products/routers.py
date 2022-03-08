from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends
from users.auth.jwt_bearer import get_current_user
from users.auth.jwt_bearer import JWTBearer

from database import get_db
from products import schemas,crud

router = APIRouter(prefix='/products')


@router.get('/',response_model=list[schemas.ReturnProduct])
async def get_products(db:Session = Depends(get_db)):
    return crud.get_products(db=db)


@router.get('/{id}/',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db),id:int):
    return crud.get_product(db=db,id=id)


@router.post('/',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db),product:schemas.Product):
    return crud.create_product(db=db,product=product)


@router.put('/{id}/',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db),product:schemas.Product,id:int):
    return crud.put_product(db=db,product=product,id=id)


@router.patch('/{id}/',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db),product:schemas.PatchProduct,id:int):
    return crud.patch_product(db=db,product=product,id=id)


@router.delete('/{id}/',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db),id:int):
    return crud.delete_product(db=db,id=id)


@router.post('/{id}/add/',response_model=schemas.ReturnCart,dependencies=[Depends(JWTBearer())])
async def get_products(*,db:Session = Depends(get_db),cart_id:int = Depends(get_current_user),product:schemas.AddProduct):
    return crud.add_products(db=db,cart_id=cart_id,product=product)


@router.get('/cart/{id}/',response_model=schemas.ReturnCart)
async def get_products(*,db:Session = Depends(get_db),id:int):
    return crud.get_cart(db=db,id=id)
