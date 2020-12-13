import datetime

calendar = ''


def search_for_event(service_object, user_booked_slots, compare_slots, which_calendar='group2codeclinic@gmail.com'):
    global calendar
    
    calendar = which_calendar
    while True:
        try:
            print("\nEnter exit/quit/close at any point to quit.")
            desired_event = input("\nPlease enter the event name: ")

            if desired_event.lower().strip() in ['exit', 'quit', 'close']:
                exit()

            matches = get_matching_events(service_object, desired_event)

            desired_date, start = get_date_time(user_booked_slots, compare_slots)

            final_event = get_final_event(matches, start, desired_date)

            return final_event
        except ValueError:
            continue


def get_final_event(matches, start, date):
    final_event = dict()
    for event in matches:
        try:
            event_time = datetime.datetime.fromisoformat(event['start']['dateTime'])
        except KeyError:
            print('Event has no start date. Check if it has been cancelled.')
            raise ValueError

        same_time = start == event_time.time()
        same_date = date == event_time.strftime("%d %B %Y")

        if same_date and same_time:
            final_event = event
            break

    if not final_event:
        print("No event for the given date and time.")
        raise ValueError
    return final_event


def get_matching_events(service_object, desired_event):
    calendar_events = service_object.events().list(calendarId='group2codeclinic@gmail.com').execute()
    matches = list()

    if 'items' not in calendar_events:
        print("Event not found.")
        exit()

    for event in calendar_events['items']:
        if 'summary' in event and event['summary'].lower() == desired_event.lower():
            matches.append(event)

    if len(matches) == 0:
        print("Event not found.")
        raise ValueError
    return matches


def get_date_time(user_booked_slots, compare_slots):
    desired_date = input("\nPlease enter the date of the event (i.e 23 December 2020): ").strip()
    start_time_str = input("Please enter the start time of the slot (i.e 10:00): ").strip()

    if desired_date.lower() in ['exit', 'quit', 'close']:
        exit()
    if start_time_str.lower() in ['exit', 'quit', 'close']:
        exit()

    try:
        start_time_object = datetime.time.fromisoformat(start_time_str)
        end_time_object = (datetime.datetime.combine(datetime.date.today(), start_time_object) + datetime.timedelta(minutes=30)).time()
        datetime.datetime.strptime(desired_date, "%d %B %Y")
    except ValueError:
        print('Please enter the correct time and date formats.')
        raise ValueError

    for day in user_booked_slots:
        if day == desired_date:
            compare_slots(user_booked_slots[day], start_time_object, end_time_object)
    return desired_date, start_time_object
