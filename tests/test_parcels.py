# import sys
# import os
# # sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
# import unittest
# import json
# from app import create_app
# from app.database.Database import Database
# from tests.data import *
#
#
#
# class TestFlaskApi(unittest.TestCase):
#     def setUp(self):
#
#         self.app = create_app(config_name="development")
#         self.client = self.app.test_client()
#         self.database = Database()
#         with self.app.app_context():
#             self.database.delete_all_tables()
#             self.database.create_all_tables()
#         self.client.environ_base[
#             'HTTP_AUTHORIZATION'] = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDUzODQ5MDgsImlhdCI6MTU0Mjc5MjkwOCwic3ViIjoyLCJlbWwiOiJta2Fub3JsZHNhcGllbnNAZ21haWwuY29tIn0.ajhX8Hd9PrNRi8NdMGCGP7rrJzVUUXfw0SW7u0xUja8" + "_"
#         self.parcel = {
#             "description": "Need 4 speed cd",
#             "destination": "Banda stage, Jinja road",
#             "pick_up_address": "Ssebagala stage, Kisasi",
#             "receiver_contact": "0705622625",
#             "receiver_name": "Ian Kendrick",
#             "sender_contact": "0757877585",
#             "size": "Small Parcel: Documents, Envelope items. less than 20KGs",
#             "status": "Initiated by Client"
#         }
#
#     # def test_get_all_orders(self):
#     #     """"Test API to get all Parcel Delivery Orders"""
#     #     response = self.app.get(
#     #         '/v1/parcels')
#     #     data = json.loads(response.data)
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertEqual(data["status message"], "All Parcel Delivery Orders")
#     # #
#     # def test_get_specific_delivery_order(self):
#     #     response = self.app.get('/v1/parcels/1')
#     #     data = json.loads(response.data)
#     #     self.assertEqual(response.status_code, 200)
#     #
#     # def test_get_specific_delivery_order_not_there(self):
#     #     response = self.app.get(
#     #         '/v1/parcels/100')
#     #     data = json.loads(response.data)
#     #     self.assertEqual(response.status_code, 404)
#     #
#     def test_create_new_delivery_order(self):
#         pass
#         # response = self.client.post('/v1/parcels', data=json.dumps(self.parcel), content_type='application/json')
#         # data = json.loads(response.data)
#         # self.assertEqual(response.status_code, 201)
#         # self.assertIn('New Delivery Order Successfully Added.', data['status message'])
#
#     # def test_cancel_a_delivery_order(self):
#     #     response = self.app.put('/v1/parcels/2/cancel')
#     #     data = json.loads(response.data)
#     #     self.assertEqual(response.status_code, 202)
#     #     self.assertIn('Item Successfully Cancelled', data['status message'])
#     #
#     # def test_get_delivery_orders_for_a_specific_user(self):
#     #     response = self.app.get('/v1/users/2/parcels')
#     #     data = json.loads(response.data)
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertIn('Success', data['status message'])
#     #
#     # def test_get_delivery_orders_for_a_specific_user_not_registered(self):
#     #     response = self.app.get('/v1/users/200/parcels')
#     #     data = json.loads(response.data)
#     #     self.assertEqual(response.status_code, 404)
#     #     self.assertIn('Fail- user has no orders or does not exist', data['status message'])
#
#
#     def tearDown(self):
#         self.database.delete_all_tables()
#
#
# if __name__ == "__main__":
#     unittest.main()
