# app/models/Parcel.py

from datetime import datetime

class Parcel:
	init_dict = {
				"sender_id":0,
				"status":"__",
				"pick_up_address":"_",
				"destination":"_",
				"current_location":"_",
				"description":"_",
				"sender_contact":"_",
				"receiver_name":"_",
				"receiver_contact":"_",
				"size":"xyz"
				}

	def __init__(self, init_dict):
		"""Initialize the post."""
		self.sender_id = init_dict["sender_id"]
		self.status = init_dict["status"]
		self.pick_up_address = init_dict["pick_up_address"]
		self.destination = init_dict["destination"]
		self.current_location = init_dict["current_location"]
		self.description = init_dict["description"]
		self.sender_contact = init_dict["sender_contact"]
		self.receiver_name = init_dict["receiver_name"]
		self.receiver_contact = init_dict["receiver_contact"]
		self.size = init_dict["size"]
		self.date_created = datetime.now()
		self.date_modified = datetime.now()

	def __str__(self):
		return {
        			"sender_id":self.sender_id,
        			"status":self.status,
        			"pick_up_address":self.pick_up_address,
        			"destination":self.destination,
					"current_location":self.current_location,
        			"description":self.description,
        			"sender_contact":self.sender_contact,
        			"receiver_name":self.receiver_name,
        			"receiver_contact":self.receiver_contact,
        			"size":self.size
    			}