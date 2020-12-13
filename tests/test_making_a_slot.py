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
    time_ = '11:30'


    @patch('sys.stdin', StringIO(f"{today_}\n"))
    def test_ask_for_date(self):
        sys.stdout, temp = StringIO(), sys.stdout
        result = making_a_slot.ask_for_date()
        answer = self.today_.split(" ")
        self.assertEqual(result,answer)
        sys.stdout = temp


    @patch('sys.stdin', StringIO(f"{time_}\n"))
    def test_ask_for_time(self):
        sys.stdout, temp = StringIO(), sys.stdout
        result = making_a_slot.ask_for_time()
        self.assertEqual(result,self.time_)
        sys.stdout = temp


    @patch('sys.stdin', StringIO(f"{today_}\n{time_}\n"))
    def test_call_date_time_check(self):
        sys.stdout, temp = StringIO(), sys.stdout
        result = making_a_slot.call_date_time_check(int(7))
        answer = self.today_.split(" ")
        self.maxDiff = None 
        year, month, day = int(answer[2]), datetime.datetime.strptime(answer[1], '%B').month, int(answer[0])
        start_date = datetime.datetime(year, month, day, hour=int(self.time_.split(':')[0]), minute=int(self.time_.split(':')[1]))
        end_date = start_date + datetime.timedelta(minutes=30)
        self.assertEqual(result, (answer, start_date, end_date))
        sys.stdout = temp


    @patch('sys.stdin', StringIO(f"{today_}\n11:30\n"))
    def test_check_available_slots(self): #booked_slots, days_stored needed
        sys.stdout, temp = StringIO(), sys.stdout
        # result = making_a_slot.check_available_slots()
        sys.stdout = temp