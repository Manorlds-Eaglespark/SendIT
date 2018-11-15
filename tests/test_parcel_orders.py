import unittest
import json
import os
from app import create_app
from tests.data import parcel



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        config_name = os.getenv('APP_SETTINGS') # config_name = "development"
        self.app = create_app(config_name).test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDM2NzY4OTcsImlhdCI6MTU0MTk0ODg5Nywic3ViIjoxfQ.xioVGMsrfzL86pcPdyXv1E-trTVkDfnQsNiutoieox8" +"_"

    
    def test_get_all_orders(self):
        """"Test API to get all Parcel Delivery Orders"""
        response = self.app.get('/v1/parcels')#, headers=({"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NjE0MzYsImlhdCI6MTU0MTc0NzAzNiwic3ViIjoxfQ.Giq3gqUSi50ombk7sVmMjgmDZUTCZkJPcMS10fmPfQI"})#{'Content-Type':'application/json',"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NDU3MzcsImlhdCI6MTU0MTczODUzNywic3ViIjoxLCJuYW0iOiJBbm9ybGQgTXVrb25lIn0.l_-eGIDTrekTjvJ488dBSDUE5AdRdfhtgkQRSJdSy4M"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status message"], "All Parcel Delivery Orders")

    def test_get_specific_delivery_order(self):
        """"Test API to get a Parcel Delivery Order"""
        response = self.app.get('/v1/parcels/1')#, headers=({"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NjE0MzYsImlhdCI6MTU0MTc0NzAzNiwic3ViIjoxfQ.Giq3gqUSi50ombk7sVmMjgmDZUTCZkJPcMS10fmPfQI"})#{'Content-Type':'application/json',"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NDU3MzcsImlhdCI6MTU0MTczODUzNywic3ViIjoxLCJuYW0iOiJBbm9ybGQgTXVrb25lIn0.l_-eGIDTrekTjvJ488dBSDUE5AdRdfhtgkQRSJdSy4M"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)   


    def test_get_specific_delivery_order_not_there(self):
        """"Test API to get an order not already made"""
        response = self.app.get('/v1/parcels/100')#, headers=({"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NjE0MzYsImlhdCI6MTU0MTc0NzAzNiwic3ViIjoxfQ.Giq3gqUSi50ombk7sVmMjgmDZUTCZkJPcMS10fmPfQI"})#{'Content-Type':'application/json',"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NDU3MzcsImlhdCI6MTU0MTczODUzNywic3ViIjoxLCJuYW0iOiJBbm9ybGQgTXVrb25lIn0.l_-eGIDTrekTjvJ488dBSDUE5AdRdfhtgkQRSJdSy4M"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)


    def test_create_new_delivery_order(self):
        """"Test API to create new order"""
        response = self.app.post('/v1/parcels', data= json.dumps(parcel), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('New Delivery Order Successfully Added.', data['status message'])

    def test_get_delivery_orders_for_a_specific_user_not_registered(self):
        """"Test API to get orders for a user not registered"""
        response = self.app.get('/v1/users/200/parcels')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('Fail- user has no orders or does not exist', data['status message'])


        
if __name__ == "__main__":
    unittest.main()
