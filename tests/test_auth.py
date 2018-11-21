import sys
import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
import json
from app import create_app
from app.database.Database import Database
from tests.data import register_user,  user_invalid_email, user_no_name, user_login_details_no_password, user_login_details_invalid_email



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="development")
        self.client = self.app.test_client()
        self.database = Database()
        with self.app.app_context():
            self.database.delete_all_tables()
            self.database.create_all_tables()

    def test_register_new_user(self):

        """"Test API to create a new user"""
        response = self.client.post('/v1/auth/register', data=json.dumps(register_user), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('You registered successfully. Please log in.', data['message'])

    def test_register_new_user_invalid_email(self):
        """"Test API to create a new user with an email in bad format"""
        response = self.client.post('/v1/auth/register', data= json.dumps(user_invalid_email), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Please enter a valid Email.', data['message'])

    def test_register_new_user_no_name_given(self):
        """"Test API to create a new user"""
        response = self.client.post('/v1/auth/register', data=json.dumps(user_no_name),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Name field: - Enter only letters. More than 3 characters.', data['message'])

    # def test_register_existing_user(self):
    #     """"Test API to create a new user"""
    #     response1 = self.client.post('/v1/auth/register', data=json.dumps(register_user2),
    #                   content_type='application/json')
    #     self.assertEqual(response1.status_code, 201)
    #     response2 = self.client.post('/v1/auth/register', data=json.dumps(register_user2),
    #                              content_type='application/json')
    #     data = json.loads(response2.data)
    #     self.assertEqual(response2.status_code, 403)
    #     self.assertIn('User already exists. Please login.', data['message'])

    # def test_login_user(self):
    #     """"Test API for logging in user"""
    #
    #
    #     self.client.post('/v1/auth/register', data=json.dumps(register_user3),
    #                                  content_type='application/json')
    #     # self.assertEqual(response1.status_code, 201)
    #
    #     response = self.client.post('/v1/auth/login', data=json.dumps(user_login_details3),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertIn('You logged in successfully.', data['message'])

    def test_login_user_password_not_given(self):
        """"Test API for logging in user"""
        response = self.client.post('/v1/auth/login', data=json.dumps(user_login_details_no_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('Please enter a valid Password.', data['message'])

    # def test_login_user_wrong_password_given(self):
    #     """"Test API for logging in user"""
    #     response = self.app.post('/v1/auth/login', data=json.dumps(user_login_details_wrong_password),
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 401)
    #     data = json.loads(response.data)
    #     self.assertIn('Invalid email or password, Please edit, then try again', data['message'])


    def test_login_user_invalid_email_given(self):
        """"Test API for logging in user"""
        response = self.client.post('/v1/auth/login', data=json.dumps(user_login_details_invalid_email),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)


    def tearDown(self):
        self.database.delete_all_tables()


if __name__ == "__main__":
    unittest.main()
