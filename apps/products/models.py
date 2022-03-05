from apps.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from users.models import User


class Product(Base):
    __tablename__='products'
    
    title = Column(String,unique=True)
    descriptions = Column(String)
    price = Column(Integer)
    amount = Column(Integer)


class Cart(Base):
    user = Column(Integer,ForeignKey(User.id))
    total_price= Column(Integer,default=0)


class CartProduct(Base):
    cart = Column(Integer,ForeignKey(Cart.id))
    product = Column(Integer,ForeignKey(Product.id))
    amount_products = Column(Integer,default=1)
