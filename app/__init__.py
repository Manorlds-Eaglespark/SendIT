# app/__init__.py
"""File that has the routes for the api """
import os
import random
from flask_api import FlaskAPI
from flask import request, jsonify, make_response, abort
from app.models import User, Parcel
from data_store.data import my_parcels, my_users

# local import
from instance.config import app_config


def create_app(config_name):
    """Initialize the flask application"""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')

#***************************************Fetch all parcel delivery orders & Make a new parcel delivery order

    @app.route('/v1/parcels', methods=['POST', 'GET'])
    def parcels():
        """fetch all orders or make an order"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                if request.method == "POST":

                    if not (request.data['sender_contact']):
                        return make_response(jsonify({"status message":"Please provide all the required details"})), 400

                    id = len(my_parcels) + 1
                    code = "i"+ str(random.randint(1000, 9999))
                    sender_id = user_id
                    status = "Initiated"
                    pick_up_address = request.data['pick_up_address']
                    destination = request.data['destination']
                    description = request.data['description']
                    sender_contact = request.data['sender_contact']
                    receiver_name = request.data['receiver_name']
                    receiver_contact = request.data['receiver_contact']
                    size = request.data['size']

                    parcel = Parcel(id=id, code=code, sender_id=sender_id, status=status, pick_up_address=pick_up_address, destination=destination, description=description, sender_contact=sender_contact, receiver_name=receiver_name, receiver_contact=receiver_contact, size=size)
                    my_parcels.append(parcel)

                    item = {
                  
                    'id': parcel.id,
                    'code': parcel.code,
                    'sender_id':parcel.sender_id,
                    'status':parcel.status,
                    'pick_up_address': parcel.pick_up_address,
                    'destination': parcel.destination,
                    'description': parcel.description,
                    'sender_contact': parcel.sender_contact,
                    'receiver_name': parcel.receiver_name,
                    'receiver_contact':parcel.receiver_contact,
                    'size':parcel.size 
                    }
                    response = jsonify({"status message":"New Delivery Order Successfully Added.", "item":item})

                    return make_response(response), 201

                else:
                    # GET all the parcels
                    results = []

                    for parcel in my_parcels:
                        obj = {
                                'id': parcel.id,
                                'code': parcel.code,
                                'sender_id':parcel.sender_id,
                                'status':parcel.status,
                                'pick_up_address': parcel.pick_up_address,
                                'destination': parcel.destination,
                                'description': parcel.description,
                                'sender_contact': parcel.sender_contact,
                                'receiver_name': parcel.receiver_name,
                                'receiver_contact':parcel.receiver_contact,
                                'size':parcel.size
                        }
                        results.append(obj)

                    return make_response(jsonify({"status message":"All Parcel Delivery Orders", "meta": str(len(results))+" items returned","items":results})), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


#***************************************************************************Fetch all parcel delivery orders by a specific user

    @app.route('/v1/users/<userz_id>/parcels', methods=['GET'])
    def user_parcels(userz_id, **kwargs):
        """Fetch order from one user"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated
                results = []

                for parcel in my_parcels:
                    if parcel.sender_id == int(userz_id):
                        obj = {
                                'id': parcel.id,
                                'code': parcel.code,
                                'sender_id':parcel.sender_id,
                                'status':parcel.status,
                                'pick_up_address': parcel.pick_up_address,
                                'destination': parcel.destination,
                                'description': parcel.description,
                                'sender_contact': parcel.sender_contact,
                                'receiver_name': parcel.receiver_name,
                                'receiver_contact':parcel.receiver_contact,
                                'size':parcel.size
                        }
                        results.append(obj)
                if len(results):
                    return make_response(jsonify({"status message": "Success", "meta": str(len(results)) + " items returned", "items": results})), 200
                else:
                    return make_response(jsonify({"status message": "Fail- user has no orders or does not exist", "meta": str(len(results)) + " items returned"})), 404
              

#***************************************************************************Fetch a parcel delivery order

    @app.route('/v1/parcels/<int:id>', methods=['GET'])
    def my_parcel(id, **kwargs):
        """Fetch a specific parcel with its id"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                for prcl in my_parcels:
                    if prcl.id == id:
                        parcel = prcl
                        break
                else:
                    parcel = "Not there"

                if not isinstance(parcel, str):                    
                    if request.method == "GET":
            
                        # Handle GET request, sending back the post to the user
                        response = {
                                    "status":"Success, item found",
                                    "item":{
                                        'id': parcel.id,
                                        'code': parcel.code,
                                        'sender_id':parcel.sender_id,
                                        'status':parcel.status,
                                        'pick_up_address': parcel.pick_up_address,
                                        'destination': parcel.destination,
                                        'description': parcel.description,
                                        'sender_contact': parcel.sender_contact,
                                        'receiver_name': parcel.receiver_name,
                                        'receiver_contact':parcel.receiver_contact,
                                        'size':parcel.size

                                    }
                                    }
                        return make_response(jsonify(response)), 200

                else:
                    return make_response(jsonify({"message":"Sorry, Parcel not found!"})), 404
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401



#***************************************************************************Cancel a parcel delivery order

    @app.route('/v1/parcels/<int:id>/cancel', methods=['PUT'])
    def cancel_my_parcel(id, **kwargs):
        """Change the status of an order to canceled"""
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1][:-1]

        
        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                #Go ahead and handle the request, the user is authenticated

                for prcl in my_parcels:
                    if prcl.id == id:
                        parcel = prcl
                        break
                else:
                    parcel = "Not there"

                if not isinstance(parcel, str): 

                    if request.method == "PUT":
                        parcel.status = "Cancelled by Client"
                        my_parcels[parcel.id] = parcel
            
                        # Handle GET request, sending back the post to the user
                        response = {
                                    "status message":"Item Successfully Cancelled.",
                                    "item":{
                                            'id': parcel.id,
                                            'code': parcel.code,
                                            'sender_id':parcel.sender_id,
                                            'status':parcel.status,
                                            'pick_up_address': parcel.pick_up_address,
                                            'destination': parcel.destination,
                                            'description': parcel.description,
                                            'sender_contact': parcel.sender_contact,
                                            'receiver_name': parcel.receiver_name,
                                            'receiver_contact':parcel.receiver_contact,
                                            'size':parcel.size

                                            }
                                        }
                        return make_response(jsonify(response)), 202

                else:
                    return make_response(jsonify({"message":"Sorry, Parcel not found!"})), 404
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                # return an error response, telling the user he is Unauthorized
                return make_response(jsonify(response)), 401




# import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app