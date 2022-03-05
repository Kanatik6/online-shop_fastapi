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


# class Product(Base):
#     __tablename__ = 'products'
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     short_descriptions = Column(String)
#     descriptions = Column(String)
#     price = Column(Integer)
    
#     carts = relationship('Cart',secondary='CartProduct',back_populates='products')


# class Cart(Base):
#     __tablename__ = 'carts'
    
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer,ForeignKey('users.id'))
#     user = relationship('User',back_populates='cart')
    
#     products = relationship('Product',secondary='CartProduct',back_populates='carts')

# CartProduct = Table('book_categorys', Base.metadata,
#     Column('cart_id', ForeignKey('carts.id'), primary_key=True),
#     Column('product_id', ForeignKey('products.id'), primary_key=True),
#     Column('price',Integer))


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    descriptions = Column(String)
