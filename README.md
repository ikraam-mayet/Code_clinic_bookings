# Code_clinic_bookings

This program can currently be used to book a slot in the user's primary calendar.
It can also download data from the current day and n days into the future (n being determined by the user at runtime).

### How to use

- Download the repo and run 'python3 app.py' in your console to start the application.
- When prompted, enter a number of days into the future you would like data for (0 will give you the current day's data).
- The app will attempt to authenticate you. A new browser window will open and ask you to give permission to the app.
- Once given the permission, the app will show you all the events for the number of days specified earlier.
- The app will then attempt to book a slot. You will need:
  - A date in 'Day Month Year' format. The day should be two digits (01, 13), the month should be the full word (May, January), and the year should be four digits (2020).
  - A start time in 'Hour:Minutes' format. Both the hours and minutes should be two digits (00:00, 13:35).
- If the calendar has an open 30 minute slot beginning at the specified time, the app will prompt you for an event summary. This is the name you will see for the event when listed on your calendar.
- You will then be prompted for a description to add any more details for the event.
- Once completed, the app prints out the calendar link for the created event and exits.
