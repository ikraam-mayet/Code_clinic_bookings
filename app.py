import csv
from authentication import authenticate
from data import create_data
from data import display_calender

booked_slots = dict() # the booked slots, stored as {'Day 1': [[start time 1, end time 1], [start time 2, end time 2]]}
days_to_store = input("Please enter an integer for the number of days to store \n0 will store today only, negatives will store nothing. ")

def main_function():
    global booked_slots

    credits_file = authenticate.open_create_credits_file()
    service_obj = authenticate.authenticate_user(credits_file)
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data. 0 returns today only, a negative returns no days
    create_data.show_events() # show the currently stored events
    booked_slots = create_data.book_event(service_obj, int(days_to_store), booked_slots)
    display_calender.display_cal()


if __name__ == "__main__":
    main_function()