from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship


class CartProduct(Base):
    __tablename__ = 'carts_products'

    cart_id = Column(
        Integer, ForeignKey('carts.id'),
        primary_key=True, index=True
    )
    product_id = Column(
        Integer, ForeignKey('products.id'),
        primary_key=True, index=True
    )
    product = relationship('Product', backref='cart_products',
                           overlaps="cart_products,product", uselist=False)
    amount_products = Column(Integer, default=0)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    descriptions = Column(String)
    price = Column(Integer)
    amount = Column(Integer)

    carts = relationship('Cart', secondary='carts_products',
                         back_populates='products', overlaps="cart_products,product")


class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Integer, default=0)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='cart')

    products = relationship(
        'Product', secondary='carts_products', back_populates='carts')
