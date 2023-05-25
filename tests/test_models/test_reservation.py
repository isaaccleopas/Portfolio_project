#!/usr/bin/python3
"""
Contains the TestReservationDocs classes
"""
from datetime import datetime
import inspect
import models
from models import reservation
from models.base_model import BaseModel
import pep8
import unittest
Reservation = reservation.Reservation


class TestReservationDocs(unittest.TestCase):
    """Tests to check the documentation and style of Reservation class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.reservation_f = inspect.getmembers(Reservation, inspect.isfunction)

    def test_pep8_conformance_reservation(self):
        """Test that models/reservation.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/reservation.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_reservation(self):
        """Test that tests/test_models/test_reservation.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_reservation.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_reservation_module_docstring(self):
        """Test for the reservation.py module docstring"""
        self.assertIsNot(reservation.__doc__, None,
                         "reservation.py needs a docstring")
        self.assertTrue(len(reservation.__doc__) >= 1,
                        "reservation.py needs a docstring")

    def test_reservation_class_docstring(self):
        """Test for the Reservation class docstring"""
        self.assertIsNot(Reservation.__doc__, None,
                         "Reservation class needs a docstring")
        self.assertTrue(len(Reservation.__doc__) >= 1,
                        "Reservation class needs a docstring")

    def test_reservation_func_docstrings(self):
        """Test for the presence of docstrings in Reservation methods"""
        for func in self.reservation_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

class TestReservation(unittest.TestCase):
    """Test the Reservation class"""
    def test_is_subclass(self):
        """Test that Reservation is a subclass of BaseModel"""
        reservation = Reservation()
        self.assertIsInstance(reservation, BaseModel)
        self.assertTrue(hasattr(reservation, "id"))
        self.assertTrue(hasattr(reservation, "created_at"))
        self.assertTrue(hasattr(reservation, "updated_at"))

    def test_event_id_attr(self):
        """Test that Reservation has attr event_id, and it's an empty string"""
        reservation = Reservation()
        self.assertTrue(hasattr(reservation, "event_id"))
        self.assertEqual(reservation.event_id, "")

    def test_to_dict_creates_dict(self):
        """Test that to_dict method creates a dictionary with proper attrs"""
        r = Reservation()
        new_d = r.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in r.__dict__:
            if attr != "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """Test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        r = Reservation()
        new_d = r.to_dict()
        self.assertEqual(new_d["__class__"], "Reservation")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], r.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], r.updated_at.strftime(t_format))

    def test_str(self):
        """Test that the str method has the correct output"""
        reservation = Reservation()
        string = "[Reservation] ({}) {}".format(reservation.id, reservation.__dict__)
        self.assertEqual(string, str(reservation))
