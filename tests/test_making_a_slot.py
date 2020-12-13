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


    def test_create_event(self):

        answer = self.today_.split(" ")
        year, month, day = int(answer[2]), datetime.datetime.strptime(answer[1], '%B').month, int(answer[0])
        start_date = datetime.datetime(year, month, day, hour=int(self.time_.split(':')[0]), minute=int(self.time_.split(':')[1]))
        end_date = start_date + datetime.timedelta(minutes=30)
        summary = 'imayet'
        student_email  = summary + '@student.wethinkcode.co.za'
        description = 'everything'

        result = making_a_slot.create_event(start_date,end_date,summary,description,student_email)

        answer = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Africa/Johannesburg',
                },
            'end': {
                'dateTime': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
                'timeZone': 'Africa/Johannesburg',
                },
            'attendees': [
                    {'email' : student_email}
            ],
            'params' : {
                'sendNotifications' : True
                },
            'reminders': {
                'useDefault': False,
                'overrides' : [
                    {'method':'email', 'minutes':60},
                    {'method': 'popup', 'minutes':10}
                ]
            }
        }

        self.assertEqual(result,answer)


    @patch('sys.stdin', StringIO(f"imayet\neverything"))
    def test_volunteer(self):

        answer = self.today_.split(" ")
        year, month, day = int(answer[2]), datetime.datetime.strptime(answer[1], '%B').month, int(answer[0])
        start_date = datetime.datetime(year, month, day, hour=int(self.time_.split(':')[0]), minute=int(self.time_.split(':')[1]))
        end_date = start_date + datetime.timedelta(minutes=30)
        summary = 'imayet'
        student_email  = summary + '@student.wethinkcode.co.za'
        description = 'everything'

        result = making_a_slot.volunteer(start_date)
        self.maxDiff = None
        event_slots = list()

        for i in range(3):
            end_date = start_date + datetime.timedelta(minutes=30)
            events = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Africa/Johannesburg',
            },
        'end': {
            'dateTime': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Africa/Johannesburg',
            },
        'attendees': [
                {'email' : student_email}
        ],
        'params' : {
            'sendNotifications' : True
            },
        'reminders': {
            'useDefault': False,
            'overrides' : [
                {'method':'email', 'minutes':60},
                {'method': 'popup', 'minutes':10}
            ]
        }
    }
            event_slots.append(events)
            start_date = end_date


        self.assertEqual(result,event_slots)