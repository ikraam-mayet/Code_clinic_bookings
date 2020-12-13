import os
import sys
from authentication import authenticate
from data import create_data
from data import display_calendar
from data.volunteer import making_a_slot
from data.patient import patient_slot_booking
from data.volunteer import cancel_slot
from data.patient import cancel_patient_booking

booked_slots = dict() # the booked slots, stored as {'Day 1': [[start time 1, end time 1], [start time 2, end time 2]]}
days_to_store = ''


def store_days():
    """
    Ask's user for the amount of days to be stored to be displayed.
    If an int isn't entered 
    """
    global days_to_store

    if not sys.stdout.isatty():
        days_to_store = 7
        return days_to_store
            
    while True:
        try:
            days_to_store = int(input("Please enter an integer for the number of days to store. \n0 will store today only, negative integers will store nothing: "))
            days_to_store = days_to_store if days_to_store < 15 else 15
            return days_to_store
        except ValueError:
            print("\nInteger was not entered correctly.\nTry again.\n")
            continue


def delete_events(src_file):
    os.remove(src_file)


def user_viewing_of_calendar(src_fn):
    """
    Param:
     - src_fn - the source file to be displayed
    Displays the users calendar based of the paramater being inputted. If the file 
    doesn't exits it created the file again based of the authentication and 
    amount of days to be displayed.
    """
    global booked_slots

    try:
        return display_calendar.display_cal(src_fn)

    except FileNotFoundError:
        service_obj = authentication()
        booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data.
                                                                                      # 0 returns today only, a negative returns no days
        return display_calendar.display_cal(src_fn)


def clinic_calendar(src_fn):
    """
    param:
    -- src_fn - is the calendar .csv file to be displayed

    Gets the clinic file data to be displayed and call the function to be 
    displayed. if the file doesn't exist it recreated the file based on how 
    many days to be displayed.
    """
    global booked_slots 

    try:
        return display_calendar.display_cal(src_fn)

    except FileNotFoundError:
        service_obj = authentication()
        booked_slots = create_data.get_clinics_cal(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data.
                                                                                      # 0 returns today only, a negative returns no days
        return display_calendar.display_cal(src_fn)


def patient_booking():
    """  
    For patient to book an event that someone has volunteered their help on a 
    topic.
    Displays the clinics calendar of all the slots, the clinic's data file is 
    then deleted. Authentication is then run to make sure the user is loggen in 
    calls the api to populate all the events, it deletes the users events so 
    that it can be updated if it is displayed again.
    """
    global booked_slots, days_to_store

    print(clinic_calendar('calendar_events.csv'))
    delete_events('calendar_events.csv')

    service_obj = authentication()
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj)
    delete_events('events.csv')

    return patient_slot_booking.patient_book_slot(service_obj, booked_slots)


def volunteer():
    """ 
    Lets a volunteer volunter their help on a specific topic for 90 mins, split 
    into 3 30 mins events.
    Authenticates the user, then displays the users calendar. It collects the 
    user's booked events for the period the user inputted then allows the 
    user to book an event during the free time in the clinics and user's 
    calendar. After that the users calendar is displayed.
    """
    global booked_slots, days_to_store

    service_obj = authentication()
    print(user_viewing_of_calendar('events.csv'))
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj) # first arg is the number of days not including today to add to the data. 
                                                                                  #0 returns today only, a negative returns no days
    generated_events = making_a_slot.check_available_slots(booked_slots,int(days_to_store)) # first arg is the number of days not including today to add to the data.
                                                                                        # 0 returns today only, a negative returns no days
    for event in generated_events:
        booked_slots = create_data.book_event(service_obj, int(days_to_store), event)
    delete_events('events.csv')
    print('\nUsers Calendar:')
    print(user_viewing_of_calendar('events.csv'))


def authentication():
    """  
    Authenticates the user
    Allows the user to login into their google account, then stores the data in 
    a hidden file in the home directory
    """
    credits_file = authenticate.open_create_credits_file()
    service_obj = authenticate.authenticate_user(credits_file)
    return service_obj


def patient_cancellation():
    """  
    Allows the patient to cancel their patient booking.
    The clinic's calendar is displayed and the stored data of the clinic is 
    deleted. The user is the authenticated and the events of their calendar is 
    stored then asks the user for which event they want to cancel
    """
    global booked_slots, days_to_store

    print(clinic_calendar('calendar_events.csv'))
    delete_events('calendar_events.csv')

    service_obj = authentication()
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj)
    cancel_patient_booking.patient_cancel_slot(service_obj, booked_slots)


def volunteer_cancellation():
    """  
    Allows the volunteer to cancel their volunteering if their is no patient.
    The user is authenticated and their calendar data is stored depending on the 
    days they inputted to display. Their calendar is then displayed and the 
    process of cancelling an event begins. The new events is stored and their 
    calendar is displayed.
    """
    global booked_slots, days_to_store

    service_obj = authentication()
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj)
    print(user_viewing_of_calendar('events.csv'))
    print(cancel_slot.calling_of_cancelations_function(service_obj, booked_slots,service_obj))
    booked_slots = create_data.store_next_n_days(int(days_to_store), service_obj)
    delete_events('events.csv')
    print(user_viewing_of_calendar('events.csv'))
    

def delete():
    """  
    The user's credentials gets deleted. If the credentials doesn't exist it 
    displays that the credenttials have been deleted 
    """
    try:
        user_home = os.path.expanduser('~')
        os.remove(f"{user_home}/.credentials.pkl")
        return ('Credentials file deleted')

    except FileNotFoundError:
        return ('Credentials file deleted')


def help_func():
    """
    The details on how the program is run. The help function.
    """
    return"""usage: python3  app.py    help
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
"""


def main_function():
    """  
    The main function that runs the program
    """
    global booked_slots, days_to_store

    if len(sys.argv) != 2 and sys.stdout.isatty():
        print(help_func())

    elif sys.argv[1] == '-v':
        store_days()
        print(user_viewing_of_calendar('events.csv'))
        delete_events('events.csv')

    elif sys.argv[1] =='-c':
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
        print("\nCode clinics calendar: ")
        print(clinic_calendar('calendar_events.csv'))
        delete_events('calendar_events.csv')
        delete_events('events.csv')

    elif sys.argv[1] == 'init':
        authentication()

    elif sys.argv[1] ==  '-v_cal':
        store_days()
        volunteer_cancellation()
        delete_events('events.csv')

    elif sys.argv[1] == '-p_cal':
        store_days()
        patient_cancellation()

    elif sys.argv[1] == 'delete':
        print(delete())

    else:
        print(help_func())


if __name__ == "__main__":
    main_function()  
