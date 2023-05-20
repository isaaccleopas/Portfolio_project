#!/usr/bin/python3
"""Contains rrservation class"""

from sqlalchemy import Column, String, ForeignKey
from base_model import BaseModel, Base


class Reservation(BaseModel, Base):
    """Represents reservation attributes"""
    __tablename__ = "reservations"
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
