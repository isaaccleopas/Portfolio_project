#!/usr/bin/python3
"""Contains user class"""

from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

class User(BaseModel, Base):
    """Represents user attributes"""
    __tablename__ = "users"
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    google_id = Column(String(128), unique=True)
    facebook_id = Column(String(128), unique=True)
    reviews = relationship("Review", backref="user")
    events = relationship("Event", backref="user")
    reservations = relationship("Reservation", backref="user")
