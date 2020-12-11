import sys
import unittest
import datetime
from io import StringIO
from tests import mock_api
from unittest.mock import patch
from data.volunteer import making_a_slot

class test_making_a_slot(unittest.TestCase):

    expected_date = datetime.date.today()
    today_ = expected_date.strftime('%d %B %Y')

    @patch('sys.stdin', StringIO(f"{today_}\n"))
    def test_ask_for_date(self):
        sys.stdout, temp = StringIO(), sys.stdout
        result = making_a_slot.ask_for_date()
        answer = self.today_.split(" ")
        self.assertEqual(result,answer)
        sys.stdout = temp


    @patch('sys.stdin', StringIO(f"11:30\n"))
    def test_ask_for_time(self):
        sys.stdout, temp = StringIO(), sys.stdout
        result = making_a_slot.ask_for_time()
        self.assertEqual(result,'11:30')
        sys.stdout = temp


    @patch('sys.stdin', StringIO(f"{today_}\n08:00\n"))
    def test_call_date_time_check(self): #days_stored needed
        sys.stdout, temp = StringIO(), sys.stdout
        days_stored = mock_api.Mock_Service().events().list().execute()
        date_,start_date,end_date = making_a_slot.call_date_time_check(days_stored)
        self.assertEqual((date_,start_date,end_date),(today_))
        sys.stdout = temp



    def test_check_available_slots(self): #booked_slots, days_stored needed
        pass