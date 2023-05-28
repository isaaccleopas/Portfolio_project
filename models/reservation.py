#!/usr/bin/python3
"""Contains reservation class"""
import models
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Reservation(BaseModel, Base):
    """Represents reservation attributes"""
    __tablename__ = "reservations"
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    slots_reserved = Column(Integer, nullable=False)
    event = relationship("Event", back_populates="reservations",
                         overlaps="reservations")
    user = relationship("User", back_populates="reservations")
    
    def __init__(self, *args, **kwargs):
        """Initializes Reservation"""
        super().__init__(*args, **kwargs)
