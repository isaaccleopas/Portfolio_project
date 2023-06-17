#!/usr/bin/python3
"""Contains review class"""
import models
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class Review(BaseModel, Base):
    """Represents review class attributes"""
    __tablename__ = "reviews"
    content = Column(Text, nullable=False)
    event_id = Column(String(60), ForeignKey('events.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    event = relationship("Event", back_populates="reviews", overlaps="reviews")
    user = relationship("User", back_populates="reviews")

    def to_dict(self):
        """Returns a dictionary representation of the Review instance"""
        review_dict = {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at,
            "event_id": self.event_id,
            "user": {
                "id": self.user.id,
                "name": self.user.name
            }
        }
        return review_dict

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
