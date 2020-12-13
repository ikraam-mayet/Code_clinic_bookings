import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauthlib.oauth2.rfc6749.errors import AccessDeniedError


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
            raise FileNotFoundError  # if file is empty force an exception to be raised
        active_credits = pickle.load(credits_file)
        credits_file.close()
        return active_credits
    except FileNotFoundError:
        # Should the file be missing, create new credentials
        try:
            print('File missing\\empty.\nCreating new credentials...')
            credits_file = open(f"{user_home}/.credentials.pkl", "wb")
            new_flow = get_flow()
            active_credits = new_flow.run_local_server(authorization_prompt_message='Please authenticate the app. Opening browser...')
            pickle.dump(active_credits, credits_file)
            credits_file.close()            
            return active_credits
        # User does not have the credits file in the right location. Exit the app.
        except FileNotFoundError:
            exit()
        # User denied access if error is raised. Exit the app.
        except AccessDeniedError:
            print("Authentication failed. Please give the app permission to your calendar.")
            exit()
        # Process is still running. Ask user to wait and exit the app.
        except OSError:
            credits_file.close()
            print('Authentication failed. Please try again in 2 minutes.')
            exit()


def get_flow():
    """
    Return a flow object for the level of permission required by the app.
    """

    # Level of permission we want to request for the application
    scopes = ['https://www.googleapis.com/auth/calendar']

    user_home = os.path.expanduser('~')

    if not os.path.isfile(f"{user_home}/Downloads/client_secret.json"):
        print("Please check if there is a client_secret.json file in the downloads directory.")
        raise FileNotFoundError

    flow = InstalledAppFlow.from_client_secrets_file(f"{user_home}/Downloads/client_secret.json", scopes=scopes)
    return flow


def authenticate_user(credits_file, test_mode=False):
    """
    Create a service that will interact with the api
    using the user's active credentials.
    """

    try:
        my_service = build('calendar', 'v3', credentials=credits_file)
        print("Signed in.")
        return my_service
    except:
        print("Invalid credentials. Creating new ones...")
        credits_file = open_create_credits_file(delete_file=True)
        my_service = build('calendar', 'v3', credentials=credits_file)
        print("Signed in.")
        return my_service
    raise TypeError("Credits file should be a Google OAuth2 Credentials object.")
    exit()
