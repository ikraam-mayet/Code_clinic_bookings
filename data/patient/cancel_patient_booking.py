from data import event_search


def patient_cancel_slot(service_object, user_booked_slots):

    final_event = event_search.search_for_event(service_object, user_booked_slots, compare_slots)

    try:
        student = final_event['attendees'][0]['email']
        test_one = service_object.events().list(calendarId=student).execute()
        test_two = service_object.events().list(calendarId='primary').execute()

        if test_one != test_two:
            raise ValueError
    except:
        print("You are not allowed to delete that event.")
        return patient_cancel_slot(service_object, final_event)

    remove_att = final_event['attendees']
    del final_event['attendees']
    remove_att = remove_att[:-1]
    final_event['attendees'] = remove_att
    remove_summ = final_event['summary']
    del final_event['summary']
    remove_summ = remove_summ.split(" ")
    remove_summ = remove_summ[0]
    final_event['summary'] = remove_summ

    print("Patient booking has been cancelled\nHave a good day!")
    return service_object.events().update(calendarId='group2codeclinic@gmail.com', body=final_event, eventId=final_event['id'], sendUpdates='all').execute()


def compare_slots(day, start, end):
    pass
