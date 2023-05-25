#!/usr/bin/python3
"""Contains rrservation class"""
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base


class Reservation(BaseModel, Base):
    """Represents reservation attributes"""
    __tablename__ = "reservations"

    def __init__(self, *args, **kwargs):
        """initializes Reservation"""
        super().__init__(*args, **kwargs)
        if models.storage_t == 'db':
            self.event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
