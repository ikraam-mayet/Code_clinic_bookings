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
        edited_event = psb.generate_new_guest_summary(mock_api.Mock_Service(), test_event)

        new_summary = edited_event['summary']
        expected_summary = 'Did you find the easter egg? // easy-life session.'
        self.assertTrue(new_summary == expected_summary)

        sys.stdout = temp

    @patch('sys.stdin', StringIO('easy-life\n'))
    def test_generate_new_guest(self):
        sys.stdout, temp = StringIO(), sys.stdout

        test_event = mock_api.Mock_Events().events['items'][0]
        edited_event = psb.generate_new_guest_summary(mock_api.Mock_Service(), test_event)

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
        edited_event = psb.generate_new_guest_summary(mock_api.Mock_Service(), test_event)

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

        self.assertTrue(psb.generate_new_guest_summary(mock_api.Mock_Service(),
        {'attendees': [1, 2, 3]}) == None)

        sys.stdout.seek(0)
        lines = sys.stdout.readlines()
        self.assertTrue('Slot fully booked.\n' in lines[0])

        sys.stdout = temp


if __name__ == "__main__":
    unittest.main()
