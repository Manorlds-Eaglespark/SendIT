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
        # self.assertIn('You logged in successfully.', data['message'])


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




    # def test_get_parcels_by_user_id_not_there(self):
    #     pass
    # def test_get_parcels_by_user_with_no_parcel_orders(self):
    #     pass
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
        # self.assertIn('You need to be admin to view this info.', data3['message'])
        self.assertEqual(response3.status_code, 200)
        # # self.assertIn('You logged in successfully.', data3['message'])



    # def test_cancel_parcel(self):
    #     pass
    # def test_cancel_parcel_not_sent_by_user(self):
    #     pass
    # def test_cancel_parcel_not_found(self):
    #     pass
    #
    # def test_user_changes_destination(self):
    #     pass
    # def test_user_enters_numbers_as_new_destination_new_address(self):
    #     pass
    # def test_user_changes_destination_for_cancelled_parcel(self):
    #     pass
    # def test_user_changes_destination_for_delivered_parcel(self):
    #     pass
    # def test_user_changes_destination_for_parcel_not_theirs(self):
    #     pass

    #
    # def test_admin_changes_parcel_status(self):
    #     pass
    # def test_non_admin_changes_parcel_status(self):
    #     pass
    # def test_admin_changes_status_of_non_existent_parcel(self):
    #     pass
    # def test_admin_changes_status_for_cancelled_parcel(self):
    #     pass
    # def test_admin_changes_status_for_delivered_parcel(self):
    #     pass
    # def test_admin_enters_numeric_status(self):
    #     pass


    #
    # def test_admin_changes_parcel_present_location(self):
    #     admin = Admin(admin_data)
    #     self.database.save_new_user(admin)
    #     response = self.client.post('/api/v1/auth/login', data=json.dumps(admin_login),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertIn('You logged in successfully.', data['message'])
    #     response1 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
    #                                 content_type='application/json', headers=({"Authorization": "Bearer "+str(data['access_token'])+"_"}))
    #     data1 = json.loads(response.data)
    #
    #     self.client.post('/api/v1/auth/register', data=json.dumps(register_user3),
    #                      content_type='application/json')
    #     response = self.client.post('/api/v1/auth/login', data=json.dumps(user_login_details3),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data)
    #     self.assertIn('You logged in successfully.', data['message'])
    #     response3 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_1),
    #                                 content_type='application/json', headers=({"Authorization": "Bearer "+str(data['access_token'])+"_"}))
    #     data3 = json.loads(response3.data)
    #     self.assertEqual(response3.status_code, 201)
    #
    #     response4 = self.client.put('/api/v1/parcels/{data3["item"]}/presentLocation, data=json.dumps(new_parcel_1),
    #                                 content_type='application/json', headers=({"Authorization": "Bearer "+str(data['access_token'])+"_"}))

    # #
    # def test_non_admin_changes_parcel_present_location(self):
    #     pass
    #
    # def test_admin_changes_present_location_of_non_existent_parcel(self):
    #     pass
    #
    # def test_admin_changes_present_location_for_cancelled_parcel(self):
    #     pass
    #
    # def test_admin_changes_present_location_for_delivered_parcel(self):
    #     pass
    #
    # def test_admin_enters_numeric_present_location(self):
    #     admin = Admin(admin_data2)
    #     self.database.save_new_user(admin)
    #     response_ = self.client.post('/api/v1/auth/login', data=json.dumps(admin_data_login2),
    #                                 content_type='application/json')
    #     self.assertEqual(response_.status_code, 200)
    #     data_ = json.loads(response_.data)
    #
    #
    #
    #     response = self.client.put('/api/v1/parcels/id/ presentLocation', data=json.dumps(admin_data_login2),
    #                                  content_type='application/json')
    #     self.assertEqual(response_.status_code, 200)
    #     data_ = json.loads(response_.data)
    #
    #
    #     response2 = self.client.post('/api/v1/parcels', data=json.dumps(new_parcel_5),
    #                                     content_type='application/json', headers=({"Authorization": "Bearer "+str(data0['access_token'])+"_"}))
    #     data2 = json.loads(response2.data)

    def tearDown(self):
        self.database.delete_all_tables()


if __name__ == "__main__":
    unittest.main()
