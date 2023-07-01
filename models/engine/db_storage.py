#!/usr/bin/python3
"""
Contains the class DBStorage
"""
from models.base_model import BaseModel, Base
import models
from models.event import Event
from models.reservation import Reservation
from models.review import Review
from models.user import User
from os import getenv
import os
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()

classes = {"Event": Event, "BaseModel": BaseModel, "Reservation": Reservation, "Review": Review, "User": User}

class DBStorage:
    """Interacts with the PostgreSQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        internal_db_url = "postgres://event_dev:om2qPnXPOKJaefr24P1BQyCyXTi7vKE8@dpg-cig531lgkuvojjfkjbm0-a/event_dev_db"
        external_db_url = "postgres://event_dev:om2qPnXPOKJaefr24P1BQyCyXTi7vKE8@dpg-cig531lgkuvojjfkjbm0-a.singapore-postgres.render.com/event_dev_db"
        
        if os.getenv("EVENT_ENV", "dev") == "dev":
            self.__engine = create_engine(internal_db_url)
        else:
            self.__engine = create_engine(external_db_url)

        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def all(self, cls=None):
        """Query the current database"""
        objects = {}
        if cls:
            query_result = self.__session.query(cls).all()
        else:
            query_result = self.__session.query(BaseModel).all()
        for obj in query_result:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            objects[key] = obj
        return objects
    
    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        try:
            self.__session.commit()
        except SQLAlchemyError as e:
            print("Error occurred during save:", str(e))
            self.__session.rollback()
            raise

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload data from the database"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def close(self):
        """Close the session"""
        self.__session.close()

    def get(self, cls, id):
        """Retrieve an object based on the class and its ID"""
        key = '{}.{}'.format(cls.__name__, id)
        objects = self.all(cls)
        return objects.get(key, None)

    def count(self, cls=None):
        """
        Returns the number of objects in storage matching the given class name.
        """
        nobjects = 0
        for clss in classes.values():
            if cls is None or cls is clss or cls is clss.__name__:
                nobjects += len(self.__session.query(clss).all())
        return nobjects

    def get_user_by_email(self, email):
        """
        Retrieve a user object based on the email address.
        Returns None if the user is not found.
        """
        try:
            user = self.__session.query(User).filter_by(email=email).one()
            return user
        except NoResultFound:
            return None

    def get_user_by_name(self, name):
        """
        Retrieve a user object based on the name.
        Returns None if the user is not found.
        """
        try:
            user = self.__session.query(User).filter_by(name=name).one()
            return user
        except NoResultFound:
            return None
