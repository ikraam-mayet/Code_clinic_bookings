import os
import sys
import pickle
import unittest
from io import StringIO
from unittest.mock import patch
from data import create_data
from data import display_calendar
import app

""" Need to do the other unittest """

class test_app(unittest.TestCase):


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