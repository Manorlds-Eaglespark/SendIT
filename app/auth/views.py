# /app/auth/views.py

from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, abort
from app.models.User import User
import re


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/auth/register"""

        name = request.data['name']

        if not isinstance(name, str) or len(name) < 3:
            return make_response(jsonify({"status message":"Name: - Enter only leters. More than 3 characters."})), 401

        email = request.data['email']
        
        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return make_response(jsonify({"status message":"Please enter a valid Email."})), 401

        password = request.data['password']
        if len(password) < 8:
            return make_response(jsonify({"status message":"Make sure your password is at lest 8 letters"})), 401
        elif re.search('[0-9]',password) is None:
            return make_response(jsonify({"status message":"Make sure your password has a number in it"})), 401
        elif re.search('[A-Z]',password) is None: 
            return make_response(jsonify({"status message":"Make sure your password has a capital letter in it"})), 401


        user = User.query.filter_by(email=request.data['email']).first()

        if not user:
            # There is no user so we'll try to register them
            try:
                post_data = request.data
                # Register the user
                name = post_data['name']
                email = post_data['email']
                password = post_data['password']
                user = User(name=name, email=email, password=password)
                user.save()


                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202





class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/auth/login"""
        
        password = request.data['password']
        email = request.data['email']

        if password == "":
            return make_response(jsonify({"status message":"Please enter a valid Password."})), 401

        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return make_response(jsonify({"status message":"Please enter a valid Email."})), 401

        try:
            # Get the user object using their email (unique to every user)
            user = User.query.filter_by(email=email).first()
            # Try to authenticate the found user using their password
            if user and user.password_is_valid(password):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id, user.email)
                if access_token:
                        response = {
                            'status message': 'You logged in successfully.',
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