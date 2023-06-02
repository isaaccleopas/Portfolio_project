#!/usr/bin/python3
"""Contains user class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import hashlib
from flask_login import UserMixin

class User(UserMixin, BaseModel, Base):
    """Represents user attributes"""
    __tablename__ = "users"
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    google_id = Column(String(128), unique=True)
    facebook_id = Column(String(128), unique=True)
    reviews = relationship("Review", back_populates="user")
    events = relationship("Event", back_populates="user",
                          cascade="all, delete")
    reservations = relationship("Reservation", back_populates="user",
                                cascade="all, delete")

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
        if "google_token" in kwargs:
            # Handle Google sign-up logic using Firebase
            google_token = kwargs["google_token"]
            # Add your Firebase Google sign-up logic here
            kwargs['google_token'] = google_token
        if "facebook_token" in kwargs:
            # Handle Facebook sign-up logic using Firebase
            facebook_token = kwargs["facebook_token"]
            # Add your Firebase Facebook sign-up logic here
            kwargs['facebook_token'] = facebook_token
        super().__init__(*args, **kwargs)
