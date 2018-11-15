# app/models/Admin.py

class Admin(User):
	"""This class defines an Admin for the SendIt platform"""

	def __init__(self, id, name, email, password, is_admin):
		"""Initialize the user with an email and a password."""
		super().__init__(id, name, email, password)
		self.is_admin = True


