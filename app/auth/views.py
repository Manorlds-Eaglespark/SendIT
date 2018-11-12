# /app/auth/views.py

from . import auth_blueprint
from flask.views import MethodView
from flask import make_response, request, jsonify, abort
from app.models import User
from data_store.data import my_users
from validate_email import validate_email


class RegistrationView(MethodView):
    """This class registers a new user."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/auth/register"""
        user_exits = False
        # Query to see if the user already exists

        for userr in my_users:
            if userr.email == request.data['email']:
                user_exits = True
                break

        if not user_exits:
            try:
                name = request.data['name']
                if name == "":
                    return make_response(jsonify({"status message":"Please enter a Name for your account."})), 401
                email = request.data['email']
                if not validate_email(email):
                    return make_response(jsonify({"status message":"Please enter a valid Email."})), 401
                password = request.data['password']
                if password == "":
                    return make_response(jsonify({"status message":"Please enter a Password for your account."})), 401


                user = User(len(my_users), name, email, password)
                my_users.append(user)

                response = {
                        'status message': 'You registered successfully. Please log in.'
                    }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'status message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'status message': 'User already exists. Please login.'
            }
            return make_response(jsonify(response)), 202





class LoginView(MethodView):
    """This class-based view handles user login and access token generation."""

    def post(self):
        """Handle POST request for this view. Url ---> /v1/auth/login"""
        user_exits = False

        if request.data['password'] == "":
            return make_response(jsonify({"status message":"Please enter a valid Password."})), 401
        
        if not validate_email(request.data['email']):
            return make_response(jsonify({"status message":"Please enter a valid Email."})), 401
        try:
            # Get the user object using their email (unique to every user)
            user = ""

            for userr in my_users:
                if userr.email == request.data['email']:
                    user = userr
                    user_exits = True
                    break

            if user_exits:
                # Try to authenticate the found user using their password

                if user and user.password_is_valid(request.data['password']):

                    # Generate the access token. This will be used as the authorization header
                    access_token = user.generate_token(user.id, user.name)
                    if access_token:
                        response = {
                            'status message': 'You logged in successfully.',
                            'access_token':  access_token.decode()
                        }
                        return make_response(jsonify(response)), 200
                else:
                    # User does not exist. Therefore, we return an error message
                    response = {
                        'status message': 'Invalid email or password, Please edit, then try again'
                    }
                    return make_response(jsonify(response)), 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'status message': str(e)
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