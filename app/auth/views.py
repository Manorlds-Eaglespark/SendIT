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

        validate_name = name.replace(" ", "")
        if not validate_name.isalnum() and not validate_name.isalpha():
            return make_response(jsonify({"message": "Enter only letter in the English alphabet for name."})), 400

        if not isinstance(name, str) or len(name) < 3:
            return make_response(jsonify({"message":"Enter more than 3 letters for name."})), 401

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
            try:
                user = User(name=name, email=email, password=password)
                database.save_new_user(user)


                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                return make_response(jsonify(response)), 201
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 400
        else:
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

        if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return make_response(jsonify({"message":"Please enter a valid Email."})), 401

        try:
            data = database.get_registered_user(email)
            if data:
                user = User(data[1], data[2], data[3])
                if data and User.password_is_valid(data[3], password):
                    access_token = user.generate_token(data[0], user.email, data[4])
                    if access_token:
                            response = {
                                'message': 'You logged in successfully.',
                                'access_token':  access_token.decode()
                            }
                            return make_response(jsonify(response)), 200
                else:
                    response = {
                        'message': 'Invalid Password, Please try again'
                    }
                    return make_response(jsonify(response)), 403
            else:
                response = {
                    'message': 'No account by that Email, please register first.'
                }
                return make_response(jsonify(response)), 400

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

auth_blueprint.add_url_rule(
    '/api/v1/auth/register',
    view_func=registration_view,
    methods=['POST'])

auth_blueprint.add_url_rule(
    '/api/v1/auth/login',
    view_func=login_view,
    methods=['POST']

)