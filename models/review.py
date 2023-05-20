#!/usr/bin/python3
"""Contains review class"""

from sqlalchemy import Column, String, ForeignKey, text
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from base_model import BaseModel, Base
from event import Event
from user import User

class Review(BaseModel, Base):
    """Represents review class attributes"""
    __tablename__ = "reviews"
    content = Column(Text, nullable=False)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    event = relationship("Event", backref="reviews")
    user = relationship("User", backref="reviews")
