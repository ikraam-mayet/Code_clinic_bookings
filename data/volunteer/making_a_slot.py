from datetime import datetime, timedelta, date


def ask_for_date():
    while True:
        try :
            date_ = input('Please enter a date i.e 07 November 2020: ').split()
        except KeyError:
            continue
        if len(date_) != 3:
            continue
        else:
            break
    return date_


def ask_for_time():

    while True:
        time_ = input("please enter time i.e 11:30: ")
        if len(time_) == 5:
            return time_
        else: continue


def call_date_time_check(days_stored):
    while True:
        date_ = ask_for_date()

        time_ = ask_for_time()

        year, month, day = int(date_[2]), datetime.strptime(date_[1], '%B').month, int(date_[0])
        start_date = datetime(year, month, day, hour=int(time_.split(':')[0]), minute=int(time_.split(':')[1]))
        end_date = start_date + timedelta(minutes=90)

        if (start_date.day - date.today().day > days_stored):
            print("Out of range. Please select a slot within the stored days.")
            continue
        else:
            return date_, start_date, end_date


def check_available_slots(booked_slots, days_stored):
    while True:
        date_ ,start_date, end_date = call_date_time_check(days_stored)

        start_time = start_date.time()
        end_time = end_date.time()
        
        for booked_slot in booked_slots[' '.join(date_)]:

            starts_in_booked_slot = (start_time >= booked_slot[0] and start_time < booked_slot[1]) # bool. True if start time is in an already booked slot
            ends_in_booked_slot = (end_time > booked_slot[0] and end_time <= booked_slot[1]) # bool. True if end time is in an already booked slot
            if starts_in_booked_slot or ends_in_booked_slot:
                print("Slot booked. Try another date/time.")
                continue
        return volunteer(start_date)
    

def create_event(start_date,end_date, summary, description):
    """
    Book a time at the date and time given.
    Generate an event between the start and end date.
    Set notifications to an email 1 hour before and a pop up 10 minutes before.
    """   

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Africa/Johannesburg',
            },
        'end': {
            'dateTime': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Africa/Johannesburg',
            },
        'attendees': [
                {'email' : 'group2codeclinic@gmail.com'}
        ],
        'params' : {
            'sendNotifications' : True
            },
        'reminders': {
            'useDefault': False,
            'overrides' : [
                {'method':'email', 'minutes':60},
                {'method': 'popup', 'minutes':10}
            ]
        }
    }
    return event


def volunteer(start_date):
    summary = input("Username: ")
    description = input("What topic do you want to volunteer for: ")
    # max_time = timedelta(minutes=30)
    event_slots = list()

    # start = start_time
    # start = str(date_[0]) + ' '+ str(date_[1]) + ' '+ str(date_[2]) + ' '+str(start_time)

    for i in range(3):
        # start = datetime.strptime(str(start), '%Y-%m-%dT%H:%M:%S')
        # start = str(start)
        # start = start[11:]
        # end = datetime.strptime(str(start), '%Y-%m-%dT%H:%M:%S') + timedelta(minutes = 30)
        # end = str(end)
        # end = end[11:]
        end_date = start_date + timedelta(minutes=30)
        events = create_event(start_date, end_date, summary, description)
        event_slots.append(events)
        start_date = end_date
        # start = datetime.strptime(str(start), '%Y-%m-%dT%H:%M:%S') + timedelta(minutes = 30)
        
    return event_slots

