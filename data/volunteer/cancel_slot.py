import datetime

def get_matching_events(service_object, desired_event):
    calendar_events = service_object.events().list(calendarId='group2codeclinic@gmail.com').execute()
    matches = list()

    if 'items' not in calendar_events:
        print("Event not found.")
        exit()

    for event in calendar_events['items']:
        if 'summary' in event and event['summary'] == desired_event.lower():
            matches.append(event)

    if len(matches) == 0:
        print("Event not found.")
        exit()
    return matches


def calling_of_cancelations_function(service_object, user_booked_slots,service_obj):

    desired_event = input("Input an event name that you would like to book (case sensitive): ")

    matches = get_matching_events(service_object, desired_event)

    desired_date, start = get_date_time(user_booked_slots)

    final_event = get_final_event(matches, start, desired_date)
    event_id = final_event['id']

    if len(final_event['attendees']) == 1:
        volunteer_cancel_slot(service_obj, event_id)
        print("\nVolunteering has been deleted")
    else:
        print("\nSlot has been booked by patient")



def get_date_time(user_booked_slots):
    desired_date = input("Please enter the date of the event (i.e 23 December 2020): ")
    start_time_str = input("Please enter the start time of the slot you want to book (i.e 10:00): ")

    try:
        start_time_object = datetime.time.fromisoformat(start_time_str)
        end_time_object = (datetime.datetime.combine(datetime.date.today(), start_time_object) + datetime.timedelta(minutes=30)).time()
    except ValueError:
        print('Please enter the correct time and date formats.')
        exit()

    for day in user_booked_slots:
        if day == desired_date:
            compare_slots(user_booked_slots[day], start_time_object, end_time_object)
    return desired_date, start_time_object


def get_final_event(matches, start, date):
    final_event = ''
    for event in matches:
        try:
            event_time = datetime.datetime.fromisoformat(event['start']['dateTime'])
        except KeyError:
            print('Event has no start date. Check if it has been cancelled.')
            exit()

        same_time = start == event_time.time()
        same_date = date == event_time.strftime("%d %B %Y")

        if same_date and same_time:
            final_event = event
    if final_event == '':
        print("Invalid date and time.")
        exit()
    return final_event


def compare_slots(day, start, end):
    for slot in day:
        if start >= slot[0] and start < slot[1]:
            return True
        


def volunteer_cancel_slot(service_obj, event_id):
    # eventId = service_obj['Id']
    service_obj.events().delete(calendarId='primary', eventId=event_id).execute()
