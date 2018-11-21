# app/models/Quotation.py

from datetime import datetime, timedelta

class Quotation():

	initDict = {
					"price":"____ UGX",
					"parcel_items":"__",
					"weight":"__ Kg",
					"sender_id":0,
					"receiver_name":"__",
					"receiver_contact":"__",
					"approx_delivery_duration":"__",
					"prepared_by":"__",
					"acceptance_status":"_"
				}

	def __init__(self, initDict):
		self.parcel_id = initDict["parcel_id"]
		self.price = initDict["price"]
		self.parcel_items = initDict["parcel_items"]
		self.weight = initDict["weight"]
		self.sender_id = initDict["sender_id"]
		self.receiver_name = initDict["receiver_name"]
		self.receiver_contact = initDict["receiver_contact"]
		self.approx_delivery_duration = initDict["approx_delivery_duration"]
		self.prepared_by = initDict["prepared_by"]
		self.acceptance_status = initDict["acceptance_status"]



	def __str__(self):
		return {
        			"id": self.id,
        			"parcel_id":self.parcel_id,
        			"price":self.price,
        			"parcel_items":self.parcel_items,
        			"weight":self.weight,
        			"sender_id":self.sender_id,
        			"receiver_name":self.receiver_name,
        			"receiver_contact":self.receiver_contact,
        			"approx_delivery_duration":self.approx_delivery_duration,
        			"prepared_by":self.prepared_by,
        			"acceptance_status":self.acceptance_status
    			}