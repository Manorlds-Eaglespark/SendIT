import unittest
import json
import os
from app import create_app
from tests.data import *



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        config_name = os.getenv('APP_SETTINGS') # config_name = "development"
        self.app = create_app(config_name).test_client()


    def test_register_new_user(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/auth/register', data= json.dumps(user), content_type='application/json')
        data = json.loads(response.data)
        self.assertIn("Name: - Enter only leters. More than 3 characters.", data['status message'])

    def test_register_new_user_invalid_email(self):
        """"Test API to create a new user with invalid email"""
        response = self.app.post('/v1/auth/register', data= json.dumps(user_invalid_email), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_register_new_user_no_name_given(self):
        """"Test API to create a new user with no name entered"""
        response = self.app.post('/v1/auth/register', data= json.dumps(user_no_name), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_register_new_user_no_password_given(self):
        """"Test API to create a new user with no password entered"""
        response = self.app.post('/v1/auth/register', data= json.dumps(user_no_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_user_password_not_given(self):
        """"Test API for logging in user with no password entered"""
        response = self.app.post('/v1/auth/login', data= json.dumps(user_login_details_no_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    
    def test_login_user_password_not_given(self):
        """"Test API for logging in user with no password entered"""
        response = self.app.post('/v1/auth/login', data= json.dumps(user_login_details_no_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_user_wrong_password_given(self):
        """"Test API for logging in user with an wrong password"""
        response = self.app.post('/v1/auth/login', data= json.dumps(user_login_details_wrong_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('Enter correct credentials, and then try again', data['status message'])

    def test_login_user_invalid_email_given(self):
        """"Test API for logging in user with an invalid email"""
        response = self.app.post('/v1/auth/login', data= json.dumps(user_login_details_wrong_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)