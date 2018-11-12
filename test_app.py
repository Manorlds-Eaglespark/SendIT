import unittest
import json
import os
from app import create_app



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        config_name = os.getenv('APP_SETTINGS') # config_name = "development"
        self.app = create_app(config_name).test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDM2NzY4OTcsImlhdCI6MTU0MTk0ODg5Nywic3ViIjoxfQ.xioVGMsrfzL86pcPdyXv1E-trTVkDfnQsNiutoieox8" +"_"
        

        self.userr = {
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
        
        self.parcel = {
                        "description": "Need 4 speed cd",
                        "destination": "Banda stage, Jinja road",
                        "pick_up_address": "Ssebagala stage, Kisasi",
                        "receiver_contact": "0705622625",
                        "receiver_name": "Ian Kendrick",
                        "sender_contact": "0757877585",
                        "size": "Small Parcel: Documents, Envelope items. less than 20KGs",
                        "status": "Initiated by Client"
                    }

    
    def test_register_new_user(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/auth/register', data= json.dumps(self.userr), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('You registered successfully. Please log in.', data['status message'])

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
        

    
    def test_get_all_orders(self):
        """"Test API to get all Parcel Delivery Orders"""
        response = self.app.get('/v1/parcels')#, headers=({"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NjE0MzYsImlhdCI6MTU0MTc0NzAzNiwic3ViIjoxfQ.Giq3gqUSi50ombk7sVmMjgmDZUTCZkJPcMS10fmPfQI"})#{'Content-Type':'application/json',"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NDU3MzcsImlhdCI6MTU0MTczODUzNywic3ViIjoxLCJuYW0iOiJBbm9ybGQgTXVrb25lIn0.l_-eGIDTrekTjvJ488dBSDUE5AdRdfhtgkQRSJdSy4M"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status message"], "All Parcel Delivery Orders")

    def test_get_specific_delivery_order(self):
        """"Test API to get all Parcel Delivery Orders"""
        response = self.app.get('/v1/parcels/1')#, headers=({"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NjE0MzYsImlhdCI6MTU0MTc0NzAzNiwic3ViIjoxfQ.Giq3gqUSi50ombk7sVmMjgmDZUTCZkJPcMS10fmPfQI"})#{'Content-Type':'application/json',"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NDU3MzcsImlhdCI6MTU0MTczODUzNywic3ViIjoxLCJuYW0iOiJBbm9ybGQgTXVrb25lIn0.l_-eGIDTrekTjvJ488dBSDUE5AdRdfhtgkQRSJdSy4M"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)   


    def test_get_specific_delivery_order_not_there(self):
        """"Test API to get all Parcel Delivery Orders"""
        response = self.app.get('/v1/parcels/100')#, headers=({"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NjE0MzYsImlhdCI6MTU0MTc0NzAzNiwic3ViIjoxfQ.Giq3gqUSi50ombk7sVmMjgmDZUTCZkJPcMS10fmPfQI"})#{'Content-Type':'application/json',"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NDU3MzcsImlhdCI6MTU0MTczODUzNywic3ViIjoxLCJuYW0iOiJBbm9ybGQgTXVrb25lIn0.l_-eGIDTrekTjvJ488dBSDUE5AdRdfhtgkQRSJdSy4M"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)


    def test_create_new_delivery_order(self):
        """"Test API to create a new user"""
        response = self.app.post('/v1/parcels', data= json.dumps(self.parcel), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('New Delivery Order Successfully Added.', data['status message'])


    def test_cancel_a_delivery_order(self):
        """"Test API to create a new user"""
        response = self.app.put('/v1/parcels/2/cancel')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 202)
        self.assertIn('Item Successfully Cancelled', data['status message'])


    def test_get_delivery_orders_for_a_specific_user(self):
        """"Test API to create a new user"""
        response = self.app.get('/v1/users/2/parcels')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Success', data['status message'])

    def test_get_delivery_orders_for_a_specific_user_not_registered(self):
        """"Test API to create a new user"""
        response = self.app.get('/v1/users/200/parcels')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Fail- user has no orders or does not exist', data['status message'])


        
if __name__ == "__main__":
    unittest.main()
