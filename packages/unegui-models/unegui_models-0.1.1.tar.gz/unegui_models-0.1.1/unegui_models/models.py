from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship
from . import db_settings

Base = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**db_settings.DATABASE))

def create_table(engine):
    Base.metadata.create_all(engine)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    price = Column('price', Float)
    tag = Column('tag', String)
    test = Column('test', String)

class CarListing(Base):
    __tablename__ = 'car_listings'

    id = Column(Integer, primary_key=True)
    link = Column(Text)
    prepayment_amount = Column(Float)
    engine_capacity = Column(Float)
    transmission = Column(String)
    drive_type = Column(String)
    car_type = Column(String)
    color = Column(String)
    manufacture_year = Column(Integer)
    import_year = Column(Integer)
    engine_type = Column(String)
    interior_color = Column(String)
    leasing = Column(String)
    location = Column(String)
    wheel_drive = Column(String)
    mileage = Column(Integer)
    condition = Column(String)
    doors = Column(Integer)
    description = Column(Text)
    monthly_payment = Column(Float)
    loan_term = Column(Integer)
    price = Column(Float)
    brand = Column(String)
    model = Column(String)
    province = Column(String)
    district = Column(String)

    images = relationship("CarImage", back_populates="car_listing")

class CarImage(Base):
    __tablename__ = 'car_images'

    id = Column(Integer, primary_key=True)
    car_listing_id = Column(Integer, ForeignKey('car_listings.id'))
    img_url = Column(Text)

    car_listing = relationship("CarListing", back_populates="images")


class CarListingJson(Base):
    __tablename__ = 'car_listing_json'

    id = Column(Integer, primary_key=True)
    car_listing_id = Column(Integer, ForeignKey('car_listings.id'))
    json_data = Column(JSON)

    car_listing = relationship("CarListing")