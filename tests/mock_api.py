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

    def list(self):
        return self.events

    def insert(self, calendarId='primary', body=None):
        self.events['items'].append(body)

    def fake_events(self):
        event_one = {'kind': 'test#event', 'etag': '"678-999-8212"',
        'id': '0mlugf7j95b8_20201116T060000Z', 'status': 'confirmed',
        'htmlLink': 'https://www.test.co.za/calendar/event?eid=wEStilLDontExist',
        'created': '2020-10-24T09:01:58.000Z', 'updated': '2020-10-24T09:03:27.846Z',
        'summary': 'Did you find the easter egg?', 'creator': {'email': 'soulja@boy.wedonotthinkcodesincewedontexist.co.za', 'self': True},
        'organizer': {'email': 'soulja@boy.wedonotthinkcodesincewedontexist.co.za', 'self': True},
        'start': {'dateTime': '2020-11-16T08:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'end': {'dateTime': '2020-11-16T09:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
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
        'start': {'dateTime': '2020-12-01T18:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'end': {'dateTime': '2020-12-01T19:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'recurringEventId': 'I-Am-Your-Father',
        'originalStartTime': {'dateTime': '2020-12-01T18:00:00+02:00', 'timeZone': 'Africa/Johannesburg'},
        'iCalUID': 'I-Am-Your-Father@google.com', 'sequence': 0, 
        'reminders': {'useDefault': True}}

        return [event_one, event_two]