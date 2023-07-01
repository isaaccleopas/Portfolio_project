#!/usr/bin/python3
"""
Initialize the models package
"""

from os import getenv
from models.engine.db_storage import DBStorage

storage_t = getenv("EVENT_TYPE_STORAGE")

if storage_t == "db":
    storage = DBStorage()
else:
    storage = None

if storage:
    storage.reload()
