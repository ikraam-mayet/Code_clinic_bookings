import unittest
from io import StringIO
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
        self.assertTrue('test.test_app' in sys.modules, "test_app module should be found")


    def test_unittest_app_succeeds(self):
        import tests.test_app
        test_result = run_unittests("test_app")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")


    def test_unittest_auth_exist(self):
        import tests.test_auth
        self.assertTrue('test.test_auth' in sys.modules, "test_auth module should be found")


    def test_unittest_auth_succeeds(self):
        import tests.test_auth
        test_result = run_unittests("test_auth")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")


    def test_unittest_display_exist(self):
        import tests.test_display
        self.assertTrue('test_display' in sys.modules, "test_display module should be found")


    def test_unittest_display_succeeds(self):
        import tests.test_display
        test_result = run_unittests("test_display")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")



if __name__ == '__main__':
    unittest.main()
