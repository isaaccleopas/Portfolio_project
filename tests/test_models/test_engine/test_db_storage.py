#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""
import inspect
import models
import pep8
import unittest
from models.base_model import BaseModel
from models.engine import db_storage
from models.event import Event
import json
import os
from models.reservation import Reservation
from models.review import Review
from models.user import User
from sqlalchemy.orm import scoped_session, sessionmaker
from models import storage
DBStorage = db_storage.DBStorage
classes = {"Event": Event, "Reservation": Reservation, "Review": Review,
                   "User": User}

class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(db_storage.DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(db_storage.DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(db_storage.DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        cls.storage = db_storage.DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Remove the test environment"""
        cls.storage.close()

    def test_all_returns_dict(self):
        """Test that all method returns a dictionary"""
        all_objs = self.storage.all()
        self.assertIsInstance(all_objs, dict)

    def test_all_returns_specific_class(self):
        """Test that all method returns objects of a specific class"""
        all_users = self.storage.all(User)
        for obj in all_users.values():
            self.assertIsInstance(obj, User)

    def test_new(self):
        """Test that new method adds an object to the current session"""
        user = User()
        self.storage.new(user)
        session = scoped_session(sessionmaker())()
        self.assertIn(user, session)

    def test_save(self):
        """Test that save method commits all changes to the database"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        session = scoped_session(sessionmaker())()
        self.assertNotIn(user, session.new)

    def test_delete(self):
        """Test that delete method deletes an object from the database"""
        user = User()
        self.storage.new(user)
        self.storage.save()
        self.storage.delete(user)
        session = scoped_session(sessionmaker())()
        self.assertNotIn(user, session)

    def test_reload(self):
        """Test that reload method reloads data from the database"""
        session1 = self.storage._DBStorage__session
        self.storage.reload()
        session2 = self.storage._DBStorage__session
        self.assertIsNot(session1, session2)
