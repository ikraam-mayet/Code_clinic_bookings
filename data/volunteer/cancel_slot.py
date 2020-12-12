import datetime
from data import event_search


def calling_of_cancelations_function(service_object, user_booked_slots, service_obj):

    final_event = event_search.search_for_event(service_object, user_booked_slots, compare_slots, which_calendar='primary')
    event_id = final_event['id']

    if len(final_event['attendees']) == 1:
        volunteer_cancel_slot(service_obj, event_id)
        return ("\nVolunteering has been deleted")
    else:
        return ("\nSlot has been booked by patient")


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
    return service_obj.events().delete(calendarId='group2codeclinic@gmail.com', eventId=event_id).execute()
