import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def open_create_credits_file(delete_file=False):
    """
    Open the user's config file and return the active credits token.
    """
    if type(delete_file) is not bool:
        raise TypeError("Delete file should be a boolean.")

    user_home = os.path.expanduser('~') # String that holds user's home dir

    if delete_file and os.path.isfile(f"{user_home}/.credentials.pkl"):
        os.remove(f"{user_home}/.credentials.pkl")

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
            print('Authentication failed.\nPlease check if their is a client_secret.json file in the home directory.\nPlease give the app permission to your calendar or try again in 5 minutes.')
            exit()


def get_flow():
    """
    Return a flow object for the level of permission required by the app.
    """

    # Level of permission we want to request for the application
    scopes = ['https://www.googleapis.com/auth/calendar']

    user_home = os.path.expanduser('~')

    flow = InstalledAppFlow.from_client_secrets_file(f"{user_home}/Downloads/client_secret.json", scopes=scopes)
    return flow


def authenticate_user(credits_file):
    """
    Create a service that will interact with the api
    using the user's active credentials.
    """

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
