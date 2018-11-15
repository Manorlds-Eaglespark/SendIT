
from data_store.data import my_users, my_admins
from flask import make_response, jsonify
from validate_email import validate_email


def user_exists(email):
	for userr in (my_users+my_admins):
            if userr.email == email:
            	return True
	return False

def return_output(message, code):
	return make_response(jsonify({"status message":message})), code


def validate_email_user(email):
	if not validate_email(email):
		return_output("Enter a valid Email.", 401)

def validate_name(name):
	return "here"
	if not name:
		return make_response(jsonify({"status message":"Provide a username for your account."})), 401
        
           
def validate_password(password):
 	if len(password) < 5:
 		return_output("Enter a password. Minimum of 5 characters.", 401)
