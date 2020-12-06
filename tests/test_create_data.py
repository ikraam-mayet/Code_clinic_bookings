import os
import unittest
from datetime import date, time, timedelta
import tests.mock_api as mock_api
from data.create_data import *
from unittest.mock import patch


class Test_Create_Data(unittest.TestCase):

    today = date.today().strftime("%d %B %Y")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%d %B %Y")
    one_hundred_days_later = (date.today() + timedelta(days=100)).strftime('%d %B %Y')
    
    def test_show_events(self):
        pass

    def test_store_next_n_days_return_today(self):
        # with patch('data.create_data.add_data') as mock_create_data
        slots_booked = store_next_n_days(0, mock_api.Mock_Service())

        self.assertTrue(self.today in slots_booked)
        self.assertEqual(time(hour=8), slots_booked[self.today][0][0])
        self.assertEqual(time(hour=9), slots_booked[self.today][0][1])

        self.assertTrue(self.tomorrow not in slots_booked)
        self.assertTrue(self.one_hundred_days_later not in slots_booked)

    def test_store_next_n_days_return_two_days(self):
        slots_booked = store_next_n_days(1, mock_api.Mock_Service())

        self.assertTrue(self.today in slots_booked)
        self.assertTrue(self.tomorrow in slots_booked)
        self.assertEqual(time(hour=8), slots_booked[self.today][0][0])
        self.assertEqual(time(hour=9), slots_booked[self.tomorrow][0][1])

        self.assertTrue(self.one_hundred_days_later not in slots_booked)

    def test_add_data_data_list(self):
        fake_events_dict = mock_api.Mock_Service().events().list().execute()

        data_list, _ = add_data(fake_events_dict, list(), dict())
        first_arg = ['Did you find the easter egg?', self.today, '08:00', self.today, '09:00']
        second_arg = ['This event totally happened', self.one_hundred_days_later, '18:00', self.one_hundred_days_later, '19:00']
        third_arg = ['UDUDLRLRBA', self.tomorrow, '08:00', self.tomorrow, '09:00']

        self.assertTrue(len(data_list) == 3)
        self.assertTrue(data_list[0] == first_arg)
        self.assertTrue(data_list[1] == second_arg)
        self.assertTrue(data_list[2] == third_arg)

    def test_add_data_booked_list(self):
        fake_events_dict = mock_api.Mock_Service().events().list().execute()

        _, booked_slots = add_data(fake_events_dict, list(), dict())
        first_arg = {self.today: [[time(hour=8), time(hour=9)]]}
        second_arg = {self.tomorrow: [[time(hour=8), time(hour=9)]]}
        third_arg = {self.one_hundred_days_later: [[time(hour=18), time(hour=19)]]}

        self.assertTrue(self.today in booked_slots)
        self.assertTrue(self.tomorrow in booked_slots)
        self.assertTrue(self.one_hundred_days_later in booked_slots)

        self.assertEqual(first_arg[self.today][0], booked_slots[self.today][0])
        self.assertEqual(second_arg[self.tomorrow][0], booked_slots[self.tomorrow][0])
        self.assertEqual(third_arg[self.one_hundred_days_later][0], booked_slots[self.one_hundred_days_later][0])

    def tests_complete(self):
        os.remove("events.csv")

if __name__ == "__main__":
    unittest.main()
