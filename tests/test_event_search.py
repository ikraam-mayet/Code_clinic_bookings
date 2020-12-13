import sys
import unittest
import datetime
from io import StringIO
from tests import mock_api
from unittest.mock import patch
from data import event_search as psb


def compare_slots(*args):
    pass


def compare_slots_error(*args):
    print('Slot blocked in your personal calendar.')
    raise ValueError


class Test_Find_Event(unittest.TestCase):

    expected_date = datetime.date.today()
    today_ = expected_date.strftime('%d %B %Y')

    def test_get_matching_events_match_found(self):
        service = mock_api.Mock_Service()
        match = psb.get_matching_events(service, 'THIs eVeNt toTAlly happened')

        self.assertTrue(len(match) == 1)
        self.assertTrue(type(match[0]) is dict)
        self.assertTrue(match[0]['summary'] == 'This event totally happened')

    def test_get_matching_events_match_not_found(self):
        sys.stdout, temp = StringIO(), sys.stdout
        service = mock_api.Mock_Service()

        self.assertRaises(ValueError, psb.get_matching_events, service, 'Nope')

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()       
        self.assertTrue('Event not found.\n' in lines)

        sys.stdout = temp

    @patch('sys.stdin', StringIO(f"{today_}\n08:00\n"))
    def test_get_date_time_correct_available(self):
        sys.stdout, temp = StringIO(), sys.stdout

        times = [[datetime.time(hour=1), datetime.time(hour=2)]]
        date_str, time_ = psb.get_date_time({f"{self.today_}": times}, compare_slots)

        self.assertTrue(date_str == self.today_)
        self.assertTrue(time_ == datetime.time(hour=8))

        sys.stdout = temp

    @patch('sys.stdin', StringIO(f"{today_}\n08:00\n"))
    def test_get_date_time_correct_booked(self):
        sys.stdout, temp = StringIO(), sys.stdout

        times = [[datetime.time(hour=8), datetime.time(hour=9)]]

        self.assertRaises(ValueError, psb.get_date_time, {f"{self.today_}": times}, compare_slots_error)

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('Slot blocked in your personal calendar.\n' in lines[1])

        sys.stdout = temp

    @patch('sys.stdin', StringIO('1/12/2020\n08:00\n'))
    def test_get_date_time_wrong_date_format(self):
        sys.stdout, temp = StringIO(), sys.stdout

        self.assertRaises(ValueError, psb.get_date_time, {}, compare_slots)

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('Please enter the correct time and date formats.\n' in lines[1])

        sys.stdout = temp

    @patch('sys.stdin', StringIO(f"{today_}\nTyd\n"))
    def test_get_date_time_wrong_time_format(self):
        sys.stdout, temp = StringIO(), sys.stdout

        self.assertRaises(ValueError, psb.get_date_time, {}, compare_slots)

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('Please enter the correct time and date formats.\n' in lines[1])

        sys.stdout = temp

    def test_get_final_event_no_result_found(self):
        sys.stdout, temp = StringIO(), sys.stdout

        self.assertRaises(ValueError, psb.get_final_event, [], datetime.time(hour=15), '01 December 2020')

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('No event for the given date and time.\n' in lines[0])

        sys.stdout = temp

    def test_get_final_event_found(self):
        sys.stdout, temp = StringIO(), sys.stdout

        list_ = mock_api.Mock_Events().events['items']
        ret = psb.get_final_event(list_, datetime.time(hour=8), f"{self.today_}")
        self.assertEqual(ret, list_[0])

        sys.stdout = temp


if __name__ == "__main__":
    unittest.main()