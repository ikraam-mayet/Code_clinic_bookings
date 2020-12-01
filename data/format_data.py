from datetime import datetime

def get_time_date(long_format_time):
    """
    Get the time and date from the longer format time.
    
    Long format is: YYYY-MM-DDTHR:MN:SC.MSCZ
    Returns "Day Month-Name Year", "Hour:Seconds", Hour:Seconds:microseconds
    """

    months = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June',
    7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

    date_object = datetime.fromisoformat(long_format_time)
    date_str = date_object.strftime(f'%d {months[date_object.month]} %Y')
    time_str = str(date_object.time())

    return date_str, time_str[:5], date_object