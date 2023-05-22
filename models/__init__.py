#!/usr/bin/python3
"""Initializes the models package"""

from os import getenv

storage = getenv(EVENT_TYPE_STORAGE)

if storage == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()

storage.reload()
