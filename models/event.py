#!/usr/bin/python3
"""Contains event class"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models

class Event(BaseModel, Base):
    """Represents event attributes"""
    if models.storage_t == 'db':
        __tablename__ = "events"
        title = Column(String(128), nullable=False)
        description = Column(String(256), nullable=False)
        image = Column(String(128), nullable=False)
        venue = Column(String(128), nullable=False)
        date_time = Column(DateTime, nullable=False)
        slots_available = Column(Integer, nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'))
        reviews = relationship("Review", backref="event")

    else:
        title = ""
        description = ""
        image = ""
        venue = ""
        date_time = ""
        slots_available = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
