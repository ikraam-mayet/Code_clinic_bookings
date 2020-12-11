import sys
import unittest
import datetime
from io import StringIO
from tests import mock_api
from unittest.mock import patch
from data import create_data
from data.patient import cancel_patient_booking

class test_cancel_patient_booking(unittest.TestCase):
    
    expected_date = datetime.date.today()
    today_ = expected_date.strftime('%d %B %Y')

    @patch('sys.stdin', StringIO(f"'Maybe I found the easter egg'?\n{today_}\n08:00\nperson\n"))
    def test_patient_cancel_slot(self):
        pass


    def test_generate_new_guest_summary(self):
        pass


    def test_get_matching_events(self):
        # creator = 'tryharders@wannabees.wedonotthinkcodesincewedontexist.co.za'

        pass


    @patch('sys.stdin', StringIO(f"{today_}\n08:00\n"))
    def test_get_date_time(self):
        sys.stdout, temp = StringIO(), sys.stdout

        times = [[datetime.time(hour=1), datetime.time(hour=2)]]
        date_str, time_ = cancel_patient_booking.get_date_time({f"{self.today_}": times})
        self.assertTrue(date_str == self.today_)
        self.assertTrue(time_ == datetime.time(hour=8))

        sys.stdout = temp


    def test_get_final_event(self):
        fake_events_dict = mock_api.Mock_Service().events().list().execute()
        data_list, _ = create_data.add_data(fake_events_dict, list(), dict())
        matches = data_list
        date_str =self.today_
        time_ = datetime.time(hour=8)
        result = cancel_patient_booking.get_final_event(matches,date_str, time_)
        self.assertEqual(result,matches)


    def test_compare_slots(self):

        fake_events_dict = mock_api.Mock_Service().events().list().execute()
        data_list, _ = create_data.add_data(fake_events_dict, list(), dict())
        start = datetime.date.today().strftime("%Y-%m-%dT08:00:00")
        end = datetime.date.today().strftime("%Y-%m-%dT09:00:00")
        result = cancel_patient_booking.compare_slots(data_list[1],start,end)
        self.assertTrue(result)