from datetime import datetime, time, date, timedelta

def volunteer_slot(booked_slots, days_stored):
    """
    Prompts user for a date and time to book a slot. 

    Uses the given time and increments it by 30 minutes. 
    If any part of the proposed slot falls within a booked slot, print booked.
    Otherwise create an event in that slot.
    """

    while True:
        try :
            date_ = input('Please enter a date i.e 07 November 2020: ').split()
        except KeyError:
            continue
        if len(date_) != 3:
            continue
        else:
            break


    time_ = input('Please enter a time i.e 11:30: ')


    year, month, day = int(date_[2]), datetime.strptime(date_[1], '%B').month, int(date_[0])
    start_date = datetime(year, month, day, hour=int(time_.split(':')[0]), minute=int(time_.split(':')[1]))
    end_date = start_date + timedelta(minutes=30)

    if (start_date.day - date.today().day > days_stored):
        print("Out of range. Please select a slot within the stored days.")
        return None

    start_time = start_date.time()
    end_time = end_date.time()

    for booked_slot in booked_slots[' '.join(date_)]:
        starts_in_booked_slot = (start_time >= booked_slot[0] and start_time < booked_slot[1]) # bool. True if start time is in an already booked slot
        ends_in_booked_slot = (end_time >= booked_slot[0] and end_time < booked_slot[1]) # bool. True if end time is in an already booked slot
        if starts_in_booked_slot or ends_in_booked_slot:
            print("Slot booked. Try another date/time.")
            return None
    return create_event(start_date, end_date)

def create_event(start_date, end_date):
    """
    Book a time at the date and time given.

    Generate an event between the start and end date.
    Set notifications to an email 1 hour before and a pop up 10 minutes before.
    """   

    event = {
        'summary': input('Summary/Event name: '),
        'description': input('Event description: '),
        'start': {
            'dateTime': start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Africa/Johannesburg',
            },
        'end': {
            'dateTime': end_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Africa/Johannesburg',
            },
        # 'attendees': [
        #     ],
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
