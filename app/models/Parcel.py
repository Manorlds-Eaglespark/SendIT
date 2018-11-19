# app/models/Parcel.py
import uuid
from app import db
from app.models.User import User


class Parcel(db.Model):
	"""This class defines the Parcels."""

	__tablename__ = 'parcels'


	# Define the columns of the users table, starting with the primary key
	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	status = db.Column(db.String(256), nullable=False)
	pick_up_address = db.Column(db.String(256), nullable=False)
	destination = db.Column(db.String(256), nullable=False)
	description = db.Column(db.String(256), nullable=False)
	sender_contact = db.Column(db.String(256), nullable=False)
	receiver_name = db.Column(db.String(256), nullable=False)
	receiver_contact = db.Column(db.String(256), nullable=False)
	size = db.Column(db.String(256), nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column( db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

	initDict = {
				"sender_id":0,
				"status":"__",
				"pick_up_address":"_",
				"destination":"_",
				"description":"_",
				"sender_contact":"_",
				"receiver_name":"_",
				"receiver_contact":"_",
				"size":"xyz"
				}

	def __init__(self, initDict):
		"""Initialize the post."""
		self.id = int(uuid.uuid4().clock_seq)
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

	def save(self):
		db.session.add(self)
		db.session.commit()


	def delete(self):
		"""Deletes a given parcel."""
		db.session.delete(self)
		db.session.commit()


	@staticmethod
	def get_all_by_user(user_id):
		"""This method gets all the parcels for a given user."""
		return Parcel.query.filter_by(sender_id=user_id)

