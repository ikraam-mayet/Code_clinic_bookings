import datetime


def patient_book_slot(service_object, user_booked_slots):

    desired_event = input("Input an event name that you would like to book (case sensitive): ")

    matches = get_matching_events(service_object, desired_event)

    desired_date, start = get_date_time(user_booked_slots)

    final_event = get_final_event(matches, start, desired_date)

    final_event = generate_new_guest_summary(final_event)

    patched_event = {'summary': final_event['summary'],
                     'attendees': final_event['attendees']}

    returned = service_object.events().patch(calendarId='group2codeclinic@gmail.com', body=patched_event, eventId=final_event['id'], sendUpdates='all').execute()
    print(f"Slot booked. Please visit {returned.get('htmlLink')} to confirm.")


def generate_new_guest_summary(final_event):
    username = input('Please enter your student username: ')
    student_email = f"{username}@student.wethinkcode.co.za"
    new_guest = {'email': student_email, 'responseStatus': 'accepted'}
    cal = {'email': 'group2codeclinic@gmail.com', 'self': True, 'responseStatus': 'accepted'}

    try:
        new_summary = f"{final_event['summary']} // {username} session."
        final_event['summary'] = new_summary
    except KeyError:
        final_event['summary'] = f"{username} session."

    if 'attendees' in final_event and len(final_event['attendees']) < 3:
        final_event['attendees'].append(new_guest)
    elif 'attendees' not in final_event:
        final_event['attendees'] = [new_guest, cal]  # add both the user and calendar as guests if it has no guests (which it will always have)
    else:
        print("Slot fully booked.")
        exit()
    return final_event


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
            print('Slot blocked in your personal calendar.')
            exit()
        if end > slot[0] and end <= slot[1]:
            print('Slot blocked in your personal calendar.')
            exit()