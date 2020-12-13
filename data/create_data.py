import csv
from data.volunteer import making_a_slot
from datetime import date, timedelta
from data.format_data import *
import data.display_calendar as display_calender
import googleapiclient.errors as errors
from googleapiclient.discovery import Resource

data_list = []


def store_next_n_days(n, service_obj, test_mode=False):
    """
    param:
    n - number of days to store
    service_obj - the google api service object

    Store all events happening in the next n days
    for the signed in user in the events.csv file.
    """

    global data_list

    try:
        int(n)
    except ValueError:
        raise ValueError("n should be an integer.")

    if type(service_obj) is not Resource and test_mode is False:
        raise ValueError("Service Object should be a google api resource.")

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

    return booked_slots


def get_clinics_cal(days_to_store, service_obj, test_mode=False):
    """
    param:
    days to store - number of days to store
    service_obj - the google api service object

    Store all events happening in the next 'days_to_store' days
    for the signed in user in the events.csv file.
    """

    global data_list

    try:
        int(days_to_store)
    except ValueError:
        raise ValueError("days_to_store should be an integer.")

    if type(service_obj) is not Resource and test_mode is False:
        raise ValueError("Service Object should be a google api resource.")

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
        print("User account not connected to the clinic calendar.")
        exit()
    data_list, booked_slots = add_data(calend, data_list, booked_slots)
    write_to_csv(header_list, data_list, 'calendar_events.csv')

    return booked_slots


def add_data(calendar_events_dict, data_list, booked_slots):
    """
    param:
    calendar_events_dict - dictionary containing all events in google format
    data_list - the list containing all slots for the upcoming days
    booked_slots - dictionary of all booked slots

    Book a slot for every event in calendar_events_dict.
    Store every event's details in data_list and 
    return the updated data_list and booked_slots.
    """
    if type(calendar_events_dict) is not dict:
        raise ValueError("Calendar events should be in a dictionary.")
    
    if type(data_list) is not list:
        raise ValueError("Data list should be a list.")

    if type(booked_slots) is not dict:
        raise ValueError("Booked slots should be in a dictionary.")

    # add event data into booked slots and data list
    for event in calendar_events_dict['items']:
        if event['status'] != 'cancelled':
            summary = event['summary'] if 'summary' in event else 'Empty Event.'
            description = event['description'] if 'description' in event else 'Empty Description.'
            start_date, start_time, start_iso_time = get_time_date(event['start']['dateTime'])  # get an event's start date time
            end_date, end_time, end_iso_time = get_time_date(event['end']['dateTime'])
            attendees = event['attendees'] if 'attendees' in event else 0
            attendees = len(attendees) if not isinstance(attendees, int) else 0

            description, summary = format_summary_description(description, summary)
            data_list.append([summary, description, start_date, start_time, end_date, end_time, attendees])  # added start iso time for sorting

            if start_date in booked_slots:
                booked_slots[start_date].append([start_iso_time.time(), end_iso_time.time()])
            else:
                booked_slots[start_date] = []
                booked_slots[start_date].append([start_iso_time.time(), end_iso_time.time()])
    return data_list, booked_slots


def format_summary_description(description, summary): # needs to be tested
    """
    param:
    description - an indvidual event's description (str)
    summary - an individual event's summary (str)

    Format the given description and summary by
    limiting them to 60 characters and removing any commas.
    Return the new description and summary.
    """

    if type(description) is not str or type(summary) is not str:
        raise ValueError("Description and summary should be strings.")

    if len(description) > 60:
        description = description[:61]
    
    if len(summary) > 60:
        summary = summary[:61]

    if ',' not in description and ',' not in summary:
        return description, summary

    return description.replace(',', ' '), summary.replace(',', ' ')


def write_to_csv(header_list, data_list, file_name):
    """
    param:
    header_list - the list containing the csv's headers
    data_list - a list containing event details for all events
    file_name - the name of the target csv

    Write all the data in data_list to a csv, with columns
    determined by header_list.
    """
    if type(header_list) is not list:
        raise ValueError("Header list should be a list.")

    if type(data_list) is not list:
        raise ValueError("Data list should be a list.")
    
    if type(file_name) is not str:
        raise ValueError("File name should be a string.")

    # move data from data_list to a csv file
    with open(file_name, 'w', newline='') as csv_file:
        writer_obj = csv.writer(csv_file)

        writer_obj.writerow(header_list)
        for row in data_list:
            writer_obj.writerow(row)


def book_event(service_obj, days, event, test_mode=False):
    """
    param:
    service_obj - the google api service object
    days - the number of days to store
    event - dictionary containing the event details

    Add the given event to the code clinic calendar,
    print out the created event's html link,
    and update the stored data to include the new event.
    """

    try:
        int(days)
    except ValueError:
        raise ValueError("Days should be an integer.")

    if type(service_obj) is not Resource and test_mode is False:
        raise ValueError("Service Object should be a google api resource.")

    if 'end' not in event or 'start' not in event:
        raise ValueError("New event should have a start and end time defined.")

    made = service_obj.events().insert(calendarId='group2codeclinic@gmail.com', body=event).execute()
    print('Event created: {}'.format(made.get('htmlLink')))
    return store_next_n_days(days, service_obj)
