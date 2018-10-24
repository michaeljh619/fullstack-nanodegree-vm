#!/usr/bin/python

# imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem

'''
Contains a class definition for the QueryHandler which will
make calling SQLAlchemy queries a lot easier.
'''

'''
This class is designed for handling queries to the restaurant
database. All session logic is encapsulated inside the QueryHandler
class.
'''
class QueryHandler:
    # Constructor initializes a session
    def __init__(self):
        # create and bind engine
        engine = create_engine('sqlite:///restaurantmenu.db')
	Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        # session instance var is connected and ready to use
        self.session = DBSession()

    # close the session
    def close(self):
        self.close()

    def get_session(self):
        return self.session
