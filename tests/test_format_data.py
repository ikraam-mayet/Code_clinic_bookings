import sys
import unittest
import datetime
from io import StringIO
from tests import mock_api
from unittest.mock import patch
from data import format_data

class test_format_data(unittest.TestCase):

    def test_get_time_date(self):
        lfm = '2020-12-14T20:10:50.999'
        result = format_data.get_time_date(lfm)
        self.assertEqual(result, ('14 December 2020', '20:10', datetime.datetime(2020, 12, 14, 20, 10, 50, 999000)))