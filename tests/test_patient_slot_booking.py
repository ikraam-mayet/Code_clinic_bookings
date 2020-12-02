import sys
import unittest
import datetime
from io import StringIO
from tests import mock_api
from unittest.mock import patch
from data.patient import patient_slot_booking as psb


class Test_Booking(unittest.TestCase):

    expected_date = datetime.date.today()
    today_ = expected_date.strftime('%d %B %Y')

    @patch('sys.stdin', StringIO(f"Did you find the easter egg?\n{today_}\n08:00\nperson\n"))
    def test_patient_book_slot(self):
        sys.stdout, temp = StringIO(), sys.stdout

        ret_event = psb.patient_book_slot(mock_api.Mock_Service(), {})
        expected_attendees_list = [{'email': 'send@help.co.za'},
        {'email': 'person@student.wethinkcode.co.za', 'responseStatus': 'accepted'}]

        self.assertTrue("Did you find the easter egg? // person session." == ret_event['summary'])
        self.assertEqual(ret_event['attendees'], expected_attendees_list)
        sys.stdout = temp

    @patch('sys.stdin', StringIO('easy-life\n'))
    def test_generate_new_summary(self):
        sys.stdout, temp = StringIO(), sys.stdout

        test_event = mock_api.Mock_Events().events['items'][0]
        edited_event = psb.generate_new_guest_summary(test_event)

        new_summary = edited_event['summary']
        expected_summary = 'Did you find the easter egg? // easy-life session.'
        self.assertTrue(new_summary == expected_summary)

        sys.stdout = temp

    @patch('sys.stdin', StringIO('easy-life\n'))
    def test_generate_new_guest(self):
        sys.stdout, temp = StringIO(), sys.stdout

        test_event = mock_api.Mock_Events().events['items'][0]
        edited_event = psb.generate_new_guest_summary(test_event)

        new_guests = edited_event['attendees']
        expected_guest_list = [{'email': 'send@help.co.za'},
        {'email': 'easy-life@student.wethinkcode.co.za',
        'responseStatus': 'accepted'}]

        self.assertTrue(new_guests == expected_guest_list)

        sys.stdout = temp

    @patch('sys.stdin', StringIO('easy-life\n'))
    def test_generate_new_guest_no_attendees(self):
        sys.stdout, temp = StringIO(), sys.stdout

        test_event = mock_api.Mock_Events().events['items'][2]
        edited_event = psb.generate_new_guest_summary(test_event)

        new_guests = edited_event['attendees']
        expected_guest_list = [{'email': 'easy-life@student.wethinkcode.co.za',
        'responseStatus': 'accepted'},
        {'email': 'group2codeclinic@gmail.com',
        'self': True, 'responseStatus': 'accepted'}]

        self.assertTrue(new_guests == expected_guest_list)

        sys.stdout = temp

    @patch('sys.stdin', StringIO('easy-life\n'))
    def test_generate_new_guest_summary_full(self):
        sys.stdout, temp = StringIO(), sys.stdout

        self.assertRaises(SystemExit, psb.generate_new_guest_summary,
        {'attendees': [1, 2, 3]})

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('Slot fully booked.\n' in lines[0])

        sys.stdout = temp

    def test_get_matching_events_match_found(self):
        service = mock_api.Mock_Service()
        match = psb.get_matching_events(service, 'THIs eVeNt toTAlly happened')

        self.assertTrue(len(match) == 1)
        self.assertTrue(type(match[0]) is dict)
        self.assertTrue(match[0]['summary'] == 'This event totally happened')

    def test_get_matching_events_match_not_found(self):
        sys.stdout, temp = StringIO(), sys.stdout
        service = mock_api.Mock_Service()

        self.assertRaises(SystemExit, psb.get_matching_events, service, 'Nope')

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()       
        self.assertTrue('Event not found.\n' in lines)

        sys.stdout = temp

    @patch('sys.stdin', StringIO(f"{today_}\n08:00\n"))
    def test_get_date_time_correct_available(self):
        sys.stdout, temp = StringIO(), sys.stdout

        times = [[datetime.time(hour=1), datetime.time(hour=2)]]
        date_str, time_ = psb.get_date_time({f"{self.today_}": times})
        
        self.assertTrue(date_str == self.today_)
        self.assertTrue(time_ == datetime.time(hour=8))

        sys.stdout = temp

    @patch('sys.stdin', StringIO(f"{today_}\n08:00\n"))
    def test_get_date_time_correct_booked(self):
        sys.stdout, temp = StringIO(), sys.stdout

        times = [[datetime.time(hour=8), datetime.time(hour=9)]]
        
        self.assertRaises(SystemExit, psb.get_date_time, {f"{self.today_}": times})

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('Slot blocked in your personal calendar.\n' in lines[0])

        sys.stdout = temp

    @patch('sys.stdin', StringIO('1/12/2020\n08:00\n'))
    def test_get_date_time_wrong_date_format(self):
        sys.stdout, temp = StringIO(), sys.stdout

        self.assertRaises(SystemExit, psb.get_date_time, {})

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('Please enter the correct time and date formats.\n' in lines[0])

        sys.stdout = temp

    @patch('sys.stdin', StringIO(f"{today_}\nTyd\n"))
    def test_get_date_time_wrong_time_format(self):
        sys.stdout, temp = StringIO(), sys.stdout

        self.assertRaises(SystemExit, psb.get_date_time, {})

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('Please enter the correct time and date formats.\n' in lines[0])

        sys.stdout = temp

    def test_get_final_event_no_result_found(self):
        sys.stdout, temp = StringIO(), sys.stdout

        self.assertRaises(SystemExit, psb.get_final_event, [], datetime.time(hour=15), '01 December 2020')

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
