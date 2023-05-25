#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from models.base_model import BaseModel
import models
from models.event import Event
from models.reservation import Reservation
from models.review import Review
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

classes = {"Event": Event, "Reservation": Reservation, "Review": Review, "User": User}

class DBStorage:
    """Interacts with the MySQL database"""
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

    def all(self, cls=None):
        """Query the current database"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session__.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object based on the class and its ID"""
        objs = self.all(cls)
        for obj in objs.values():
            if obj.id == id:
                return obj
        return None
