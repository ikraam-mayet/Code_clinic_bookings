import os
import sys
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import google.oauth2.credentials

def open_create_credits_file(delete_file=False):
    """
    Open the user's config file and return the active credits token.
    """
    if type(delete_file) is not bool:
        raise TypeError("Delete file should be a boolean.")

    user_home = os.path.expanduser('~') # String that holds user's home dir

    if (os.path.isfile(f"{user_home}/.credentials.pkl")) and (delete_file == True or 'delete' in sys.argv):
        os.remove(f"{user_home}/.credentials.pkl")
    # Check if credentials file exists, if it does read the active credentials from it
    try:
        print('Authenticating...')
        credits_file = open(f"{user_home}/.credentials.pkl", "rb")
        if os.path.getsize(f"{user_home}/.credentials.pkl") == 0:
            credits_file.close()
            raise FileNotFoundError # if file is empty force an exception to be raised
        active_credits = pickle.load(credits_file)
        credits_file.close()
        return active_credits
    except FileNotFoundError:
        # Should the file be missing, create new credentials
        try:
            print('File missing/empty.\nCreating new credentials...')
            credits_file = open(f"{user_home}/.credentials.pkl", "wb")
            active_credits = get_flow().run_local_server(authorization_prompt_message='Please authenticate the app. Opening browser...')
            pickle.dump(active_credits, credits_file)
            credits_file.close()
            return active_credits
        # Assume user denied access if the previous try block failed. Exit the app.
        except:
            credits_file.close()
            print('Authentication failed. Please give the app permission to your calendar or try again in 5 minutes.')
            exit()
    
def get_flow():
    # Level of permission we want to request for the application
    scopes = ['https://www.googleapis.com/auth/calendar']

    # ??
    user_home = os.path.expanduser('~')

    flow = InstalledAppFlow.from_client_secrets_file(f"{user_home}/Downloads/client_secret.json", scopes=scopes)
    return flow

def authenticate_user(credits_file):
    # Create a service that will interact with the api using the active credentials

    try:
        my_service = build('calendar', 'v3', credentials=credits_file)
        return my_service
    except:
        print("Invalid credentials. Creating new ones...")
        credits_file = open_create_credits_file(delete_file=True)
        my_service = build('calendar', 'v3', credentials=credits_file)
        return my_service
    raise TypeError("Credits file should be a Google OAuth2 Credentials object.")
    exit()