from apps.database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from users.models import User


class Product(Base):
    __tablename__='products'
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    descriptions = Column(String)
    price = Column(Integer)
    amount = Column(Integer)
    
    cart = relationship('Cart',secondary='CartProduct',back_populates='products')


class Cart(Base):
    __tablename__ = 'carts'
    
    id = Column(Integer,primary_key=True,index=True)
    user = Column(Integer,ForeignKey(User.id))

    cart = relationship('Cart',secondary='CartProduct',back_populates='carts')
    
    @property
    def total_price(self):
        products = self.cart_products.filter(cart_id=self.id)
        return


class CartProduct(Base):
    __tablename__ = 'carts_products'

    cart_id = Column(Integer,ForeignKey(Cart.id),primary_key=True,index=True)
    product_id = Column(Integer,ForeignKey(Product.id),primary_key=True,index=True)
    amount_products = Column(Integer)
    cart = relationship(Cart,back_populates='cart_products')
    product = relationship(Product,back_populates='cart_products')
