import unittest
import sys
from test_base import run_unittests
from test_base import captured_io
import os
import pickle
import csv
from data import create_data
from data import display_calendar
import app
from unittest.mock import patch
from authentication.authenticate import *
from io import StringIO
import re
from tabulate import tabulate


class test_acceptance(unittest.TestCase):

    def test_unittest_app_exist(self):
        import tests.test_app
        self.assertTrue('tests.test_app' in sys.modules, "test_app module should be found")


    def test_unittest_app_succeeds(self):
        test_result = run_unittests("tests.test_app")
        self.assertTrue(test_result.wasSuccessful(), "app unit tests should succeed")


    def test_unittest_auth_exist(self):
        import tests.test_auth
        self.assertTrue('tests.test_auth' in sys.modules, "test_auth module should be found")


    def test_unittest_auth_succeeds(self):
        test_result = run_unittests("tests.test_auth")
        self.assertTrue(test_result.wasSuccessful(), "auth unit tests should succeed")


    def test_unittest_display_exist(self):
        import tests.test_display
        self.assertTrue('tests.test_display' in sys.modules, "test_display module should be found")


    def test_unittest_display_succeeds(self):
        test_result = run_unittests("tests.test_display")
        self.assertTrue(test_result.wasSuccessful(), "display unit tests should succeed")


    def test_unittest_test_patient_slot_booking_exists(self):
        import tests.test_patient_slot_booking
        self.assertTrue("tests.test_patient_slot_booking" in sys.modules, "test_patient_slot_booking module should be found.")


    def test_unittest_test_patient_slot_booking_succeeds(self):
        test_result = run_unittests("tests.test_patient_slot_booking")
        self.assertTrue(test_result.wasSuccessful(), "patient slot booking unit tests should succeed")


    def test_unittest_test_create_data_exists(self):
        import tests.test_create_data
        self.assertTrue("tests.test_create_data" in sys.modules, "test_create_data module should be found.")


    def test_unittest_test_create_data_succeeds(self):
        test_result = run_unittests("tests.test_create_data")
        self.assertTrue(test_result.wasSuccessful(), "create data unit tests should succeed")


    def test_unittest_cancel_patient_booking(self):
        import tests.test_cancel_patient_booking
        self.assertTrue('tests.test_cancel_patient_booking' in sys.modules, "test_cancel_patient_booking module should be found")


    def test_unittest_cancel_patient_booking(self):
        test_result = run_unittests('tests.test_cancel_patient_booking')
        self.assertTrue(test_result.wasSuccessful(), "cancel_patient_booking unit tests should succeed")


    def test_unittest_cancel_slot(self):
        import tests.test_cancel_slot
        self.assertTrue('tests.test_cancel_slot' in sys.modules, "test_cancel_slot module should be found")


    def test_unittest_cancel_slot(self):
        test_result = run_unittests('tests.test_cancel_slot')
        self.assertTrue(test_result.wasSuccessful(), "cancel_slot unit tests should succeed")


    def test_unittest_format_data(self):
        import tests.test_format_data
        self.assertTrue('tests.test_format_data' in sys.modules, "test_format_data module should be found")


    def test_unittest_format_data(self):
        test_result = run_unittests('tests.test_format_data')
        self.assertTrue(test_result.wasSuccessful(), "format_data unit tests should succeed")


    def test_unittest_making_a_slot(self):
        import tests.test_making_a_slot
        self.assertTrue('tests.test_making_a_slot' in sys.modules, "test_making_a_slot module should be found")


    def test_unittest_making_a_slot(self):
        test_result = run_unittests('tests.test_making_a_slot')
        self.assertTrue(test_result.wasSuccessful(), "making_a_slot unit tests should succeed")


if __name__ == '__main__':
    unittest.main()
