
# app/models.py
import os
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta


class User:
	"""This class defines the user model """

	def __init__(self, id, name, email, password):
		"""Initialize the user with an email and a password."""
		self.id = id
		self.name = name
		self.email = email
		self.password = Bcrypt().generate_password_hash(password).decode()

	def password_is_valid(self, password):
		"""
		Checks the password against it's hash to validates the user's password
		"""
		return Bcrypt().check_password_hash(self.password, password)

	def generate_token(self, user_id, name):
			""" Generates the access token"""

			try:
				# set up a payload with an expiration time
				payload = {    
					'exp': datetime.utcnow() + timedelta(minutes=28800),  #Expiry time is 20 days
					'iat': datetime.utcnow(),
					'sub': user_id
				}
				# create the byte string token using the payload and the SECRET key
				jwt_string = jwt.encode(
					payload,
					str(os.getenv('SECRET')),
					algorithm='HS256'
				)
				return jwt_string

			except Exception as e:
				# return an error in string format if an exception occurs
				return str(e)

	@staticmethod
	def decode_token(token):
		"""Decodes the access token from the Authorization header."""
		try:
			# try to decode the token using our SECRET variable
			payload = jwt.decode( token, str(os.getenv('SECRET')), algorithms='HS256')
			return payload['sub']
		except jwt.ExpiredSignatureError:
			# the token is expired, return an error string
			return "Expired token. Please login to get a new token"
		except jwt.InvalidTokenError:
			# the token is invalid, return an error string
			return "Invalid token. Please register or login"


class Admin(User):
	"""This class defines an Admin for the SendIt platform"""

	def __init__(self, id, name, email, password, is_admin):
		"""Initialize the user with an email and a password."""
		super().__init__(id, name, email, password)
		self.is_admin = True



class Parcel:
	"""This class defines the Orders."""

	initDict = {"id":0,
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
		self.id = initDict["id"]
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


	def __repr__(self):
		"""Return a representation of a post instance."""
		return "<Parcel: {}>".format(self.code)

