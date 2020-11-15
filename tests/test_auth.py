import os
import sys
import pickle
import unittest
from io import StringIO
from unittest.mock import patch
from authentication.authenticate import *

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
        pass

    def list(self):
        pass

    def insert(self):
        pass

class TestAuthentication(unittest.TestCase):

    def test_open_create_credits_file_file_exists(self):
        sys.stdout, temp = StringIO(), sys.stdout

        user_home = os.path.expanduser('~')
        file_name = '.credentials.pkl'

        with patch('authentication.authenticate.get_flow') as mock_get_flow:
            mock_get_flow.return_value = Flow()
            open_create_credits_file(delete_file=True)
            self.assertTrue(os.path.isfile(f'{user_home}/{file_name}'))
            self.assertTrue(os.path.getsize(f'{user_home}/{file_name}') > 0)

        with patch('authentication.authenticate.get_flow') as mock_get_flow:
            mock_get_flow.return_value = Flow()
            open_create_credits_file()
            self.assertTrue(os.path.isfile(f'{user_home}/{file_name}'))
            self.assertTrue(os.path.getsize(f'{user_home}/{file_name}') > 0)
        
        sys.stdout = temp

    def test_open_create_credits_file_empty_file_filled(self):
        sys.stdout, temp = StringIO(), sys.stdout

        user_home = os.path.expanduser('~')
        file_name = '.credentials.pkl'

        if (os.path.isfile(f'{user_home}/{file_name}')):
            os.remove(f"{user_home}/.credentials.pkl") # if the file exists, remove it
        
        with open(f"{user_home}/.credentials.pkl", "w"):
            pass # open and close file to leave it empty

        with patch('authentication.authenticate.get_flow') as mock_get_flow:
            mock_get_flow.return_value = Flow()
            open_create_credits_file()
            self.assertTrue(os.path.isfile(f'{user_home}/{file_name}'))
            self.assertTrue(os.path.getsize(f'{user_home}/{file_name}') > 0)

        sys.stdout = temp

    def test_open_create_credits_file_credentials_match(self):
        sys.stdout, temp = StringIO(), sys.stdout

        user_home = os.path.expanduser('~')
        file_name = '.credentials.pkl'

        with patch('authentication.authenticate.get_flow') as mock_get_flow:
            mock_get_flow.return_value = Flow()
            open_create_credits_file(delete_file=True)
            
            file_obj = open(f'{user_home}/{file_name}', 'rb')
            saved_credentials = pickle.load(file_obj)
            file_obj.close()
            self.assertEqual(saved_credentials, Flow().run_local_server())
        
        sys.stdout = temp

    def test_open_create_credits_file_return(self):
        sys.stdout, temp = StringIO(), sys.stdout

        user_home = os.path.expanduser('~')
        file_name = '.credentials.pkl'

        with patch('authentication.authenticate.get_flow') as mock_get_flow:
            mock_get_flow.return_value = Flow()
            returned = open_create_credits_file()

            self.assertEqual(returned, Flow().run_local_server())
            self.assertTrue(type(returned) == dict)
        
        sys.stdout = temp
    
    def test_open_create_credits_file_parameter(self):
        self.assertRaises(TypeError, open_create_credits_file, 'K')
        self.assertRaises(TypeError, open_create_credits_file, 0)
        self.assertRaises(TypeError, open_create_credits_file, list())
        self.assertRaises(TypeError, open_create_credits_file, dict())

    def test_get_flow_return(self):

        with patch('authentication.authenticate.InstalledAppFlow') as mock_IAF:
            mock_IAF.from_client_secrets_file.return_value = Flow()
            self.assertEqual(type(get_flow()), type(Flow()))
            self.assertEqual(get_flow().run_local_server(), Flow().run_local_server())

    def test_authenticate_user_parameter(self):

        self.assertRaises(TypeError, authenticate_user, list())
        self.assertRaises(TypeError, authenticate_user, str())
        self.assertRaises(TypeError, authenticate_user, int())
        self.assertRaises(TypeError, authenticate_user, set())

    def test_authenticate_user_valid_credentials(self):
        with patch('authentication.authenticate.build') as mock_build:
            mock_build.return_value = Mock_Service()
            service_returned = authenticate_user({'Test Number': 1})
            self.assertEqual(type(service_returned), type(Mock_Service()))

    @patch('authentication.authenticate.build')
    def test_authenticate_user_invalid_credentials(self, mock_build):
        with patch('authentication.authenticate.open_create_credits_file') as mock_OCF:
            mock_OCF.return_value = Flow().run_local_server()
            mock_build.side_effect = [TypeError, Mock_Service()]
            service_returned = authenticate_user({'Test Number': 2, 'Test Number 3': 3})
            self.assertEqual(type(service_returned), type(Mock_Service()))

if __name__ == "__main__":
    unittest.main()