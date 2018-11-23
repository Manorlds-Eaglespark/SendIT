import unittest
import json
from app import create_app
from app.database.Database import Database
from tests.data import *
from app.models.Admin import Admin
from app.data_store.data import admin_login, admin_data



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.database = Database()
        self.database.create_all_tables()

    def test_creating_parcel_with_string_size(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user6),
                         content_type='application/json')
        response0 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details6),
                                     content_type='application/json')
        self.assertEqual(response0.status_code, 200)
        data0 = json.loads(response0.data)
        self.assertIn('You logged in successfully.', data0['message'])

        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_2),
                                     content_type='application/json',
                                     headers=({"Authorization": "Bearer " + str(data0['access_token']) + "_"}))
        self.assertEqual(response2.status_code, 400)

    def test_creating_parcel_with_fields_missing(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user7),
                         content_type='application/json')
        response0 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details7),
                                     content_type='application/json')
        self.assertEqual(response0.status_code, 200)
        data0 = json.loads(response0.data)
        self.assertIn('You logged in successfully.', data0['message'])

        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_3),
                                     content_type='application/json',
                                     headers=({"Authorization": "Bearer " + str(data0['access_token']) + "_"}))
        self.assertEqual(response2.status_code, 400)

    def tearDown(self):
        self.database.delete_all_tables()


if __name__ == "__main__":
    unittest.main()
