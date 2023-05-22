#!/usr/bin/python3
"""
Contains the class DBStorage
"""
import models
from models.base_model import BaseModel, Base
from models.event import Event
from models.review import Review
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Event": Event, "Reservation": Reservation, "Review": Review,
           "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        EVENT_MYSQL_USER = getenv('EVENT_MYSQL_USER')
        EVENT_MYSQL_PWD = getenv('EVENT_MYSQL_PWD')
        EVENT_MYSQL_HOST = getenv('EVENT_MYSQL_HOST')
        EVENT_MYSQL_DB = getenv('EVENT_MYSQL_DB')
        EVENT_ENV = getenv('EVENT_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(EVENT_MYSQL_USER,
                                             EVENT_MYSQL_PWD,
                                             EVENT_MYSQL_HOST,
                                             EVENT_MYSQL_DB))
        if EVENT_ENV == "test":
            Base.metadata.drop_all(self.__engine)
