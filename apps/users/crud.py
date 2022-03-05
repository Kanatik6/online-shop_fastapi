from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from decouple import config
from users.auth.jwt_handler import singJWT
import time

from users import models,schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db:Session,user:schemas.User):
    # if first_name is exist, raise exception
    if db.query(models.User).filter_by(first_name=user.first_name).first() != None:
        raise HTTPException(status_code=400,detail='first_name must be unique, try again')
    
    user = models.User(first_name=user.first_name,
                       last_name=user.last_name,
                       hashed_password=pwd_context.hash(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db:Session,user:schemas.UserLogin):
    db_user=db.query(models.User).filter_by(first_name=user.first_name).first()
    if not db_user:
        raise HTTPException(status_code=401,detail='user not found')

    if not pwd_context.verify(user.password,db_user.hashed_password):
        raise HTTPException(status_code=401,detail='wrong password')

    token = singJWT(db_user.id)
    return token

def delete_user(db:Session,user:schemas.UserLogin):
    db_user=db.query(models.User).filter_by(first_name=user.first_name).first()
    if not db_user:
        raise HTTPException(status_code=401,detail='user not found')
    if not pwd_context.verify(user.password,db_user.hashed_password):
        raise HTTPException(status_code=401,detail='wrong password')
    db.delete(db_user)
    db.commit()
    return JSONResponse({'success':True},status_code=204)
