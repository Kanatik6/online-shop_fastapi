from sqlalchemy import Column, Integer, String, ForeignKey, Table
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True)
    last_name = Column(String)
    hashed_password = Column(String)

    cart = relationship('Cart', back_populates='user', uselist=False)


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    descriptions = Column(String)
