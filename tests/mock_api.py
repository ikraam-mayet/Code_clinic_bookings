import copy
import random
import datetime

class Flow:

    def __init__(self):
        pass

    def run_local_server(self, authorization_prompt_message="This is a mock"):
        return {"client_id":"1234","project_id":"ThisIsATest","auth_uri":"https://test.co.za","token_uri":"https://test.co.za/token","JT":"https://still-test.co.za","client_secret":"i-like-the-room","redirect_uris":["urn:hello","http://done"]}


class Mock_Service:

    def __init__(self):
        pass

    def events(self):
        return Mock_Events()


class Mock_Events:

    def __init__(self):
        self.events = {'kind': 'test#events', 
        'etag': '"Group2"',
        'summary': 'test-email@wedontexist.co.za',
        'updated': '2020-11-16T00:42:00.000Z',
        'timeZone': 'Africa/Johannesburg',
        'accessRole': 'owner',
        'defaultReminders': [{'method': 'popup', 'minutes': 10}],
        'items': self.fake_events()
        }

    def list(self, calendarId='primary', timeMin='0', timeMax='1', singleEvents=True, orderBy='startTime'):
        events_to_return = copy.deepcopy(self.events)

        index = 0
        for event in self.events['items']:
            if event['start']['dateTime'] < timeMin and timeMin != '0':
                events_to_return['items'].pop(index)
                index -= 1
            elif event['start']['dateTime'] > timeMax and timeMax != '1':
                events_to_return['items'].pop(index)
                index -= 1
            index += 1

        return Fake_Execute_Obj(what_to_return=events_to_return)

    def insert(self, calendarId='primary', body=None):
        self.events['items'].append(body)
        body['htmlLink'] = f"https://www.test.co.za/calendar/event?eid=wEStilLDontExist{random.randint(4, 9999)}"
        return Fake_Execute_Obj(what_to_return=body)

    def patch(self, calendarId='nix', body=None, eventId='0', sendUpdates='none'):
        if eventId == '0' or calendarId == 'nix':
            raise ValueError('Event ID and body required.')

        chosen_one = self.events['items'][0]

        if body is None or type(body) is not dict:
            return Fake_Execute_Obj(chosen_one)
        else:
            changed_keys = body.keys()
            for key in changed_keys:
                try:
                    chosen_one[key] = body[key]
                except KeyError:
                    continue
        return Fake_Execute_Obj(chosen_one)


    def fake_events(self):
        event_one = {'kind': 'test#event', 'etag': '"678-999-8212"',
        'id': '0mlugf7j95b8_20201116T060000Z', 'status': 'confirmed',
        'htmlLink': 'https://www.test.co.za/calendar/event?eid=wEStilLDontExist',
        'created': '2020-10-24T09:01:58.000Z', 'updated': '2020-10-24T09:03:27.846Z',
        'summary': 'Did you find the easter egg?', 'creator': {'email': 'soulja@boy.wedonotthinkcodesincewedontexist.co.za', 'self': True},
        'organizer': {'email': 'soulja@boy.wedonotthinkcodesincewedontexist.co.za', 'self': True},
        'start': {'dateTime': datetime.date.today().strftime("%Y-%m-%dT08:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'end': {'dateTime': datetime.date.today().strftime("%Y-%m-%dT09:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'attendees': [{'email': 'send@help.co.za'}],
        'recurringEventId': '0mlugf7j95b8_20201116T060000Z',
        'originalStartTime': {'dateTime': '2020-11-16T08:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'iCalUID': '0mlugf7j95b8_20201116T060000Z@google.com', 'sequence': 0, 
        'reminders': {'useDefault': True}}

        event_two = {'kind': 'test#event', 'etag': '"NRG"',
        'id': 'I-Am-Your-Father', 'status': 'confirmed',
        'htmlLink': 'https://www.test.co.za/calendar/event?eid=wEStilLDontExist2',
        'created': '2020-10-24T09:21:14.000Z', 'updated': '2020-10-26T19:03:27.846Z',
        'summary': 'This event totally happened', 'creator': {'email': 'lucas@arts.gamesAreTheBest.co.za', 'self': True},
        'organizer': {'email': 'soulja@boy.wedonotthinkcodesincewedontexist.co.za', 'self': True},
        'start': {'dateTime': (datetime.date.today() + datetime.timedelta(days=100)).strftime("%Y-%m-%dT18:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'end': {'dateTime':  (datetime.date.today() + datetime.timedelta(days=100)).strftime("%Y-%m-%dT19:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'recurringEventId': 'I-Am-Your-Father',
        'originalStartTime': {'dateTime': '2021-12-01T18:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'iCalUID': 'I-Am-Your-Father@google.com', 'sequence': 0,
        'reminders': {'useDefault': True}}

        event_three = {'kind': 'test#event', 'etag': '"Gamer-Boy"',
        'id': 'Bethany-Esda', 'status': 'confirmed',
        'htmlLink': 'https://www.test.co.za/calendar/event?eid=wEStilLDontExist3',
        'created': '2020-10-24T09:01:58.000Z', 'updated': '2020-10-24T09:03:27.846Z',
        'summary': 'UDUDLRLRBA', 'creator': {'email': 'death-stranding-slapped@seriously.co.za', 'self': True},
        'organizer': {'email': 'death-stranding-slapped@seriously.co.za', 'self': True},
        'start': {'dateTime': (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT08:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'end': {'dateTime': (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%dT09:00:00"), 'timeZone': 'Africa/Johannesburg'},
        'recurringEventId': 'Bethany-Esda',
        'originalStartTime': {'dateTime': '2020-11-16T08:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'iCalUID': 'Bethany-Esda@google.com', 'sequence': 0,
        'reminders': {'useDefault': True}}

        return [event_one, event_two, event_three]


class Fake_Execute_Obj:

    def __init__(self, what_to_return):
        self.return_this = what_to_return

    def execute(self):
        return self.return_this
