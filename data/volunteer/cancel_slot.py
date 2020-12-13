import datetime
from data import event_search


def calling_of_cancelations_function(service_object, user_booked_slots, service_obj):

    final_event = event_search.search_for_event(service_object, user_booked_slots, compare_slots)
    event_id = final_event['id']

    if len(final_event['attendees']) == 1:
        volunteer_cancel_slot(service_obj, event_id)
        return ("\nVolunteering has been deleted")
    else:
        return ("\nSlot has been booked by patient")


def compare_slots(day, start, end):
    for slot in day:
        if start >= slot[0] and start < slot[1]:
            return True


def volunteer_cancel_slot(service_obj, event_id):
    return service_obj.events().delete(calendarId='group2codeclinic@gmail.com', eventId=event_id).execute()
