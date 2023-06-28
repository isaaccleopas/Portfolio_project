#!/usr/bin/python3
"""Contains user class"""
import hashlib
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from flask_login import UserMixin

class User(UserMixin, BaseModel, Base):
    """Represents user attributes"""
    __tablename__ = "users"
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    reviews = relationship("Review", back_populates="user")
    events = relationship("Event", back_populates="user",
                          cascade="all, delete")
    reservations = relationship("Reservation", back_populates="user",
                                cascade="all, delete")

    def set_password(self, password):
        """Sets the password for the user by hashing it"""
        self.password = hashlib.md5(password.encode()).hexdigest()

    def validate_password(self, password):
        hashed_input_password = hashlib.md5(password.encode()).hexdigest()
        return self.password == hashed_input_password

    def get_id(self):
        """Returns the user ID as a string"""
        return str(self.id)

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)
        if "password" in kwargs:
            password = kwargs["password"]
            m = hashlib.md5()
            m.update(str.encode(password))
            kwargs['password'] = m.hexdigest()
        super().__init__(*args, **kwargs)
