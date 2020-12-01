import os
import sys
from authentication import authenticate
from data import create_data
from data import display_calendar
from data.volunteer import making_a_slot
from data.patient import patient_slot_booking

booked_slots = dict() # the booked slots, stored as {'Day 1': [[start time 1, end time 1], [start time 2, end time 2]]}
days_to_store = ''


def store_days():
    global days_to_store
    days_to_store = input("Please enter an integer for the number of days to store. \n0 will store today only, negative integers will store nothing: ")


def user_viewing_of_calendar(src_fn):
    try:
        return display_calendar.display_cal(src_fn)

    except FileNotFoundError:
        credits_file = authenticate.open_create_credits_file()
        service_obj = authenticate.authenticate_user(credits_file)
        booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data.
                                                                                      # 0 returns today only, a negative returns no days
        return display_calendar.display_cal(src_fn)


def clinic_calendar(src_fn):
    try:
        return display_calendar.display_cal(src_fn)

    except FileNotFoundError:
        credits_file = authenticate.open_create_credits_file()
        service_obj = authenticate.authenticate_user(credits_file)
        booked_slots = create_data.get_clinics_cal(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data.
                                                                                      # 0 returns today only, a negative returns no days
        return display_calendar.display_cal(src_fn)


def patient_booking():
    global booked_slots, days_to_store

    print(clinic_calendar('calendar_events.csv'))
    delete_events('calendar_events.csv')

    credits_file = authenticate.open_create_credits_file()
    service_obj = authenticate.authenticate_user(credits_file)
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj)
    delete_events('events.csv')

    patient_slot_booking.patient_book_slot(service_obj, booked_slots)


def volunteer():
    global booked_slots, days_to_store

    credits_file = authenticate.open_create_credits_file()
    service_obj = authenticate.authenticate_user(credits_file)
    print(user_viewing_of_calendar('events.csv'))
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data. 
                                                                                  #0 returns today only, a negative returns no days
    generated_events = making_a_slot.check_available_slots(booked_slots,int(days_to_store)) # first arg is the number of days not including today to add to the data.
                                                                                        # 0 returns today only, a negative returns no days
    for event in generated_events:
        booked_slots = create_data.book_event(service_obj, int(days_to_store), event)
    print(user_viewing_of_calendar('events.csv'))


def authentication():
    credits_file = authenticate.open_create_credits_file()
    service_obj = authenticate.authenticate_user(credits_file)


def patient_cancellation():
    pass


def volunteer_cancellation():
    pass


def delete():
    try:
        user_home = os.path.expanduser('~')
        os.remove(f"{user_home}/.credentials.pkl")
        print('Credentials file deleted')

    except FileNotFoundError:
        print('Credentials file deleted')


def help_func():
    return"""usage: python3  app.py    help
               <command> [<args>]
        
These are the code-clinic commands that can be used in various situations:

setup and login:
        authenticate        creates login details and uses your calendar
        delete              deletes login details so new user can use calendar

View calendar:
        view_calendar       displays users calendar
        clinic_calendar     displays code clinics calendar

Booking:
        patient             Patient can book a volunteer for help
        volunteer           Volunteer can make slots for patients to help

Cancelation:
        patient_cal         Used for patient to cancel their booking
        volunteer_cal       Used for volunteer to cancel their volunteering if no one has booked them
"""


def delete_events(src_file):
    os.remove(src_file)


def main_function():
    global booked_slots, days_to_store

    if len(sys.argv) != 2:
        print(help_func())

    elif sys.argv[1] == 'view_calendar':
        store_days()
        print(user_viewing_of_calendar('events.csv'))
        delete_events('events.csv')

    elif sys.argv[1] =='clinic_calendar':
        store_days()
        print(clinic_calendar('calendar_events.csv'))
        delete_events('calendar_events.csv')

    elif sys.argv[1] == 'patient':
        store_days()
        patient_booking()
        print(user_viewing_of_calendar('events.csv'))
        delete_events('events.csv')

    elif sys.argv[1] == 'volunteer':
        store_days()
        volunteer()
        print(user_viewing_of_calendar('events.csv'))
        delete_events('events.csv')

    elif sys.argv[1] == 'authenticate':
        authentication()

    elif sys.argv[1] ==  'volunteer_cal':
        volunteer_cancellation()

    elif sys.argv[1] == 'patient_cal':
        patient_cancellation()

    elif sys.argv[1] == 'delete':
        delete()

    else:
        print(help_func())


if __name__ == "__main__":
    main_function()  
