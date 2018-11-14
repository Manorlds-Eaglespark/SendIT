import unittest
import json
import os
from app import create_app



class TestFlaskApi(unittest.TestCase):
    def setUp(self):
        config_name = os.getenv('APP_SETTINGS') # config_name = "development"
        self.app = create_app(config_name).test_client()
        self.app.environ_base['HTTP_AUTHORIZATION'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDM2NzY4OTcsImlhdCI6MTU0MTk0ODg5Nywic3ViIjoxfQ.xioVGMsrfzL86pcPdyXv1E-trTVkDfnQsNiutoieox8" +"_"
     
        self.quotation = {
                            "parcel_code":"i2531",
                            "price":"25000 UGX",
                            "parcel_items":"2 Bunches of Matooke",
                            "weight":"15 Kg",
                            "sender_id":2,
                            "receiver_name":"Anorld Mukone",
                            "receiver_contact":"0788229573",
                            "approx_delivery_duration":"3 Hours",
                            "acceptance_status":"Pending"
                    }

    
    def test_get_all_quotes(self):
        """"Test API to get all Parcel Delivery Orders"""
        response = self.app.get('/v1/parcels')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status message"], "All Parcel Delivery Orders")

    def test_get_all_quotation_for_specific_user(self):

    def test_get_a_specific_quotation(self):

    def test_get_a_non_existent_quotation(self):

    def test_admin_creates_new_quotation(self):

    def test_admin_creates_new_quotation_for_non_existent_parcel(self):

    def test_admin_creates_new_quotation_with_no_parcel_items(self):

    def test_user_accepts_quotation(self):
    
    def test_create_new_delivery_order(self):
        """"Test API to create new order"""
        response = self.app.post('/v1/parcels', data= json.dumps(self.parcel), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('New Delivery Order Successfully Added.', data['status message'])



        
if __name__ == "__main__":
    unittest.main()
