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


    def test_parcel_is_created(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user3),
                         content_type='application/json')
        response = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details3),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('You logged in successfully.', data['message'])
        response1 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
                                    content_type='application/json', headers=({"Authorization": "Bearer "+str(data['access_token'])+"_"}))
        data1 = json.loads(response1.data)
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(data1['message'], 'New Delivery Order Successfully Added. Email sent to Admin.')


    def test_admin_can_view_all_parcels(self):
        admin = Admin(admin_data)
        self.database.save_new_user(admin)
        response = self.client.post('/api/v1/auth/login', data=json.dumps(admin_login),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user4),
                         content_type='application/json')
        response1 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details4),
                                    content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        data1 = json.loads(response1.data)
        self.assertIn('You logged in successfully.', data1['message'])
        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
                                    content_type='application/json', headers=({"Authorization": "Bearer "+str(data1['access_token'])+"_"}))
        data2 = json.loads(response2.data)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(data2['message'], 'New Delivery Order Successfully Added. Email sent to Admin.')

        response3 = self.client.get('/api/v1/parcels', headers=({"Authorization": "Bearer " + str(data['access_token']) + "_"}))

        self.assertEqual(response3.status_code, 200)


    def test_non_admin_cannot_view_all_parcels(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user5),
                         content_type='application/json')
        response0 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details5),
                                     content_type='application/json')
        self.assertEqual(response0.status_code, 200)
        data0 = json.loads(response0.data)
        self.assertIn('You logged in successfully.', data0['message'])


        self.client.post('/api/v1/auth/register', data=json.dumps(register_user4),
                         content_type='application/json')
        response1 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details4),
                                    content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        data1 = json.loads(response1.data)
        self.assertIn('You logged in successfully.', data1['message'])

        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
                                    content_type='application/json', headers=({"Authorization": "Bearer "+str(data1['access_token'])+"_"}))
        data2 = json.loads(response2.data)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(data2['message'], 'New Delivery Order Successfully Added. Email sent to Admin.')

        response3 = self.client.get('/api/v1/parcels', headers=({"Authorization": "Bearer " + str(data0['access_token']) + "_"}))
        self.assertEqual(response3.status_code, 403)


    def test_creating_parcel_with_string_size(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user6),
                         content_type='application/json')
        response0 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details6),
                                     content_type='application/json')
        self.assertEqual(response0.status_code, 200)
        data0 = json.loads(response0.data)
        self.assertIn('You logged in successfully.', data0['message'])

        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_2),
                                        content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
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
                                        content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
        self.assertEqual(response2.status_code, 400)


    def test_normal_user_can_not_view_parcels_for_user(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user9),
                         content_type='application/json')
        response10 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details9),
                                     content_type='application/json')
        self.assertEqual(response10.status_code, 200)
        data10 = json.loads(response10.data)

        self.client.post('/api/v1/auth/register', data=json.dumps(register_user7),
                         content_type='application/json')
        response0 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details7),
                                     content_type='application/json')
        self.assertEqual(response0.status_code, 200)
        data0 = json.loads(response0.data)
        self.assertIn('You logged in successfully.', data0['message'])

        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_4),
                                        content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
        data2 = json.loads(response2.data)
        response3 = self.client.get('/api/v1/parcels/'+ str((data2['item'])['id']),
                                    headers=({"Authorization": "Bearer " + str(data10['access_token']) + "_"}))
        data3 = json.loads(response3.data)
        self.assertEqual(response3.status_code, 403)


    def test_get_parcels_by_user_id(self):
        admin = Admin(admin_data2)
        self.database.save_new_user(admin)
        response_ = self.client.post('/api/v1/auth/login', data=json.dumps(admin_data_login2),
                                    content_type='application/json')
        self.assertEqual(response_.status_code, 200)
        data_ = json.loads(response_.data)

        self.client.post('/api/v1/auth/register', data=json.dumps(register_user8),
                         content_type='application/json')
        response0 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details8),
                                     content_type='application/json')
        self.assertEqual(response0.status_code, 200)
        data0 = json.loads(response0.data)
        # self.assertIn('You logged in successfully.', data0['message'])

        response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_4),
                                        content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
        data2 = json.loads(response2.data)
        i_d = (data2['item'])['id']
        response3 = self.client.get('/api/v1/parcels/'+ str(i_d),
                                    headers=({"Authorization": "Bearer " + str(data_['access_token']) + "_"}))
        data3 = json.loads(response3.data)
        self.assertEqual(response3.status_code, 200)


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


    def test_cancel_parcel_not_found(self):
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

        self.client.post('/api/v1/auth/register', data=json.dumps(register_user11),
                         content_type='application/json')
        response10 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details11),
                                      content_type='application/json')
        data10 = json.loads(response10.data)

        response4 = self.client.put('/api/v1/parcels/1000/cancel',
                                    data=json.dumps(new_location),
                                    content_type='application/json', headers=({"Authorization": "Bearer "+str(data10['access_token'])+"_"}))
        self.assertEqual(response4.status_code, 403)


    def test_admin_changes_parcel_status(self):
        admin = Admin(admin_data3)
        self.database.save_new_user(admin)
        response_ = self.client.post('/api/v1/auth/login', data=json.dumps(admin_data_login3),
                                     content_type='application/json')
        self.assertEqual(response_.status_code, 200)
        data_ = json.loads(response_.data)

        self.client.post('/api/v1/auth/register', data=json.dumps(register_user3),
                         content_type='application/json')
        response1 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details3),
                                     content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data1 = json.loads(response1.data)
        self.assertIn('You logged in successfully.', data1['message'])
        response3 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
                                     content_type='application/json',
                                     headers=({"Authorization": "Bearer " + str(data1['access_token']) + "_"}))
        data3 = json.loads(response3.data)
        self.assertEqual(response3.status_code, 201)
        response4 = self.client.put('/api/v1/parcels/' + str((data3["item"])['id']) + '/presentLocation',
                                    data=json.dumps(new_location),
                                    content_type='application/json',
                                    headers=({"Authorization": "Bearer " + str(data['access_token']) + "_"}))
        data4 = json.loads(response4.data)
        self.assertEqual(response4.status_code, 202)


    def test_admin_enters_numeric_present_location(self):
        admin = Admin(admin_data2)
        self.database.save_new_user(admin)
        response_ = self.client.post('/api/v1/auth/login', data=json.dumps(admin_data_login2),
                                     content_type='application/json')
        self.assertEqual(response_.status_code, 200)
        data_ = json.loads(response_.data)

        self.client.post('/api/v1/auth/register', data=json.dumps(register_user13),
                         content_type='application/json')
        response1 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details13),
                                     content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        data1 = json.loads(response1.data)
        self.assertIn('You logged in successfully.', data1['message'])
        response3 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
                                     content_type='application/json',
                                     headers=({"Authorization": "Bearer " + str(data1['access_token']) + "_"}))
        data3 = json.loads(response3.data)
        self.assertEqual(response3.status_code, 201)

        response4 = self.client.put('/api/v1/parcels/' + str((data3["item"])['id']) + '/status',
                                    data=json.dumps(new_status),
                                    content_type='application/json',
                                    headers=({"Authorization": "Bearer " + str(data_['access_token']) + "_"}))
        self.assertEqual(response4.status_code, 202)


    def test_admin_changes_parcel_present_location(self):
        admin = Admin(admin_data)
        self.database.save_new_user(admin)
        response = self.client.post('/api/v1/auth/login', data=json.dumps(admin_login),
                                    content_type='application/json')
        data = json.loads(response.data)
        self.assertIn('You logged in successfully.', data['message'])
        self.client.post('/api/v1/auth/register', data=json.dumps(register_user3),
                         content_type='application/json')
        response1 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details3),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data1 = json.loads(response1.data)
        self.assertIn('You logged in successfully.', data1['message'])
        response3 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
                                    content_type='application/json', headers=({"Authorization": "Bearer "+str(data1['access_token'])+"_"}))
        data3 = json.loads(response3.data)
        self.assertEqual(response3.status_code, 201)
        response4 = self.client.put('/api/v1/parcels/'+str((data3["item"])['id'])+'/presentLocation', data=json.dumps(new_location),
                                    content_type='application/json', headers=({"Authorization": "Bearer "+str(data['access_token'])+"_"}))
        data4 = json.loads(response4.data)
        self.assertEqual(response4.status_code, 202)

    def test_admin_enters_numeric_present_location_(self):
        admin = Admin(admin_data2)
        self.database.save_new_user(admin)
        response_ = self.client.post('/api/v1/auth/login', data=json.dumps(admin_data_login2),
                                    content_type='application/json')
        self.assertEqual(response_.status_code, 200)
        data_ = json.loads(response_.data)

        self.client.post('/api/v1/auth/register', data=json.dumps(register_user10),
                                              content_type='application/json')
        response1 = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details10),
                             content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        data1 = json.loads(response1.data)
        self.assertIn('You logged in successfully.', data1['message'])
        response3 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
                             content_type='application/json', headers=({"Authorization": "Bearer "+str(data1['access_token'])+"_"}))
        data3 = json.loads(response3.data)
        self.assertEqual(response3.status_code, 201)

        response4 = self.client.put('/api/v1/parcels/'+str((data3["item"])['id'])+'/presentLocation', data=json.dumps(new_location2),
                                     content_type='application/json', headers=({"Authorization": "Bearer "+str(data_['access_token'])+"_"}))
        self.assertEqual(response4.status_code, 401)





    def tearDown(self):
        self.database.delete_all_tables()


if __name__ == "__main__":
    unittest.main()
