#!/usr/bin/python3
"""
Contains the TestEventDocs classes
"""
from datetime import datetime
import inspect
import models
from models import storage
from models import event
from models.base_model import BaseModel
import pep8
import unittest
Event = event.Event


class TestEventDocs(unittest.TestCase):
    """Tests to check the documentation and style of Event class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.event_f = inspect.getmembers(Event, inspect.isfunction)

    def test_pep8_conformance_event(self):
        """Test that models/event.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/event.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_event(self):
        """Test that tests/test_models/test_event.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_event.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_event_module_docstring(self):
        """Test for the event.py module docstring"""
        self.assertIsNot(event.__doc__, None,
                         "event.py needs a docstring")
        self.assertTrue(len(event.__doc__) >= 1,
                        "event.py needs a docstring")

    def test_event_class_docstring(self):
        """Test for the Event class docstring"""
        self.assertIsNot(Event.__doc__, None,
                         "Event class needs a docstring")
        self.assertTrue(len(Event.__doc__) >= 1,
                        "Event class needs a docstring")

    def test_event_func_docstrings(self):
        """Test for the presence of docstrings in Event methods"""
        for func in self.event_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestEvent(unittest.TestCase):
    """Test the Event class"""
    def test_is_subclass(self):
        """Test that Event is a subclass of BaseModel"""
        event = Event()
        self.assertIsInstance(event, BaseModel)
        self.assertTrue(hasattr(event, "id"))
        self.assertTrue(hasattr(event, "created_at"))
        self.assertTrue(hasattr(event, "updated_at"))

    def test_title_attr(self):
        """Test that Event has attr title, and it's an empty string"""
        event = Event()
        self.assertTrue(hasattr(event, "title"))
        self.assertEqual(event.title, "")

    def test_description_attr(self):
        """Test that Event has attr description, and it's an empty string"""
        event = Event()
        self.assertTrue(hasattr(event, "description"))
        self.assertEqual(event.description, "")

    def test_image_attr(self):
        """Test that Event has attr image, and it's an empty string"""
        event = Event()
        self.assertTrue(hasattr(event, "image"))
        self.assertEqual(event.image, "")

    def test_venue_attr(self):
        """Test that Event has attr venue, and it's an empty string"""
        event = Event()
        self.assertTrue(hasattr(event, "venue"))
        self.assertEqual(event.venue, "")

    def test_date_time_attr(self):
        """Test that Event has attr date_time, and it's None"""
        event = Event()
        self.assertTrue(hasattr(event, "date_time"))
        self.assertIsNone(event.date_time)

    def test_slots_available_attr(self):
        """Test that Event has attr slots_available, and it's 0"""
        event = Event()
        self.assertTrue(hasattr(event, "slots_available"))
        self.assertEqual(event.slots_available, 0)

    def test_user_id_attr(self):
        """Test that Event has attr user_id, and it's an empty string"""
        event = Event()
        self.assertTrue(hasattr(event, "user_id"))
        self.assertEqual(event.user_id, "")

    def test_reviews_attr(self):
        """Test that Event has attr reviews, and it's an empty list"""
        event = Event()
        self.assertTrue(hasattr(event, "reviews"))
        self.assertEqual(event.reviews, [])

    def test_to_dict_creates_dict(self):
        """Test that to_dict method creates a dictionary with proper attrs"""
        e = Event()
        new_d = e.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in e.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        e = Event()
        new_d = e.to_dict()
        self.assertEqual(new_d["__class__"], "Event")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], e.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], e.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output"""
        event = Event()
        string = "[Event] ({}) {}".format(event.id, event.__dict__)
        self.assertEqual(string, str(event))
