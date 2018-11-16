# app/models/Admin.py
from app.models.User import User

class Admin(User):
	"""This class defines an Admin for the SendIt platform"""

	initDict={
				"name":"_",
				"email":"_",
				"password":"dfsa",
				"is_admin":False
	}

	def __init__(self, initDict):
		"""Initialize the user with an email and a password."""
		super().__init__(initDict['name'], initDict['email'], initDict['password'])
		self.is_admin = True


