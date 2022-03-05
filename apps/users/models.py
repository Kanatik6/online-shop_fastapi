from sqlalchemy import Column,Integer,String,ForeignKey,Table
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String,unique=True)
    last_name = Column(String)
    hashed_password = Column(String)
    
#     cart_id = Column(Integer,ForeignKey('cart.id'))
#     cart = relationship('Cart',back_populates='user')

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    descriptions = Column(String)
