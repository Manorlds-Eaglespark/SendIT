import unittest
import json
import os
from app import create_app
from tests.data import quotation



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        config_name = os.getenv('APP_SETTINGS') # config_name = "development"
        self.app = create_app(config_name).test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDQ4ODY0MTcsImlhdCI6MTU0MjI5NDQxNywic3ViIjoyNSwiZW1sIjoiYWRtaW5Ac2VuZGl0LmNvbSJ9.yVwDGj0VV_JE_rJ-X4K2dKZgbG1JdvrahE9pZH-3PCs" +"_"
     
    def test_get_all_quotations(self):
        """"Test API to get all Parcel Delivery Orders"""
        response = self.app.get('/v1/quotations')#, headers=({"Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NjE0MzYsImlhdCI6MTU0MTc0NzAzNiwic3ViIjoxfQ.Giq3gqUSi50ombk7sVmMjgmDZUTCZkJPcMS10fmPfQI"})#{'Content-Type':'application/json',"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDE3NDU3MzcsImlhdCI6MTU0MTczODUzNywic3ViIjoxLCJuYW0iOiJBbm9ybGQgTXVrb25lIn0.l_-eGIDTrekTjvJ488dBSDUE5AdRdfhtgkQRSJdSy4M"})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status message"], "All Quotations For All Orders")

    def test_get_specific_quotation(self):
        """"Test API to get a Parcel Delivery Order"""
        response = self.app.get('/v1/quotations/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200) 

    def test_get_specific_quotation_not_there(self):
        """"Test API to get a quotation not already made"""
        response = self.app.get('/v1/quotations/100')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)


    def test_create_new_quotation_order(self):
        """"Test API to create new quotation"""
        response = self.app.post('/v1/quotations', data= json.dumps(quotation), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('New Quotation Successfully created.', data['status message'])
    

        
if __name__ == "__main__":
    unittest.main()
