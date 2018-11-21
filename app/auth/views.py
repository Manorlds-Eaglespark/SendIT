# /app/auth/views.py
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, abort, json
from app.models.User import User
from app.database.Database import Database
import re

database = Database()


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/auth/register"""

        name = json.loads(request.data)['name']

        if not isinstance(name, str) or len(name) < 3:
            return make_response(jsonify({"message":"Name field: - Enter only letters. More than 3 characters."})), 401

        email = json.loads(request.data)['email']
        
        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return make_response(jsonify({"message":"Please enter a valid Email."})), 401

        password = json.loads(request.data)['password']
        if len(password) < 8:
            return make_response(jsonify({"message":"Make sure your password is at lest 8 letters"})), 401
        elif re.search('[0-9]',password) is None:
            return make_response(jsonify({"message":"Make sure your password has a number in it"})), 401
        elif re.search('[A-Z]',password) is None: 
            return make_response(jsonify({"message":"Make sure your password has a capital letter in it"})), 401


        user = database.get_registered_user(email)

        if not user:
            # There is no user so we'll try to register them
            try:
                user = User(name=name, email=email, password=password)
                database.save_new_user(user)
                ##save this user


                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occurred, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 400
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 403





class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/auth/login"""
        
        password = json.loads(request.data)['password']
        email = json.loads(request.data)['email']

        if password == "":
            return make_response(jsonify({"message":"Please enter a valid Password."})), 401

        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return make_response(jsonify({"message":"Please enter a valid Email."})), 401

        try:
            # Get the user object using their email (unique to every user)
            data = database.get_registered_user(email)
            if data:
                user = User(data[1], data[2], data[3])##get user
                # Try to authenticate the found user using their password
                if data and User.password_is_valid(data[3], password):
                    # Generate the access token. This will be used as the authorization header
                    access_token = user.generate_token(data[0], user.email)
                    if access_token:
                            response = {
                                'message': 'You logged in successfully.',
                                'access_token':  access_token.decode()
                            }
                            return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500


# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/v1/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the registration url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/v1/auth/login',
    view_func=login_view,
    methods=['POST']

)