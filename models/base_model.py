#!/usr/bin/python3
"""
Contains the BaseModel Class
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy()

class BaseModel:
    """BaseModel class from which other classes will inherit base data"""
    __abstract__ = True
    id = Column(String (60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
