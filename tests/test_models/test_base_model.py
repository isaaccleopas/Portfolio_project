#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
import inspect
import models
import pep8 as pycodestyle
import time
from models import storage
from unittest import mock
from datetime import datetime
from models.base_model import BaseModel
BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the docstring tests"""
        cls.base_model_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/base_model.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(models.base_model.__doc__, None,
                         "base_model.py needs a docstring")
        self.assertTrue(len(models.base_model.__doc__) > 1,
                        "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) > 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_model_funcs:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) > 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        self.assertIsInstance(inst.created_at, datetime)
        self.assertIsInstance(inst.updated_at, datetime)

    def test_id_creation(self):
        """Test that BaseModel assigns a unique ID"""
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def test_str(self):
        """Test that the __str__ method has the correct output"""
        b = BaseModel()
        string = "[BaseModel] ({}) {}".format(b.id, b.__dict__)
        self.assertEqual(string, str(b))

    def test_save(self):
        """Test that save method updates the updated_at attribute"""
        b = BaseModel()
        old_updated_at = b.updated_at
        b.save()
        self.assertNotEqual(old_updated_at, b.updated_at)

    def test_to_dict(self):
        """Test that to_dict method returns a dictionary"""
        b = BaseModel()
        b_dict = b.to_dict()
        self.assertEqual(type(b_dict), dict)

    def test_to_dict_has_all_attrs(self):
        """Test that to_dict method includes all attributes"""
        b = BaseModel()
        b_dict = b.to_dict()
        self.assertTrue("id" in b_dict)
        self.assertTrue("created_at" in b_dict)
        self.assertTrue("updated_at" in b_dict)
        self.assertTrue("__class__" in b_dict)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        b = BaseModel()
        b_dict = b.to_dict()
        self.assertEqual(b_dict["__class__"], "BaseModel")
        self.assertEqual(type(b_dict["created_at"]), str)
        self.assertEqual(type(b_dict["updated_at"]), str)
        self.assertEqual(b_dict["created_at"], b.created_at.strftime(t_format))
        self.assertEqual(b_dict["updated_at"], b.updated_at.strftime(t_format))

    def test_delete(self):
        """Test that delete method deletes the instance from storage"""
        b = BaseModel()
        models.storage.new(b)
        models.storage.save()
        b.delete()
        self.assertNotIn(b, models.storage.all().values())
