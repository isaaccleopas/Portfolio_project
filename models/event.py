#!/usr/bin/python3
"""Contains event class"""
from sqlalchemy import Column, String, DateTime, Integer
from base_model import BaseModel, Base

class Event(BaseModel, Base):
    """Represents event attributes"""
    __tablename__ = "events"
    title = Column(String(128), nullable=False)
    description = Column(String(256), nullable=False)
    image = Column(String(128), nullable=False)
    venue = Column(String(128), nullable=False)
    date_time = Column(DateTime, nullable=False)
    slots_available = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'))
    reviews = relationship("Review", backref="event")
