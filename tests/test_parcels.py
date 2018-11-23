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



    def test_cancel_parcel(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user8),
                             content_type='application/json')
        response0 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details8),
                                     content_type='application/json')
        self.assertEqual(response0.status_code, 200)
        data0 = json.loads(response0.data)

        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_4),
                                        content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
        data2 = json.loads(response2.data)
        i_d = (data2['item'])['id']

        response4 = self.client.put('/api/v1/parcels/' + str(i_d) + '/cancel',
                                    data=json.dumps(new_location),
                                    content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
        self.assertEqual(response4.status_code, 202)


    def test_cancel_parcel_not_sent_by_user(self):

        self.client.post('/api/v1/auth/register', data=json.dumps(register_user12),
                             content_type='application/json')
        response0 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details12),
                                     content_type='application/json')
        self.assertEqual(response0.status_code, 200)
        data0 = json.loads(response0.data)

        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_4),
                                        content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
        data2 = json.loads(response2.data)
        i_d = (data2['item'])['id']

        response4 = self.client.put('/api/v1/parcels/' + str(i_d) + '/cancel',
                                    data=json.dumps(new_location),
                                    content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
        self.assertEqual(response4.status_code, 202)






    def tearDown(self):
        self.database.delete_all_tables()


if __name__ == "__main__":
    unittest.main()
