import unittest
import json
from app import create_app
from app.database.Database import Database
from tests.data import *



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.database = Database()
        self.database.create_all_tables()

    def test_register_new_user(self):
        response = self.client.post('/v1/auth/register', data=json.dumps(register_user), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('You registered successfully. Please log in.', data['message'])

    def test_register_new_user_invalid_email(self):
        response = self.client.post('/v1/auth/register', data= json.dumps(user_invalid_email), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Please enter a valid Email.', data['message'])

    def test_register_new_user_no_name_given(self):
        response = self.client.post('/v1/auth/register', data=json.dumps(user_no_name),
                                 content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual('Enter only letter in the English alphabet for name.', data['message'])

    def test_register_existing_user(self):
        self.client.post('/v1/auth/register', data=json.dumps(register_user2),
                       content_type='application/json')
        response1 = self.client.post('/v1/auth/register', data=json.dumps(register_user2),
                                 content_type='application/json')
        data = json.loads(response1.data)
        self.assertEqual(response1.status_code, 403)
        self.assertIn('User already exists. Please login.', data['message'])

    def test_login_user(self):
        self.client.post('/v1/auth/register', data=json.dumps(register_user3),
                                     content_type='application/json')
        response = self.client.post('/v1/auth/login', data=json.dumps(user_login_details3),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('You logged in successfully.', data['message'])

    def test_login_user_password_not_given(self):
        response = self.client.post('/v1/auth/login', data=json.dumps(user_login_details_no_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertIn('Please enter a valid Password.', data['message'])

    def test_login_user_wrong_password_given(self):
        self.client.post('/v1/auth/register', data=json.dumps(register_user3),
                         content_type='application/json')
        response = self.client.post('/v1/auth/login', data=json.dumps(user_login_details_wrong_password),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn('Invalid Password, Please try again', data['message'])


    def test_login_user_invalid_email_given(self):
        response = self.client.post('/v1/auth/login', data=json.dumps(user_login_details_invalid_email),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_login_user_new_email_given(self):
        response = self.client.post('/v1/auth/login', data=json.dumps(user_login_details_new_email),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        self.database.delete_all_tables()


if __name__ == "__main__":
    unittest.main()
