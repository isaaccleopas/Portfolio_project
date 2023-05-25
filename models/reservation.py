#!/usr/bin/python3
"""Contains rrservation class"""
import models
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class Reservation(BaseModel, Base):
    """Represents reservation attributes"""
    if models.storage_t == 'db':
        __tablename__ = "reservations"
        event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    else:
        event_id = ""
        user_id = ""

    def __init__(self, *args, **kwargs):
        """initializes Reservation"""
        super().__init__(*args, **kwargs)
