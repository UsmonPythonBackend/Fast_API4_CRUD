from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(155), nullable=False)
    last_name = Column(String(155), nullable=False)
    username = Column(String(155), unique=True)
    email = Column(String(155), nullable=False)
    password = Column(Text, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        # return '<User %r>' % self.username
        return f'User {self.username}'


class Order(Base):

    __tablename__ = 'orders'



    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    address = Column(String(300), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('product.id'))

    users = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')
    cargo = relationship('Cargo', back_populates='orders')

    def __repr__(self):
        return f"Order(id={self.id}, status={self.order_status})"

class Cargo(Base):

    __tablename__ = 'cargo'


    id = Column(Integer, primary_key=True)
    title = Column(String(155), nullable=False)
    quantity = Column(Integer, nullable=False)
    insurance = Column(Boolean, default=False)
    order_id = Column(Integer, ForeignKey('orders.id'))

    orders = relationship('Order', back_populates='cargo')

    def __repr__(self):
        return f"Product (title={self.title}, quantity={self.quantity})"

class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    rating = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    color = Column(String(50), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'))

    orders = relationship('Order', back_populates='product')

    def __repr__(self):
        return f"Product(title={self.title}, price={self.price})"







