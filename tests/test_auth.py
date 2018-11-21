import unittest
import os
import json
# from app import create_app
# from tests.data import register_user

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from app import create_app
from app.database.TestDatabase import TestDatabase
from tests.data import register_user



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        config_name = os.getenv('APP_SETTINGS') # config_name = "development"
        self.app = create_app(config_name).test_client()
        self.database = TestDatabase()
        self.database.create_all_tables()

    def test_register_new_user(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/auth/register', data=json.dumps(register_user), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('You registered successfully. Please log in.', data['status message'])

    def tearDown(self):
        self.database.delete_all_tables()


if __name__ == "__main__":
    unittest.main()
