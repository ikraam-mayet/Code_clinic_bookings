import csv
from data.volunteer import making_a_slot
from datetime import date, timedelta
from data.format_data import *
import data.display_calendar as display_calender
import googleapiclient.errors as errors

data_list = []


def show_events():
    """
    This functions calls the display_cal function from display_calender to 
    display the calender
    """
    display_calender.display_cal('events.csv')

def store_next_n_days(n, service_obj):
    global data_list

    booked_slots = dict()

    # set current and end date to be downloaded, use n as the difference between today and the end date
    current_date = str(date.today()) + 'T00:00:00.000Z'
    end_date = str(date.today() + timedelta(days=int(n))) + 'T23:59:00.000Z'

    # get the user calendar's events in the given period, sorted by start time (ascending), recurring events repeated as they happen
    calend = service_obj.events().list(calendarId='primary', timeMin=current_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()

    # store data into memory in lists. Each list uses the format below
    header_list = ['Event name', 'Start Date', 'Start Time', 'End Date', 'End Time']

    data_list = []
    data_list, booked_slots = add_data(calend, data_list, booked_slots)
    write_to_csv(header_list, data_list, 'events.csv')

    # # add the code clinic calendar's events in the time period if the calendar is connected to the user's account
    # try:
    #     data_list.clear()
    #     calend = service_obj.events().list(calendarId='group2codeclinic@gmail.com', timeMin=current_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    #     data_list, booked_slots = add_data(calend, data_list, booked_slots)
    #     write_to_csv(header_list, data_list, 'calendar_events.csv')
    # except:
    #     pass

    return booked_slots


def get_clinics_cal(days_to_store, service_obj):
    global data_list

    booked_slots = dict()

    # store data into memory in lists. Each list uses the format below
    header_list = ['Event name', 'Start Date', 'Start Time', 'End Date', 'End Time']

    # set current and end date to be downloaded, use n as the difference between today and the end date
    current_date = str(date.today()) + 'T00:00:00.000Z'
    end_date = str(date.today() + timedelta(days=int(days_to_store))) + 'T23:59:00.000Z'

    data_list.clear()
    try:
        calend = service_obj.events().list(calendarId='group2codeclinic@gmail.com', timeMin=current_date, timeMax=end_date, singleEvents=True, orderBy='startTime').execute()
    except errors.HttpError:
        print("User not connected to the clinic calendar")
        exit()
    data_list, booked_slots = add_data(calend, data_list, booked_slots)
    write_to_csv(header_list, data_list, 'calendar_events.csv')

    return booked_slots


def add_data(calendar_events_dict, data_list, booked_slots):
    # add event data into booked slots and data list
    for event in calendar_events_dict['items']:
        if event['status'] != 'cancelled':
            summary = event['summary'] if 'summary' in event else 'Empty Event'
            start_date, start_time, start_iso_time = get_time_date(event['start']['dateTime'])  # get an event's start date time
            end_date, end_time, end_iso_time = get_time_date(event['end']['dateTime'])

            data_list.append([summary, start_date, start_time, end_date, end_time])  # added start iso time for sorting

            if start_date in booked_slots:
                booked_slots[start_date].append([start_iso_time.time(), end_iso_time.time()])
            else:
                booked_slots[start_date] = []
                booked_slots[start_date].append([start_iso_time.time(), end_iso_time.time()])
    return data_list, booked_slots


def write_to_csv(header_list, data_list, file_name):
    # move data from data_list to a csv file
    with open(file_name, 'w', newline='') as csv_file:
        writer_obj = csv.writer(csv_file)

        writer_obj.writerow(header_list)
        for row in data_list:
            writer_obj.writerow(row)


def book_event(service_obj, days, event):
    made = service_obj.events().insert(calendarId='group2codeclinic@gmail.com', body=event).execute()
    print('Event created: {}'.format(made.get('htmlLink')))
    return store_next_n_days(days, service_obj)
