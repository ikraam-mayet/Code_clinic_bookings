import os
import sys
import pickle
import unittest
from io import StringIO
from unittest.mock import patch
import csv
import re
from tabulate import tabulate
from data import display_calendar


THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class test_display_calendar(unittest.TestCase):


    def test_divide_chuncks(self):
        l = ['col1','col2','col3',1,3,'foo',2,5,'bar','e']
        result = display_calendar.divide_chunks(l,5)
        self.assertEqual(result,[['col1','col2','col3',1,3],['foo',2,5,'bar','e']])


    def test_display_cal(self):
        self.maxDiff = None
        result = display_calendar.display_cal('tests/test_event.csv')
        print(result)
        self.assertEqual(result,"""╒══════════════╤═══════════════╤══════════════╤══════════════╤════════════╤════════════╕
│ Event name   │ Description   │ Start Date   │ Start Time   │ End Date   │ End Time   │
╞══════════════╪═══════════════╪══════════════╪══════════════╪════════════╪════════════╡
│ \u001b[34mcol1         │ col2          │ col3         │ 1            │ 3          │ 4\u001b[0m          │
├──────────────┼───────────────┼──────────────┼──────────────┼────────────┼────────────┤
│ foo          │ 2             │ 5            │ bar          │ e          │ z          │
╘══════════════╧═══════════════╧══════════════╧══════════════╧════════════╧════════════╛""")


    def test_remove_attendees(self):
        data_list = [['Event name', 'Description', 'Start Date', 'Start Time', 'End Date', 'End Time','attendees'],['Event name', 'Description', 'Start Date', 'Start Time', 'End Date', 'End Time','attendees']]
        result = display_calendar.remove_attendees(data_list)
        self.assertEqual(result, [['Event name', 'Description', 'Start Date', 'Start Time', 'End Date', 'End Time'],['Event name', 'Description', 'Start Date', 'Start Time', 'End Date', 'End Time']])