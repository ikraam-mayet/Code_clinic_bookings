from datetime import datetime, timedelta, date


def ask_for_date():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
    'August', 'September', 'October', 'November', 'December']
    while True:
        try :
            date_ = input('Please enter a date i.e 07 November 2020: ').split()
        except KeyError:
            continue
        date_[1] = date_[1][0].upper() + date_[1][1:].lower()
        if len(date_) != 3 or len(date_[0]) != 2 or not date_[1] in months or len(date_[2]) != 4:
            continue
        else:
            break
    return date_


def ask_for_time():

    while True:
        time_ = input("please enter time i.e 11:30: ")
        if len(time_) == 5 and ':' in time_:
            time_ = time_.split(':', 1)
            if len(time_[0]) == 2  and len(time_[1]) == 2:
                return ':'.join(time_)
        else: continue


def call_date_time_check(days_stored):
    while True:
        date_ = ask_for_date()

        time_ = ask_for_time()
        year, month, day = int(date_[2]), datetime.strptime(date_[1], '%B').month, int(date_[0])
        start_date = datetime(year, month, day, hour=int(time_.split(':')[0]), minute=int(time_.split(':')[1]))
        end_date = start_date + timedelta(minutes=30)
        # print(start_date.day, days_stored)
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
        # print(booked_slots, str(start_time))
        for booked_slot in booked_slots[' '.join(date_)]:
            starts_in_booked_slot = (start_time >= booked_slot[0] and end_time <= booked_slot[1]) 
            if starts_in_booked_slot:
                print("Slot booked. Try another date/time.")
                return check_available_slots( booked_slots,days_stored)
        return volunteer(start_date)
    

def create_event(start_date,end_date, summary, description, student_email):
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
                {'email' : student_email}
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
    user_email  = summary + '@student.wethinkcode.co.za'
    description = input("What topic do you want to volunteer for: ")
    event_slots = list()

    for i in range(3):
        end_date = start_date + timedelta(minutes=30)
        events = create_event(start_date, end_date, summary, description,user_email)
        event_slots.append(events)
        start_date = end_date    
    return event_slots