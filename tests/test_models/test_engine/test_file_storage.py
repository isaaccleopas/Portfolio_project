import json
import os
import pep8
import unittest
from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.event import Event
from models.base_model import BaseModel
from models.review import Review
from models.reservation import Reservation
from models.user import User

FileStorage = file_storage.FileStorage
classes = {
    "Event": Event,
    "BaseModel": BaseModel,
    "Reservation": Reservation,
    "Review": Review,
    "User": User
}

class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8"""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_models/test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up the class"""
        cls.storage = FileStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Tear down the class"""
        del cls.storage
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all(self):
        """Test the all method of FileStorage"""
        # Add objects to storage
        event = Event()
        event_id = event.id
        event_key = "Event." + event_id
        self.storage.new(event)
        review = Review()
        review_id = review.id
        review_key = "Review." + review_id
        self.storage.new(review)
        reservation = Reservation()
        reservation_id = reservation.id
        reservation_key = "Reservation." + reservation_id
        self.storage.new(reservation)
        user = User()
        user_id = user.id
        user_key = "User." + user_id
        self.storage.new(user)
        self.storage.save()

         # Test all() without arguments
        objects = self.storage.all()
        self.assertEqual(type(objects), dict)
        self.assertIn(event_key, objects)
        self.assertEqual(objects[event_key], event)
        self.assertIn(review_key, objects)
        self.assertEqual(objects[review_key], review)
        self.assertIn(reservation_key, objects)
        self.assertEqual(objects[reservation_key], reservation)
        self.assertIn(user_key, objects)
        self.assertEqual(objects[user_key], user)

        # Test all() with class argument
        objects = self.storage.all(Event)
        self.assertEqual(type(objects), dict)
        self.assertIn(event_key, objects)
        self.assertEqual(objects[event_key], event)
        self.assertNotIn(review_key, objects)
        self.assertNotIn(reservation_key, objects)
        self.assertNotIn(user_key, objects)

        objects = self.storage.all("Review")
        self.assertEqual(type(objects), dict)
        self.assertNotIn(event_key, objects)
        self.assertIn(review_key, objects)
        self.assertEqual(objects[review_key], review)
        self.assertNotIn(reservation_key, objects)
        self.assertNotIn(user_key, objects)

    def test_new(self):
        """Test the new method of FileStorage"""
        obj = BaseModel()
        obj_id = obj.id
        obj_key = "BaseModel." + obj_id
        self.storage.new(obj)
        self.assertIn(obj_key, self.storage.all())
        self.assertEqual(self.storage.all()[obj_key], obj)

    def test_save(self):
        """Test the save method of FileStorage"""
        obj = BaseModel()
        obj_id = obj.id
        obj_key = "BaseModel." + obj_id
        self.storage.new(obj)
        self.storage.save()

        # Check if file was created
        self.assertTrue(os.path.exists("file.json"))

        # Load data from file
        with open("file.json", "r") as f:
            data = json.load(f)

        self.assertIn(obj_key, data)
        self.assertEqual(data[obj_key]["__class__"], "BaseModel")
        self.assertEqual(data[obj_key]["id"], obj_id)

    def test_reload(self):
        """Test the reload method of FileStorage"""
        # Create a new storage instance and load data from file
        storage2 = FileStorage()
        storage2.reload()

        # Check if objects were loaded correctly
        self.assertEqual(len(storage2.all()), len(self.storage.all()))

        obj = BaseModel()
        obj_id = obj.id
        obj_key = "BaseModel." + obj_id
        self.storage.new(obj)
        self.storage.save()

        # Reload data in storage2 and check if new object was added
        storage2.reload()
        self.assertIn(obj_key, storage2.all())
        self.assertEqual(storage2.all()[obj_key], obj)

    def test_delete(self):
        """Test the delete method of FileStorage"""
        obj = BaseModel()
        obj_id = obj.id
        obj_key = "BaseModel." + obj_id
        self.storage.new(obj)
        self.storage.save()

        # Check if object is in storage
        self.assertIn(obj_key, self.storage.all())

        # Delete the object and save changes
        self.storage.delete(obj)
        self.storage.save()

        # Check if object is deleted from storage
        self.assertNotIn(obj_key, self.storage.all())

    def test_get(self):
        """Test the get method of FileStorage"""
        obj = BaseModel()
        obj_id = obj.id
        obj_key = "BaseModel." + obj_id
        self.storage.new(obj)
        self.storage.save()

        # Get the object using get() method
        get_obj = self.storage.get(BaseModel, obj_id)

        # Check if the obtained object is the same as the original object
        self.assertEqual(get_obj, obj)
