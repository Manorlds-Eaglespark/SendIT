# app/models/User.py
import os
import uuid
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta



class User:

	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = Bcrypt().generate_password_hash(password).decode()
		self.is_admin = "False"
		self.date_created = datetime.now()
		self.date_modified = datetime.now()


	def password_is_valid(self, password):
		return Bcrypt().check_password_hash(self.password, password)

	def generate_token(self, user_id, email, is_admin):

			try:
				# set up a payload with an expiration time
				payload = {
					'exp': datetime.utcnow() + timedelta(minutes=120),
					'iat': datetime.utcnow(),
					'sub': user_id,
					'eml': email,
					'adn':is_admin
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
	def password_is_valid(password1, password2):
		"""
		Checks the password against it's hash to validates the user's password
		"""
		return Bcrypt().check_password_hash(password1, password2)

	@staticmethod
	def decode_admin_status(token):
		"""Decodes the email from the Authorization header."""
		payload = jwt.decode( token, str(os.getenv('SECRET')), algorithms='HS256')
		return payload['adn']

	@staticmethod
	def decode_email(token):
		"""Decodes the email from the Authorization header."""
		payload = jwt.decode( token, str(os.getenv('SECRET')), algorithms='HS256')
		return payload['eml']
		
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

	@staticmethod
	def users_list(users):
		users_list = []
		for user in users:
			user_obj = {
							'id': str(user[0]),
							'name': str(user[1]),
							'email': str(user[2]),
							'password': str(user[3]),
							'is_admin': str(user[4]),
							'date_created': str(user[5]),
							'date_modified': str(user[6])
						}
			users_list.append(user_obj)
		return users_list

	@staticmethod
	def user_dictionary(user):
		user_obj = {
			'id': str(user[0]),
			'name': str(user[1]),
			'email': str(user[2]),
			'password': str(user[3]),
			'is_admin': str(user[4]),
			'date_created': str(user[5]),
			'date_modified': str(user[6])
		}
		return user_obj