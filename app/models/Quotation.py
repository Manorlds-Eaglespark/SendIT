# app/models/Quotation.py
import uuid
from app import db


class Quotation(db.Model):

	__tablename__ = 'quotations'

	# Define the columns of the users table, starting with the primary key
	id = db.Column(db.Integer, primary_key=True)
	parcel_id = db.Column(db.Integer, nullable=False, unique=True)
	price = db.Column(db.String(256), nullable=False)
	parcel_items = db.Column(db.String(256), nullable=False)
	weight = db.Column(db.String(256), nullable=False)
	sender_id = db.Column(db.Integer, nullable=False)
	receiver_name = db.Column(db.String(256), nullable=False)
	receiver_contact = db.Column(db.String(256), nullable=False)
	approx_delivery_duration = db.Column(db.String(256), nullable=False)
	prepared_by = db.Column(db.String(256), nullable=False)
	acceptance_status = db.Column(db.String(256), nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column( db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	
	initDict = {
					"parcel_id":0,
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
		self.id = int(uuid.uuid4().clock_seq)
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


	def save(self):
		db.session.add(self)
		db.session.commit()


	def delete(self):
		"""Deletes a given quotation."""
		db.session.delete(self)
		db.session.commit()


	@staticmethod
	def get_all(user_id):
		"""This method gets all the quotations for a given user."""
		return Quotation.query.filter_by(created_by=user_id)


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
