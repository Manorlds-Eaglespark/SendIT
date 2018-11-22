# app/models/Admin.py
from app.models.User import User

class Admin(User):
	init_dict={
				"name":"_",
				"email":"_",
				"password":"dfsa",
				"is_admin":"True"
	}

	def __init__(self, init_dict):
		"""Initialize the user with an email and a password."""
		super().__init__(init_dict['name'], init_dict['email'], init_dict['password'])
		self.is_admin = "True"


