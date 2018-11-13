import unittest
import json
import os
from app import create_app



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        config_name = os.getenv('APP_SETTINGS') # config_name = "development"
        self.app = create_app(config_name).test_client()

        self.user = {
                        "name": "Bob",
                        "email": "bob@gmail.com", 
                        "password": "xxy210"
                     }

        self.userr_invalid_email = {
                        "name": "Bob",
                        "email": "__lll652", 
                        "password": "xxy210"
                     }

        self.userr_no_name = {
                        "name": "",
                        "email": "__lll652", 
                        "password": "xxy210"
                     }

        self.userr_no_password = {
                        "name": "dafddf",
                        "email": "afdsa@gmail.com", 
                        "password": ""
                     }

        self.userr_existing = {
                        "name": "Anorld Mukone",
                        "email": "manorldsapiens@gmail.com", 
                        "password": "123456"
                    }

        self.user_login_details = {
                                "email": "manorldsapiens@gmail.com", 
                                "password": "123456",
                            }

        self.user_login_details_no_password = {
                                "email": "manorldsapiens@gmail.com", 
                                "password": "",
                            }
        self.user_login_details_wrong_password = {
                                "email": "manorldsapiens@gmail.com", 
                                "password": "fgafgdvsadf",
                            }
        self.user_login_details_invalid_email = {
                                "email": "...", 
                                "password": "fgafgdvsadf",
                            }
        
    def test_register_new_user(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/auth/register', data= json.dumps(self.user), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 202)

    def test_register_new_user_invalid_email(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/auth/register', data= json.dumps(self.userr_invalid_email), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Please enter a valid Email.', data['status message'])

    def test_register_new_user_no_name_given(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/auth/register', data= json.dumps(self.userr_no_name), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Please enter a Name for your account.', data['status message'])

    def test_register_new_user_no_password_given(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/auth/register', data= json.dumps(self.userr_no_password), content_type='application/json')
        data = json.loads(response.data)
        self.assertIn('Please enter a Password for your account.', data['status message'])

    def test_register_existing_user(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/auth/register', data= json.dumps(self.userr_existing), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 202)
        self.assertIn('User already exists. Please login.', data['status message'])

    def test_login_user(self):
        """"Test API for logging in user"""
        response = self.app.post('/v1/auth/login', data= json.dumps(self.user_login_details), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('You logged in successfully.', data['status message'])

    def test_login_user_password_not_given(self):
        """"Test API for logging in user"""
        response = self.app.post('/v1/auth/login', data= json.dumps(self.user_login_details_no_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('Please enter a valid Password.', data['status message'])

    def test_login_user_wrong_password_given(self):
        """"Test API for logging in user"""
        response = self.app.post('/v1/auth/login', data= json.dumps(self.user_login_details_wrong_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('Invalid email or password, Please edit, then try again', data['status message'])

    def test_login_user_invalid_email_given(self):
        """"Test API for logging in user"""
        response = self.app.post('/v1/auth/login', data= json.dumps(self.user_login_details_wrong_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        
        
if __name__ == "__main__":
    unittest.main()
