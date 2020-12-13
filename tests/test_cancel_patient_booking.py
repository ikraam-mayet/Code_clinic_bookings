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

    def test_patient_cancel_slot(self):
        pass
