from data import event_search


def patient_book_slot(service_object, user_booked_slots):

    final_event = event_search.search_for_event(service_object, user_booked_slots, compare_slots)
    final_event = generate_new_guest_summary(service_object, final_event)
    patched_event = {'summary': final_event['summary'],
                        'attendees': final_event['attendees']}

    returned = service_object.events().patch(calendarId='group2codeclinic@gmail.com', body=patched_event, eventId=final_event['id'], sendUpdates='all').execute()
    print(f"Slot booked. Please visit {returned.get('htmlLink')} to confirm.")
    return returned


def generate_new_guest_summary(service_object, final_event):
    username = input('Please enter your student username: ').lower().strip()
    student_email = f"{username}@student.wethinkcode.co.za"
    new_guest = {'email': student_email, 'responseStatus': 'accepted'}
    cal = {'email': 'group2codeclinic@gmail.com', 'self': True, 'responseStatus': 'accepted'}

    if username in ['exit', 'quit', 'close']:
        exit()

    try:
        test_one = service_object.events().list(calendarId=student_email).execute()
        test_two = service_object.events().list(calendarId='primary').execute()

        if test_one != test_two:
            raise ValueError
    except:
        print("Please enter YOUR username.")
        return generate_new_guest_summary(service_object, final_event)

    try:
        new_summary = f"{final_event['summary']} // {username} session."
        final_event['summary'] = new_summary
    except KeyError:
        final_event['summary'] = f"{username} session."

    if 'attendees' in final_event and len(final_event['attendees']) < 2:
        final_event['attendees'].append(new_guest)
    elif 'attendees' not in final_event:
        final_event['attendees'] = [new_guest, cal]  # add both the user and calendar as guests if it has no guests (which it will always have)
    else:
        print("Slot fully booked.")
        raise ValueError
    return final_event


def compare_slots(day, start, end):
    for slot in day:
        if start >= slot[0] and start < slot[1]:
            print('Slot blocked in your personal calendar.')
            raise ValueError
        if end > slot[0] and end <= slot[1]:
            print('Slot blocked in your personal calendar.')
            raise ValueError
