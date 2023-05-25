#!/usr/bin/python3
"""Contains review class"""
import models
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class Review(BaseModel, Base):
    """Represents review class attributes"""
    if models.storage_t == 'db':
        __tablename__ = "reviews"
        content = Column(Text, nullable=False)
        event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        event = relationship("Event", backref="reviews")
        user = relationship("User", backref="reviews")

    else:
        content = ""
        event_id = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
