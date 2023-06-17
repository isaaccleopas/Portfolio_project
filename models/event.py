#!/usr/bin/python3
"""Contains event class"""
from sqlalchemy import Column, String, LargeBinary, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models

class Event(BaseModel, Base):
    """Represents event attributes"""
    __tablename__ = "events"
    title = Column(String(128), nullable=False)
    description = Column(String(256), nullable=False)
    image = Column(String(255))
    venue = Column(String(128), nullable=False)
    date_time = Column(DateTime, nullable=False)
    slots_available = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'))
    user = relationship("User", back_populates="events")
    reviews = relationship("Review", back_populates="event",
                           cascade="all, delete")
    reservations = relationship("Reservation", back_populates="event",
                           cascade="all, delete")

    def to_dict(self, include_reviews=False):
        event_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'venue': self.venue,
            'date_time': self.date_time.isoformat(),
            'slots_available': self.slots_available,
            'reviews': [review.to_dict() for review in self.reviews]
        }

        return event_dict

    def __init__(self, *args, **kwargs):
        image_file = kwargs.pop("image_file", None)
        super().__init__(*args, **kwargs)
        self.image = image_file
