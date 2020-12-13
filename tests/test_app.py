import os
import sys
import pickle
import unittest
from io import StringIO
from unittest.mock import patch
from data import create_data
from data import display_calendar
import app
import datetime

""" Need to do the other unittest """

class test_app(unittest.TestCase):

    expected_date = datetime.date.today()
    today_ = expected_date.strftime('%d %B %Y')

    def test_user_viewing_of_calendar(self):
        src_fn= 'tests/test_event.csv'
        self.maxDiff = None
        result = app.user_viewing_of_calendar(src_fn)
        self.assertEqual(result,"""╒══════════════╤═══════════════╤══════════════╤══════════════╤════════════╤════════════╕
│ Event name   │ Description   │ Start Date   │ Start Time   │ End Date   │ End Time   │
╞══════════════╪═══════════════╪══════════════╪══════════════╪════════════╪════════════╡
│ \u001b[34mcol1         │ col2          │ col3         │ 1            │ 3          │ 4\u001b[0m          │
├──────────────┼───────────────┼──────────────┼──────────────┼────────────┼────────────┤
│ foo          │ 2             │ 5            │ bar          │ e          │ z          │
╘══════════════╧═══════════════╧══════════════╧══════════════╧════════════╧════════════╛""")


    @patch('sys.stdin', StringIO(f"5\n"))
    def test_store_days(self):
        sys.stdout, temp = StringIO(), sys.stdout

        result = app.store_days()
        self.assertEqual(result ,7)

    def test_delete_events(self):
        self.assertTrue('events.csv' not in sys.modules, "events module should not be found")


    def test_clinic_calendar(self):
        src_fn = 'tests/test_event.csv'
        result = app.clinic_calendar(src_fn)
        self.assertEqual(result,"""╒══════════════╤═══════════════╤══════════════╤══════════════╤════════════╤════════════╕
│ Event name   │ Description   │ Start Date   │ Start Time   │ End Date   │ End Time   │
╞══════════════╪═══════════════╪══════════════╪══════════════╪════════════╪════════════╡
│ \u001b[34mcol1         │ col2          │ col3         │ 1            │ 3          │ 4\u001b[0m          │
├──────────────┼───────────────┼──────────────┼──────────────┼────────────┼────────────┤
│ foo          │ 2             │ 5            │ bar          │ e          │ z          │
╘══════════════╧═══════════════╧══════════════╧══════════════╧════════════╧════════════╛""")


    def test_delete(self):
        result = app.delete()
        self.assertEqual(result , 'Credentials file deleted')


    def test_help(self):
        self.assertEqual(app.help_func(),"""usage: python3  app.py    help
               <command> [<args>]
        
These are the code-clinic commands that can be used in various situations:

setup and login:
        init                creates login details and uses your calendar
        delete              deletes login details so new user can use calendar

View calendar:
        -v                  displays users calendar
        -c                  displays code clinics calendar

Booking:
        patient             Patient can book a volunteer for help
        volunteer           Volunteer can make slots for patients to help

Cancelation:
        -p_cal              Used for patient to cancel their booking
        -v_cal             Used for volunteer to cancel their volunteering if no one has booked them
""")