from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends

from main import get_db
from products import models,schemas,crud

router = APIRouter(prefix='poducts')


router.get('/',response_model=schemas.ReturnProduct)
async def get_products(db:Session = Depends(get_db())):
    return crud.get_products(db=db)


router.get('/{id}',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db()),id:int):
    return crud.get_products(db=db,id=id)


router.post('/',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db()),product=schemas.Product):
    return crud.create_product(db=db,product=product)


router.put('/{id}',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db()),product=schemas.Product,id:int):
    return crud.put_product(db=db,product=product,id=id)


router.patch('/{id}',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db()),product=schemas.PatchProduct,id:int):
    return crud.put_product(db=db,product=product,id=id)


router.delete('/{id}',response_model=schemas.ReturnProduct)
async def get_products(*,db:Session = Depends(get_db()),id:int):
    return crud.delete_product(db=db,id=id)


app.include_router(router=router)
