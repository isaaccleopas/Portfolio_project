#!/usr/bin/python3
"""Contains review class"""
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class Review(BaseModel, Base):
    """Represents review class attributes"""
    __tablename__ = "reviews"
    content = Column(Text, nullable=False)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)

    if 'models' in dir():
        if models.storage_t == 'db':
            event = relationship("Event", backref="reviews")
            user = relationship("User", backref="reviews")
