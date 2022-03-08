from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,Table
from sqlalchemy.orm import relationship


class CartProduct(Base):
    __tablename__ = 'carts_products'

    cart_id = Column(Integer,ForeignKey('carts.id'),primary_key=True,index=True)
    product_id = Column(Integer,ForeignKey('products.id'),primary_key=True,index=True)
    amount_products = Column(Integer,default=0)
    product = relationship('Product',backref='cart_products',overlaps="cart_products,product")


class Product(Base):
    __tablename__='products'
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    descriptions = Column(String)
    price = Column(Integer)
    amount = Column(Integer)
    
    carts = relationship('Cart',secondary='carts_products',back_populates='products',overlaps="cart_products,product")


class Cart(Base):
    __tablename__ = 'carts'
    
    id = Column(Integer,primary_key=True,index=True)
    user = Column(Integer,ForeignKey('users.id'))
    total_price = Column(Integer,default=0)

    products = relationship('Product',secondary='carts_products',back_populates='carts')

    # @property
    # def total_price(self):
    #     products = self.cart_products.filter(cart_id=self.id)
    #     return

