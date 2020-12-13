# Code_clinic_bookings
Code clinic booking system based of google calendar api 


How to use the Code Clinic Program

### How to use

- Download the repo
- Run 'pip3 install -r requirements.txt' to pip install all the required packages

### Setup and first time login:
Run the command "python3 app.py init" to begin the setup for first time use, the user will be asked for their username as well as for permission for the app to access their google calendar
after the user has accepted permission, the program saves the users login details to be used for the program.
If there is a user already logged in and the new user would like to switch their own profile simply typing in the command "python3 app.py delete", 
will then remove any existing login details to allow for a new user to login.


### Viewing of the calendar:
After the user has finished setup and login, the user may now view their current calendar by executing the command "python3 app.py -v",
this will display the users primary calendar taken from their Google Calendar.
If the user would like to view any available slots or simply view the Code Clinics calendar, the user may enter "python3 app.py -c",
doing so will display the current Code Clinics calendar as well as available slots to the user depicted in color, 
eg. Red - Booked slot, Green - Available slot or Blue - Event occurring on calendar.


### Booking a slot (Patient/Volunteer):
Executing the "python3 app.py patient" command will display the Code Clinics calendar as well as allow the patient to book a slot created by a volunteer for help
depending on what the volunteer has availed themselves for.The patient will have be prompted with a date/time of the slot as well as ask which event they would like to select.
Once the patient has booked a slot, the program will display the calendar again to show the patient what they have booked. A patient cannot book any slots already occupied which are displayed in Red.
For volunteers similar to the patient command, "python3 app.py volunteer". This will bring up the Code Clinic calendar and ask for a date/time as well as topic the 
volunteer would like to help with. Once the volunteer has entered each prompt it will create three, thirty minute slots that the volunteer will be assigned to help.


### Cancellation of slots (Patient/Volunteer):
To cancel a patient slot, the user needs to enter the command "python3 app.py -p_cal". Once the user has entered the command they will be shown their calendar and the events they had specified for help.
The user will be asked to enter the date/time and event name they wish to cancel and once done, the program will remove them from the event they needed help in.
Similarly to the patient cancellation the volunteer will need to enter in "python3 app.py -v_cal", this will bring up the Code Clinic calendar of events and the volunteer will be asked for date/time
and event name they wish to cancel although if there is already a patient present in an event they wish to cancel it will not be removed as they have been specified a specific time to help and cannot be cancelled
until the patient cancels first


### Help:
If the user is having difficulty using the app, running the "python3 app.py" or "python3 app.py help" commands will bring up a display of available commands that can be executed
