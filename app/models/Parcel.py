# app/models/Parcel.py
import uuid


class Parcel:
	"""This class defines the Orders."""

	initDict = {
				"code":"t2584",
				"sender_id":0,
				"status":"__",
				"pick_up_address":"_",
				"destination":"_",
				"description":"_",
				"sender_contact":"_",
				"receiver_name":"_",
				"receiver_contact":"_",
				"size":"xyz"}

	def __init__(self, initDict):
		"""Initialize the post."""
		self.id = uuid.uuid4
		self.code = initDict["code"]
		self.sender_id = initDict["sender_id"]
		self.status = initDict["status"]
		self.pick_up_address = initDict["pick_up_address"]
		self.destination = initDict["destination"]
		self.description = initDict["description"]
		self.sender_contact = initDict["sender_contact"]
		self.receiver_name = initDict["receiver_name"]
		self.receiver_contact = initDict["receiver_contact"]
		self.size = initDict["size"]


	def __str__(self):
		return {
        			"id": self.id,
        			"code":self.code,
        			"sender_id":self.sender_id,
        			"status":self.status,
        			"pick_up_address":self.pick_up_address,
        			"destination":self.destination,
        			"description":self.description,
        			"sender_contact":self.sender_contact,
        			"receiver_name":self.receiver_name,
        			"receiver_contact":self.receiver_contact,
        			"size":self.size
    			}

