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

    def test_get_list_of_users(self):
        admin = Admin(admin_data)
        self.database.save_new_user(admin)
        response = self.client.post('/api/v1/auth/login', data=json.dumps(admin_login),
                         content_type='application/json')
        data = json.loads(response.data)
        response2 = self.client.get('/api/v2/users',  headers=({"Authorization": "Bearer " + str(data['access_token']) + "_"}))
        data2 = json.loads(response2.data)
        self.assertEqual(response2.status_code, 200)

    def test_get_list_of_users_user_not_admin(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user3),
                         content_type='application/json')
        response = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details3),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        response2 = self.client.get('/api/v2/users',  headers=({"Authorization": "Bearer " + str(data['access_token']) + "_"}))
        data2 = json.loads(response2.data)
        self.assertEqual(response2.status_code, 403)




    def tearDown(self):
        self.database.delete_all_tables()
