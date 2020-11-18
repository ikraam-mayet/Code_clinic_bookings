import csv
from authentication import authenticate
from data import create_data
from data import display_calendar
import sys

booked_slots = dict() # the booked slots, stored as {'Day 1': [[start time 1, end time 1], [start time 2, end time 2]]}
days_to_store = input("Please enter an integer for the number of days to store. \n0 will store today only, negative integers will store nothing: ")

# def main_function():
#     global booked_slots

#     credits_file = authenticate.open_create_credits_file()
#     service_obj = authenticate.authenticate_user(credits_file)
#     booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data. 0 returns today only, a negative returns no days
#     print(display_calendar.display_cal('events.csv'))
#     create_data.show_events() # show the currently stored events
#     booked_slots = create_data.book_event(service_obj, int(days_to_store), booked_slots)
#     print(display_calendar.display_cal('events.csv'))


def viewing_of_calendar(src_fn):
    try:
        return display_calendar.display_cal(src_fn)

    except FileNotFoundError:
        credits_file = authenticate.open_create_credits_file()
        service_obj = authenticate.authenticate_user(credits_file)
        booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data.
                                                                                      # 0 returns today only, a negative returns no days
        return print(display_calendar.display_cal(src_fn))


def patient_booking():
    credits_file = authenticate.open_create_credits_file()
    service_obj = authenticate.authenticate_user(credits_file)
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data.
                                                                                  # 0 returns today only, a negative returns no days
    booked_slots = create_data.book_event(service_obj, int(days_to_store), booked_slots)
    viewing_of_calendar('events.csv')

if __name__ == "__main__":
    if sys.argv[1] == 'view_calendar':
        viewing_of_calendar('events.csv')

    elif sys.argv[1] == 'patient':
        patient_booking()
