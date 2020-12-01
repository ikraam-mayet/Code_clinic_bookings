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
        result = display_calendar.display_cal('tests/test_event.csv')
        self.assertEqual(result,"""╒══════════════╤══════════════╤══════════════╤════════════╤════════════╕
│ Event name   │ Start Date   │ Start Time   │ End Date   │ End Time   │
╞══════════════╪══════════════╪══════════════╪════════════╪════════════╡
│ col1         │ col2         │ col3         │ 1          │ 3          │
├──────────────┼──────────────┼──────────────┼────────────┼────────────┤
│ foo          │ 2            │ 5            │ bar        │ e          │
╘══════════════╧══════════════╧══════════════╧════════════╧════════════╛""")