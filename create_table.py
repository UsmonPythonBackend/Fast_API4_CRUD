from database import Base, ENGINE
from models import User, Product, Order, Cargo

Base.metadata.create_all(bind=ENGINE)