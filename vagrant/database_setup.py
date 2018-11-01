#!/usr/bin/python

# imports
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import os
import sys

'''
Script designed to set up an SQL database
using SQLAlchemy.
'''

# Create base class for sql tables
Base = declarative_base()


# Create Restaurant Class (table)
class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80),
                  nullable=False)
    id = Column(Integer,
                primary_key=True)

    @property
    def serialize(self):
        return{
            'name': self.name,
        }


# Create Menu Item Class (table)
class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80),
                  nullable=False)
    id = Column(Integer,
                primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer,
                           ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # returns object data in serializeable format
        return{
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }

# Sql Database setup footer
engine = create_engine(
    'sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
