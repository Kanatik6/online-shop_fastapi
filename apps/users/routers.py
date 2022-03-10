from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends,Body
from products.crud import create_cart

from database import get_db
from users import schemas, crud

router = APIRouter(prefix='/users')


@router.post('/sing-up/', response_model=schemas.ReturnUser, tags=['user'])
async def create_user(*, db: Session = Depends(get_db), user: schemas.User):
    user = crud.create_user(db=db, user=user)
    create_cart(db=db, id=user.id)
    return user


@router.post('/sing-in/', tags=['user'])
async def login_user(*, db: Session = Depends(get_db), user: schemas.UserLogin, tags=['user']):
    return crud.login_user(db=db, user=user)


@router.post('/sing-in/refresh_token', tags=['user'])
async def refresh_user(token:str=Body(...,)):
    return crud.login_refresh_user(token=token)
