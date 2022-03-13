from fastapi import Depends
from decouple import config
from .jwt_bearer import JWTBearer
import jwt
from sqlalchemy.orm import Session
from users.models import User
from products.models import Cart,Product
from database import get_db
from fastapi.exceptions import HTTPException


JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


def test_permission(*,token: str = Depends(JWTBearer()),db:Session = Depends(get_db),id:int):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[
                         JWT_ALGORITHM], verify_signature=False)
    user_id = db.query(User.id).filter_by(id=payload.get("userID")).first()
    cart = db.query(Cart).filter_by(user_id=user_id[0]).first()
    product = db.query(Product).filter_by(id=id).first()
    if product not in cart.products:
        raise HTTPException(status_code=403,detail='not permitted')
    
