import sys
import unittest
import datetime
from io import StringIO
from tests import mock_api
from unittest.mock import patch
from data.patient import cancel_patient_booking as cpb


class test_cancel_patient_booking(unittest.TestCase):

    expected_date = datetime.date.today()
    today_ = expected_date.strftime('%d %B %Y')

    event = mock_api.Mock_Events().events['items'][0]
    event['attendees'].append({'email': 'yahneh@test.co.za'})


    @patch('sys.stdin', StringIO(f"Easteregg // found\n{today_}\n08:00\n"))
    def test_patient_cancel_slot(self):
        sys.stdout, temp = StringIO(), sys.stdout
        self.maxDiff = None
        event_four = {'kind': 'test#event', 'etag': '"try-hard-101"',
        'id': '0mlugf7j95b8_20201116T956841Z', 'status': 'confirmed',
        'htmlLink': 'https://www.test.co.za/calendar/event?eid=wEStilLDontExist',
        'created': '2020-10-24T09:01:58.000Z', 'updated': '2020-10-24T09:03:27.846Z',
        'summary': 'Easteregg // found', 'creator': {'email': 'tryharders@wannabees.wedonotthinkcodesincewedontexist.co.za', 'self': True},
        'organizer': {'email': 'tryharders@wannabees.wedonotthinkcodesincewedontexist.co.za', 'self': True},
        'start': {'dateTime': datetime.date.today().strftime("%Y-%m-%dT08:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'end': {'dateTime': datetime.date.today().strftime("%Y-%m-%dT09:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'attendees': [{'email': 'send@help.co.za'},{'email': 'IamHereTo@help.co.za'}],
        'recurringEventId': '0mlugf7j95b8_20201116T060000Z',
        'originalStartTime': {'dateTime': '2020-11-16T08:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'iCalUID': '0mlugf7j95b8_20201116T060000Z@google.com', 'sequence': 0, 
        'reminders': {'useDefault': True}}

        result = cpb.patient_cancel_slot(mock_api.Mock_Service(),event_four)
        answer = {'kind': 'test#event', 'etag': '"try-hard-101"',
        'id': '0mlugf7j95b8_20201116T956841Z', 'status': 'confirmed', 
        'htmlLink': 'https://www.test.co.za/calendar/event?eid=wEStilLDontExist',
        'created': '2020-10-24T09:01:58.000Z', 'updated': '2020-10-24T09:03:27.846Z',
        'summary': 'Easteregg', 'creator': {'email': 'tryharders@wannabees.wedonotthinkcodesincewedontexist.co.za',
        'self': True}, 'organizer': {'email': 'tryharders@wannabees.wedonotthinkcodesincewedontexist.co.za', 'self': True},
        'start': {'dateTime': datetime.date.today().strftime("%Y-%m-%dT08:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'end': {'dateTime': datetime.date.today().strftime("%Y-%m-%dT09:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'attendees': [{'email': 'send@help.co.za'}], 'recurringEventId': '0mlugf7j95b8_20201116T060000Z',
        'originalStartTime': {'dateTime': '2020-11-16T08:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'iCalUID': '0mlugf7j95b8_20201116T060000Z@google.com', 'sequence': 0,
         'reminders': {'useDefault': True}}
        self.assertEqual(result, answer)

        sys.stdout = temp
