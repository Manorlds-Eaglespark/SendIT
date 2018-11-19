
# app/models.py
import os
from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta


class User(db.Model):
	"""This class defines the users table """

	__tablename__ = 'users'

	# Define the columns of the users table, starting with the primary key
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(256), nullable=False)
	email = db.Column(db.String(256), nullable=False, unique=True)
	password = db.Column(db.String(256), nullable=False)
	about = db.Column(db.String(256), nullable=True)
	country = db.Column(db.String(256), nullable=False)
	photo = db.Column(db.String(256), nullable=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column( db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	posts = db.relationship('Post', order_by='Post.id', cascade="all, delete-orphan")
	medals = db.relationship('Medal', order_by='Medal.id', cascade="all, delete-orphan")
	events = db.relationship('Event', order_by='Event.id', cascade="all, delete-orphan")
	business_posts = db.relationship('BusinessPost', order_by='BusinessPost.id', cascade="all, delete-orphan")
	#tomatoes = db.relationship('Rotten_Tomato', order_by='Rotten_Tomato.id', cascade="all, delete-orphan")

	def __init__(self, name, about, email, password, country):
		"""Initialize the user with an email and a password."""
		self.name = name
		self.about = about
		self.email = email
		self.password = Bcrypt().generate_password_hash(password).decode()
		self.country = country
	   
	   
	def password_is_valid(self, password):
		"""
		Checks the password against it's hash to validates the user's password
		"""
		return Bcrypt().check_password_hash(self.password, password)

	def save(self):
		"""Save a user to the database.
		This includes creating a new user and editing one.
		"""
		db.session.add(self)
		db.session.commit()

	def generate_token(self, user_id, country, name):
		""" Generates the access token"""

		try:
			# set up a payload with an expiration time
			payload = {
				'exp': datetime.utcnow() + timedelta(minutes=120),
				'iat': datetime.utcnow(),
				'sub': user_id,
				'cty':country,
				'nam':name
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
			payload = jwt.decode(token, str(os.getenv('SECRET')))
			return payload['sub']
		except jwt.ExpiredSignatureError:
			# the token is expired, return an error string
			return "Expired token. Please login to get a new token"
		except jwt.InvalidTokenError:
			# the token is invalid, return an error string
			return "Invalid token. Please register or login"


	@staticmethod
	def decode_country(token):
		"""Decodes the access token from the Authorization header."""
		# try to decode the token using our SECRET variable
		payload = jwt.decode(token, str(os.getenv('SECRET')))
		return payload['cty']

	@staticmethod
	def decode_name(token):
		"""Decodes the access token from the Authorization header."""
		# try to decode the token using our SECRET variable
		return jwt.decode(token, str(os.getenv('SECRET')))['nam']

class Post(db.Model):
	"""This class defines the post table."""
	__tablename__ = 'posts'
	# define the columns of the table, starting with its primary key
	id = db.Column(db.Integer, primary_key=True)
	created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	creator_name = db.Column(db.String(255) , nullable=False)
	country = db.Column(db.String(255) , nullable=False)
	text = db.Column(db.String(255), nullable=False)
	image_filename = db.Column(db.String(255), default=None, nullable=True)
	image_url = db.Column(db.String(255), default=None, nullable=True)
	video = db.Column(db.String(255), nullable=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column( db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	post_replies = db.relationship('PostReply', order_by='PostReply.id', cascade="all, delete-orphan")
	medals = db.relationship('Medal', order_by='Medal.id', cascade="all, delete-orphan")
	#tomatoes = db.relationship('Rotten_Tomato', order_by='Rotten_Tomato.id', cascade="all, delete-orphan")
	

	def __init__(self, created_by, creator_name, country, text, image_filename, video):
		"""Initialize the post."""
		self.created_by = created_by
		self.creator_name = creator_name
		self.country = country
		self.text = text
		self.image_filename = image_filename
		self.video = video

	def save(self):
		"""Save a post.
		This applies for both creating a new post
		and updating an existing onupdate
		"""
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all(user_id):
		"""This method gets all the posts for a given user."""
		return Post.query.filter_by(created_by=user_id)

	def delete(self):
		"""Deletes a given post."""
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		"""Return a representation of a post instance."""
		return "<Post: {}>".format(self.text)




class PostReply(db.Model):
	"""This class defines the post table."""
	__tablename__ = 'post_replies'
	# define the columns of the table, starting with its primary key
	id = db.Column(db.Integer, primary_key=True)
	created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	post = db.Column(db.Integer, db.ForeignKey(Post.id), nullable=False)
	text = db.Column(db.String(255) , nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column( db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	

	def __init__(self, created_by, post, text):
		"""Initialize the post."""
		self.created_by = created_by
		self.post = post
		self.text = text

	def save(self):
		"""Save a post reply.
		This applies for both creating a new post reply
		and updating an existing onupdate
		"""
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all(post_id):
		"""This method gets all the posts for a given user."""
		return PostReply.query.filter_by(post=post_id)

	def delete(self):
		"""Deletes a given post."""
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		"""Return a representation of a post instance."""
		return "<PostReply: {}>".format(self.text)



class Medal(db.Model):
	"""This class defines the post table."""
	__tablename__ = 'medals'
	# define the columns of the table, starting with its primary key
	id = db.Column(db.Integer, primary_key=True)
	post = db.Column(db.Integer, db.ForeignKey(Post.id), nullable=False)
	created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column( db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	

	def __init__(self, post, created_by):
		"""Initialize the post."""
		self.created_by = created_by
		self.post = post

	def save(self):
		"""Save a post.
		This applies for both creating a new post
		and updating an existing onupdate
		"""
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all(post):
		"""This method gets all the posts for a given user."""
		return Medal.query.filter_by(post=post)

	def delete(self):
		"""Deletes a given post."""
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		"""Return a representation of a post instance."""
		return "<Medals: {}>".format(self.id)




class Event(db.Model):
	"""This class defines the events table."""
	__tablename__ = 'events'
	# define the columns of the table, starting with its primary key
	id = db.Column(db.Integer, primary_key=True)
	created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	creator_name = db.Column(db.String(255) , nullable=False)
	country = db.Column(db.String(255) , nullable=False)
	title = db.Column(db.String(255), nullable=False)
	details = db.Column(db.String(255), nullable=False)
	image = db.Column(db.String(255), nullable=True)
	dueDate = db.Column(db.String(255), nullable=True)
	startingTime  = db.Column(db.String, nullable=True)
	endingTime  = db.Column(db.String, nullable=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column( db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	

	def __init__(self, created_by, creator_name, country, title, details, image, dueDate, startingTime, endingTime):
		"""Initialize the post."""
		self.created_by = created_by
		self.country = country
		self.creator_name = creator_name
		self.title = title
		self.details = details
		self.image = image
		self.dueDate = dueDate
		self.startingTime = startingTime
		self.endingTime = endingTime 

	def save(self):
		"""Save a post.
		This applies for both creating a new post
		and updating an existing onupdate
		"""
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all(user_id):
		"""This method gets all the posts for a given user."""
		return Post.query.filter_by(created_by=user_id)

	def delete(self):
		"""Deletes a given post."""
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		"""Return a representation of a post instance."""
		return "<Event: {}>".format(self.text)



class BusinessPost(db.Model):
	"""This class defines the events table."""
	__tablename__ = 'business_post'
	# define the columns of the table, starting with its primary key
	id = db.Column(db.Integer, primary_key=True)
	created_by = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	creator_name = db.Column(db.String(255) , nullable=False)
	country = db.Column(db.String(255) , nullable=False)
	title = db.Column(db.String(255), nullable=False)
	details = db.Column(db.String(255), nullable=False)
	image = db.Column(db.String(255), nullable=True)
	currency = db.Column(db.String(255), nullable=True)
	price = db.Column(db.String(255), nullable=True)
	contact_details = db.Column(db.String(255), nullable=True)
	address  = db.Column(db.String, nullable=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column( db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
	

	def __init__(self, created_by, creator_name, country, title, details, image, currency, price, contact_details, address):
		"""Initialize the post."""
		self.created_by = created_by
		self.creator_name = creator_name
		self.country = country
		self.title = title
		self.details = details
		self.image = image
		self.currency = currency
		self.contact_details = contact_details
		self.price = price
		self.address = address

	def save(self):
		"""Save a post.
		This applies for both creating a new post
		and updating an existing onupdate
		"""
		db.session.add(self)
		db.session.commit()

	@staticmethod
	def get_all(user_id):
		"""This method gets all the posts for a given user."""
		return Post.query.filter_by(created_by=user_id)

	def delete(self):
		"""Deletes a given post."""
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		"""Return a representation of a post instance."""
		return "<BusinessPost: {}>".format(self.text)
