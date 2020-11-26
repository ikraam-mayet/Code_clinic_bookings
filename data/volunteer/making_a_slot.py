from authentication import authenticate
from data import create_data
from data import display_calendar
import os
import sys
from datetime import datetime, timedelta, date


def check_available_slots(booked_slots, days_stored):
    while True:
        try :
            date_ = input('Please enter a date i.e 07 November 2020: ').split()
        except KeyError:
            continue
        if len(date_) != 3:
            continue
        else:
            break

    time_ = input("please enter time i.e 11:30: ")

    year, month, day = int(date_[2]), datetime.strptime(date_[1], '%B').month, int(date_[0])
    start_date = datetime(year, month, day, hour=int(time_.split(':')[0]), minute=int(time_.split(':')[1]))
    end_date = start_date + timedelta(minutes=90)

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
    return volunteer(start_time)
    

def volunteer(start_time):
    summary = input("Username: ")
    description = input("What topic do you want to volunteer for: ")
    timezone = 'Africa/Johannesburg'
    max_time = timedelta(minutes=30)
    event_slots = list()


    for i in range(3):
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': (start_time + max_time * i).strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': timezone,
            },
            'end': {
                'dateTime': (start_time + max_time * (i+1)).strftime("%Y-%m-%dT%H:%M:%S"), 
                'timeZone': timezone,
            },
            'attendees' : {
                {'email' : 'group2codeclinic@gmail.com'}
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
        event_slots.append(event)
    
        return event